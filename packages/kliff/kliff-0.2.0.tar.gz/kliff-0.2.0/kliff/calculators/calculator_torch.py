import logging
import multiprocessing as mp
import os
from pathlib import Path
from typing import Dict, List, Optional

import torch
import torch.distributed as dist
from kliff.dataset.dataset import Configuration
from kliff.dataset.dataset_torch import FingerprintsDataset, fingerprints_collate_fn
from kliff.models.model_torch import ModelTorch
from kliff.models.neural_network import NeuralNetwork
from torch.nn.parallel import DistributedDataParallel
from torch.utils.data import DataLoader

logger = logging.getLogger(__name__)


class CalculatorTorch:
    """
    A calculator for torch based models.

    Args:
        model: torch models, e.g. :class:`~kliff.neuralnetwork.NeuralNetwork`.
    """

    implemented_property = ["energy", "forces", "stress"]

    def __init__(self, model: ModelTorch):

        self.model = model
        self.dtype = self.model.descriptor.dtype
        self.fingerprints_path = None

        self.use_energy = None
        self.use_forces = None
        self.use_stress = None

        self.results = dict([(i, None) for i in self.implemented_property])

    def create(
        self,
        configs: List[Configuration],
        use_energy: bool = True,
        use_forces: bool = True,
        use_stress: bool = False,
        fingerprints_path: Optional[Path] = None,
        fingerprints_mean_and_stdev_path: Optional[Path] = None,
        reuse: bool = False,
        serial: bool = False,
        nprocs: int = mp.cpu_count(),
    ):
        """
        Process configs to generate fingerprints.

        Args:
            configs: atomic configurations
            use_energy: Whether to require the calculator to compute energy.
            use_forces: Whether to require the calculator to compute forces.
            use_stress: Whether to require the calculator to compute stress.
            fingerprints_path: Path to the to be generated fingerprints. If ``None``,
            default to ``./fingerprint.pkl``.
            fingerprints_mean_and_stdev_path: Path to the mean and standard deviation of
                the fingerprints. If ``normalize`` is not required by a descriptor,
                this is ignored. Otherwise, the mean and standard deviation read from
                ``fingerprints_mean_and_stdev_path``, are used to normalize the
                fingerprints. If ``None``, mean and standard deviation will be calculated
                from the descriptors and write to ``./fingerprints_mean_and_stdev.pkl``;
            reuse: If ``True``, reuse the fingerprints if found existing one. Otherwise,
                generate fingerprints from scratch no matter there is existing one or not.
            serial: Compute fingerprints in serial mode. Memory efficient.
            nprocs: Number of processes to use to generate the fingerprints.
                If ``serial`` is ``True``, this is ignored.
        """

        self.configs = configs
        self.use_energy = use_energy
        self.use_forces = use_forces
        self.use_stress = use_stress

        if isinstance(configs, Configuration):
            configs = [configs]

        # generate pickled fingerprints
        self.fingerprints_path = self.model.descriptor.generate_fingerprints(
            configs,
            use_forces,
            use_stress,
            reuse,
            fingerprints_path,
            fingerprints_mean_and_stdev_path,
            serial,
            nprocs,
        )

    def get_compute_arguments(self, batch_size: int = 1):
        """
        Return the dataloader with batch size set to ``batch_size``.
        """
        fname = self.fingerprints_path
        fp = FingerprintsDataset(fname)
        loader = DataLoader(
            dataset=fp, batch_size=batch_size, collate_fn=fingerprints_collate_fn
        )

        return loader

    def fit(self):
        path = self.fingerprints_path
        self.model.fit(path)

    def compute(self, batch):

        grad = self.use_forces or self.use_stress

        # collate batch input to NN
        zeta_config = [sample["zeta"] for sample in batch]
        if grad:
            for zeta in zeta_config:
                zeta.requires_grad_(True)

        # evaluate model
        zeta_stacked = torch.cat(zeta_config, dim=0)
        energy_atom = self.model(zeta_stacked)

        # energy
        natoms_config = [len(zeta) for zeta in zeta_config]
        energy_config = [e.sum() for e in torch.split(energy_atom, natoms_config)]

        # forces and stress
        if not self.use_forces:
            forces_config = None
        else:
            forces_config = []
        if not self.use_stress:
            stress_config = None
        else:
            stress_config = []
        if grad:
            for i, sample in enumerate(batch):

                # derivative of energy w.r.t. zeta
                energy = energy_config[i]
                zeta = zeta_config[i]
                dedz = torch.autograd.grad(energy, zeta, create_graph=True)[0]
                zeta.requires_grad_(False)  # no need of grad any more

                if self.use_forces:
                    dzetadr_forces = sample["dzetadr_forces"]
                    f = self.compute_forces(dedz, dzetadr_forces)
                    forces_config.append(f)

                if self.use_stress:
                    dzetadr_stress = sample["dzetadr_stress"]
                    volume = sample["dzetadr_volume"]
                    s = self.compute_stress(dedz, dzetadr_stress, volume)
                    stress_config.append(s)

        self.results["energy"] = energy_config
        self.results["forces"] = forces_config
        self.results["stress"] = stress_config
        return {
            "energy": energy_config,
            "forces": forces_config,
            "stress": stress_config,
        }

    @staticmethod
    def compute_forces(denergy_dzeta, dzetadr):
        forces = -torch.tensordot(denergy_dzeta, dzetadr, dims=([0, 1], [0, 1]))
        return forces

    @staticmethod
    def compute_stress(denergy_dzeta, dzetadr, volume):
        forces = torch.tensordot(denergy_dzeta, dzetadr, dims=([0, 1], [0, 1])) / volume
        return forces

    def get_energy(self, batch):
        return self.results["energy"]

    def get_forces(self, batch):
        return self.results["forces"]

    def get_stress(self, batch):
        return self.results["stress"]


class CalculatorTorchSeparateSpecies(CalculatorTorch):
    """
    A calculator supporting models of difference species.

    Args:
        models: {species:model} with species specifying the chemical symbol for the model.
    """

    def __init__(
        self,
        models: Dict[str, NeuralNetwork],
    ):
        self.models = models

        self.dtype = None
        for s, m in self.models.items():
            if self.dtype is None:
                self.dtype = m.descriptor.dtype
            else:
                if self.dtype != m.descriptor.dtype:
                    raise CalculatorTorchError("inconsistent `dtype` from descriptors.")

        # TODO change this (we now temporarily set model to the last one)
        self.model = m

        self.fingerprints_path = None

        self.use_energy = None
        self.use_forces = None
        self.use_stress = None

        self.results = dict([(i, None) for i in self.implemented_property])

    def compute(self, batch):

        grad = self.use_forces or self.use_stress

        # collate batch by species
        zeta_config = [sample["zeta"] for sample in batch]
        if grad:
            for zeta in zeta_config:
                zeta.requires_grad_(True)

        supported_species = self.models.keys()
        zeta_by_species = {s: [] for s in supported_species}
        config_id_by_species = {s: [] for s in supported_species}
        zeta_config = []

        for i, sample in enumerate(batch):
            zeta = sample["zeta"]
            species = sample["configuration"].species
            zeta.requires_grad_(True)
            zeta_config.append(zeta)

            for s, z in zip(species, zeta):
                # TODO move check to somewhere else to speed up computation
                if s not in supported_species:
                    raise CalculatorTorchError(f"No model for species: {s}")
                else:
                    zeta_by_species[s].append(z)
                    config_id_by_species[s].append(i)

        # evaluate model to compute energy
        energy_config = [None for _ in range(len(batch))]
        for s, zeta in zeta_by_species.items():

            # have no species "s" in this batch of data
            if not zeta:  # zeta == []
                continue

            z_tensor = torch.stack(zeta)  # convert a list of tensor to tensor
            energy = self.models[s](z_tensor)

            for e_atom, i in zip(energy, config_id_by_species[s]):
                if energy_config[i] is None:
                    energy_config[i] = e_atom
                else:
                    # note cannot use +=, energy e_atom is a view
                    energy_config[i] = energy_config[i] + e_atom

        # forces and stress
        if not self.use_forces:
            forces_config = None
        else:
            forces_config = []
        if not self.use_stress:
            stress_config = None
        else:
            stress_config = []
        if grad:
            for i, sample in enumerate(batch):

                # derivative of energy w.r.t. zeta
                energy = energy_config[i]
                zeta = zeta_config[i]
                dedz = torch.autograd.grad(energy, zeta, create_graph=True)[0]
                zeta.requires_grad_(False)  # no need of grad any more

                if self.use_forces:
                    dzetadr_forces = sample["dzetadr_forces"]
                    f = self.compute_forces(dedz, dzetadr_forces)
                    forces_config.append(f)

                if self.use_stress:
                    dzetadr_stress = sample["dzetadr_stress"]
                    volume = sample["dzetadr_volume"]
                    s = self.compute_stress(dedz, dzetadr_stress, volume)
                    stress_config.append(s)

        self.results["energy"] = energy_config
        self.results["forces"] = forces_config
        self.results["stress"] = stress_config
        return {
            "energy": energy_config,
            "forces": forces_config,
            "stress": stress_config,
        }


class CalculatorTorchDDPCPU(CalculatorTorch):
    def __init__(self, model, rank, world_size):
        super(CalculatorTorchDDPCPU, self).__init__(model)
        self.set_up(rank, world_size)

    def set_up(self, rank, world_size):
        os.environ["MASTER_ADDR"] = "localhost"
        os.environ["MASTER_PORT"] = "12355"
        dist.init_process_group("gloo", rank=rank, world_size=world_size)

    def clean_up(self):
        dist.destroy_process_group()

    def compute(self, batch):
        grad = self.use_forces

        # collate batch input to NN
        zeta_config = self._collate(batch, "zeta")
        if grad:
            for zeta in zeta_config:
                zeta.requires_grad_(True)
        zeta_stacked = torch.cat(zeta_config, dim=0)

        # evaluate model
        model = DistributedDataParallel(self.model)
        energy_atom = model(zeta_stacked)

        # energy
        natoms_config = [len(zeta) for zeta in zeta_config]
        energy_config = [e.sum() for e in torch.split(energy_atom, natoms_config)]

        # forces
        if grad:
            dzetadr_config = self._collate(batch, "dzetadr")
            forces_config = self.compute_forces_config(
                energy_config, zeta_config, dzetadr_config
            )
            for zeta in zeta_config:
                zeta.requires_grad_(False)
        else:
            forces_config = None

        return {"energy": energy_config, "forces": forces_config}

    def __del__(self):
        self.clean_up()


class CalculatorTorchError(Exception):
    def __init__(self, msg):
        super(CalculatorTorchError, self).__init__(msg)
        self.msg = msg

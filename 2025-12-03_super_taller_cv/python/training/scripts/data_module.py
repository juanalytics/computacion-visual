"""
Utilidades para cargar datasets (CIFAR10 por defecto).
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Subset
from torchvision import datasets, transforms


def build_transforms(input_size: int = 32):
    return transforms.Compose(
        [
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.247, 0.243, 0.261)),
        ]
    )


def get_cifar10(data_dir: Path, train: bool, download: bool = True):
    tfm = build_transforms(32)
    return datasets.CIFAR10(root=str(data_dir), train=train, download=download, transform=tfm)


def build_loaders(
    data_dir: Path,
    batch_size: int,
    num_workers: int = 4,
    train_fraction: float | None = None,
    val_fraction: float | None = None,
    seed: int = 42,
) -> Tuple[DataLoader, DataLoader]:
    train_dataset = get_cifar10(data_dir, train=True)
    test_dataset = get_cifar10(data_dir, train=False, download=True)

    if train_fraction and 0 < train_fraction < 1.0:
        generator = torch.Generator().manual_seed(seed)
        indices = torch.randperm(len(train_dataset), generator=generator)[: int(len(train_dataset) * train_fraction)]
        train_dataset = Subset(train_dataset, indices)
    if val_fraction and 0 < val_fraction < 1.0:
        generator = torch.Generator().manual_seed(seed + 1)
        indices = torch.randperm(len(test_dataset), generator=generator)[: int(len(test_dataset) * val_fraction)]
        test_dataset = Subset(test_dataset, indices)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )
    return train_loader, test_loader


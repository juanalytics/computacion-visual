"""
Entrena una CNN básica en CIFAR10 y guarda métricas/paresos.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import yaml
from torch.utils.data import DataLoader
from tqdm import tqdm

from python.training.scripts.data_module import build_loaders
from python.training.scripts.models import SimpleCNN


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_config(path: Path) -> Dict:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def accuracy(logits, targets):
    preds = torch.argmax(logits, dim=1)
    correct = (preds == targets).sum().item()
    return correct / len(targets)


def train_one_epoch(
    model,
    loader: DataLoader,
    criterion,
    optimizer,
    epoch: int,
    device: torch.device,
    log_interval: int,
):
    model.train()
    running_loss = 0.0
    running_acc = 0.0
    for batch_idx, (inputs, targets) in enumerate(loader):
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        running_acc += accuracy(outputs, targets)

        if (batch_idx + 1) % log_interval == 0:
            print(
                f"[train] Epoch {epoch} Step {batch_idx+1}/{len(loader)} "
                f"Loss {running_loss / (batch_idx+1):.4f} "
                f"Acc {running_acc / (batch_idx+1):.4f}"
            )
    return running_loss / len(loader), running_acc / len(loader)


@torch.no_grad()
def evaluate(model, loader: DataLoader, criterion, device: torch.device):
    model.eval()
    total_loss = 0.0
    total_acc = 0.0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        total_loss += loss.item()
        total_acc += accuracy(outputs, targets)
    total_loss /= len(loader)
    total_acc /= len(loader)
    return total_loss, total_acc


def save_metrics(output_dir: Path, metrics: Dict[str, float]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"[train] Métricas guardadas en {metrics_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Entrena CNN scratch en CIFAR10.")
    parser.add_argument("--config", type=Path, default=Path("python/training/configs/cnn_scratch.yaml"))
    parser.add_argument("--epochs", type=int, help="Sobrescribe número de epochs")
    parser.add_argument("--device", type=str, help="cpu o cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)

    seed = cfg.get("seed", 42)
    set_seed(seed)

    device = torch.device(args.device or cfg.get("device", "cpu"))
    if device.type == "cuda" and not torch.cuda.is_available():
        print("[train] CUDA no disponible, usando CPU.")
        device = torch.device("cpu")

    data_dir = Path(cfg.get("data_dir", "data/processed/cifar10"))
    batch_size = cfg.get("batch_size", 128)
    num_workers = cfg.get("num_workers", 4)
    epochs = args.epochs or cfg.get("epochs", 1)
    lr = cfg.get("learning_rate", 1e-3)
    wd = cfg.get("weight_decay", 5e-4)
    log_interval = cfg.get("log_interval", 50)
    output_dir = Path(cfg.get("output_dir", "results/training/cnn_scratch"))

    train_fraction = cfg.get("train_fraction")
    val_fraction = cfg.get("val_fraction")
    train_loader, test_loader = build_loaders(
        data_dir,
        batch_size,
        num_workers,
        train_fraction=train_fraction,
        val_fraction=val_fraction,
        seed=seed,
    )

    model = SimpleCNN(num_classes=10).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)

    best_acc = 0.0
    history = []

    for epoch in range(1, epochs + 1):
        print(f"[train] Epoch {epoch}/{epochs}")
        train_loss, train_acc = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            epoch,
            device,
            log_interval,
        )
        val_loss, val_acc = evaluate(model, test_loader, criterion, device)

        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "val_loss": val_loss,
                "val_acc": val_acc,
            }
        )

        print(
            f"[val] Epoch {epoch} Loss {val_loss:.4f} Acc {val_acc:.4f} "
            f"(train acc {train_acc:.4f})"
        )

        if val_acc > best_acc:
            best_acc = val_acc
            output_dir.mkdir(parents=True, exist_ok=True)
            ckpt_path = output_dir / "model_best.pt"
            torch.save(model.state_dict(), ckpt_path)
            print(f"[train] Nuevo mejor modelo guardado en {ckpt_path}")

    metrics = {
        "config": str(args.config),
        "epochs": epochs,
        "best_val_acc": best_acc,
        "history": history,
    }
    save_metrics(output_dir, metrics)


if __name__ == "__main__":
    main()


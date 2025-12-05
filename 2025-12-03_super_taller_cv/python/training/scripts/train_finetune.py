"""
Fine-tuning de ResNet18 preentrenada en CIFAR10.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import yaml
from torch.utils.data import DataLoader
from tqdm import tqdm
from torchvision import models, transforms

from python.training.scripts.data_module import build_loaders


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


def freeze_backbone(model: nn.Module, until_layer: str | None) -> None:
    if not until_layer:
        return

    freeze = True
    for name, param in model.named_parameters():
        if until_layer in name:
            freeze = False
        param.requires_grad = not freeze


def build_model(num_classes: int, freeze_until: str | None):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    freeze_backbone(model, freeze_until)
    return model


def get_train_transforms():
    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(0.1, 0.1, 0.1, 0.05),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def get_val_transforms():
    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def replace_transforms(loader: DataLoader, tfm) -> None:
    if hasattr(loader.dataset, "dataset"):
        dataset = loader.dataset.dataset
    else:
        dataset = loader.dataset
    if hasattr(dataset, "transform"):
        dataset.transform = tfm


def train_one_epoch(model, loader, criterion, optimizer, device, epoch, log_interval):
    model.train()
    running_loss = 0.0
    running_acc = 0.0
    for batch_idx, (inputs, targets) in enumerate(tqdm(loader, desc=f"train {epoch}", leave=False)):
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
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    total_acc = 0.0
    for inputs, targets in tqdm(loader, desc="val", leave=False):
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        total_loss += loss.item()
        total_acc += accuracy(outputs, targets)
    return total_loss / len(loader), total_acc / len(loader)


def save_metrics(output_dir: Path, metrics: Dict[str, object]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"[finetune] Métricas guardadas en {metrics_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tuning ResNet18 para CIFAR10.")
    parser.add_argument("--config", type=Path, default=Path("python/training/configs/resnet_finetune.yaml"))
    parser.add_argument("--epochs", type=int, help="Sobrescribe epochs.")
    parser.add_argument("--device", type=str, help="cpu o cuda.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)

    set_seed(cfg.get("seed", 123))
    device = torch.device(args.device or cfg.get("device", "cpu"))
    if device.type == "cuda" and not torch.cuda.is_available():
        print("[finetune] CUDA no disponible, usando CPU.")
        device = torch.device("cpu")

    data_dir = Path(cfg.get("data_dir", "data/processed/cifar10"))
    batch_size = cfg.get("batch_size", 64)
    num_workers = cfg.get("num_workers", 4)
    epochs = args.epochs or cfg.get("epochs", 1)
    lr = cfg.get("learning_rate", 5e-4)
    wd = cfg.get("weight_decay", 1e-4)
    log_interval = cfg.get("log_interval", 50)
    output_dir = Path(cfg.get("output_dir", "results/training/resnet18_finetune"))

    train_loader, val_loader = build_loaders(
        data_dir,
        batch_size,
        num_workers,
        train_fraction=cfg.get("train_fraction"),
        val_fraction=cfg.get("val_fraction"),
        seed=cfg.get("seed", 123),
    )

    replace_transforms(train_loader, get_train_transforms())
    replace_transforms(val_loader, get_val_transforms())

    model = build_model(num_classes=10, freeze_until=cfg.get("freeze_backbone_until"))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=lr, weight_decay=wd)

    best_acc = 0.0
    history = []

    for epoch in range(1, epochs + 1):
        print(f"[finetune] Epoch {epoch}/{epochs}")
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device, epoch, log_interval)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)

        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "val_loss": val_loss,
                "val_acc": val_acc,
            }
        )

        print(f"[finetune] Val Epoch {epoch} Loss {val_loss:.4f} Acc {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            output_dir.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), output_dir / "model_best.pt")
            print("[finetune] Guardado nuevo mejor modelo.")

    metrics = {
        "config": str(args.config),
        "epochs": epochs,
        "best_val_acc": best_acc,
        "history": history,
    }
    save_metrics(output_dir, metrics)


if __name__ == "__main__":
    main()



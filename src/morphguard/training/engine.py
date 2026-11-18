from __future__ import annotations
from pathlib import Path
import torch

def train_epoch(model, loader, optimizer, criterion, device="cpu"):
    model.train(); total=correct=loss_sum=0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad(set_to_none=True); logits=model(images); loss=criterion(logits,labels); loss.backward(); optimizer.step()
        loss_sum += float(loss.item())*len(labels); correct += int((logits.argmax(1)==labels).sum()); total += len(labels)
    return {"loss": loss_sum/max(total,1), "accuracy": correct/max(total,1)}

def save_checkpoint(path: Path, model, optimizer=None, epoch=0, history=None, config=None):
    path.parent.mkdir(parents=True,exist_ok=True); torch.save({"epoch":epoch,"model":model.state_dict(),"optimizer":optimizer.state_dict() if optimizer else None,"history":history or [],"config":config or {}},path)

def load_checkpoint(path: Path, model, optimizer=None, device="cpu"):
    state=torch.load(path,map_location=device,weights_only=False); model.load_state_dict(state["model"])
    if optimizer is not None and state.get("optimizer"): optimizer.load_state_dict(state["optimizer"])
    return state

from __future__ import annotations
def create_model(name: str, pretrained=False):
    try:
        import torch.nn as nn
        from torchvision import models
    except ImportError as exc: raise RuntimeError("Install torch and torchvision to use deep models") from exc
    if name == "custom_cnn":
        return nn.Sequential(nn.Conv2d(3,32,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),nn.Conv2d(32,64,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Dropout(.25),nn.Linear(64,2))
    if name == "resnet18":
        model=models.resnet18(weights=models.ResNet18_Weights.DEFAULT if pretrained else None); model.fc=nn.Linear(model.fc.in_features,2); return model
    if name == "efficientnet_b0":
        model=models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT if pretrained else None); model.classifier[-1]=nn.Linear(model.classifier[-1].in_features,2); return model
    raise ValueError(f"Unknown model: {name}")

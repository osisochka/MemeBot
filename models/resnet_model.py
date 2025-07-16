from models.base_model import BaseModel
from torch import nn
from torchvision import models

class ResNet(BaseModel):
    def __init__(self, pretrained=True):
        super().__init__()
        self.model = models.resnet50(
            weights=models.ResNet50_Weights.IMAGENET1K_V1 if pretrained else None
        )
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 1)

    def forward(self, x):
        return self.model(x)
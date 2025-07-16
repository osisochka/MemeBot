from torch import nn
from torchvision import models

from models.base_model import BaseModel


class EffModel(BaseModel):
    def __init__(self, pretrained=True):
        super().__init__()
        self.model = models.efficientnet_b0(
            weights=models.EfficientNet_B2_Weights.IMAGENET1K_V1 if pretrained else None
        )
        num_features = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(num_features, 1)

    def forward(self, x):
        return self.model(x)

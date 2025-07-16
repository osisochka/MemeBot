from models.base_model import BaseModel
from torch import nn
from torchvision import models

class VITModel(BaseModel):
    def __init__(self, pretrained=True):
        super().__init__()
        self.model = models.vit_b_16(
            weights=models.ViT_B_16_Weights.IMAGENET1K_V1 if pretrained else None
        )
        num_features = self.model.heads.head.in_features
        self.model.heads.head = nn.Linear(num_features, 1)

    def forward(self, x):
        return self.model(x)

import os
from abc import ABC, abstractmethod

import torch
import torch.nn as nn


class BaseModel(ABC, nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()

    @abstractmethod
    def forward(self, x):
        pass

    def load(self, path):
        if os.path.exists(path):
            self.load_state_dict(torch.load(path))
            print(f"Model loaded from {path}")
        else:
            raise FileNotFoundError(f"No model found at {path}")

    def get_device(self):
        return next(self.parameters()).device

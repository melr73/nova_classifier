
import torch
import torch.nn as nn
import torch.nn.functional as F

class NovaClassifier(nn.Module):
        def __init__(self):
            super().__init__()
            self.layer_1 = nn.Linear(in_features=2001, out_features=1000)
            self.layer_2 = nn.Linear(in_features=1000, out_features=1)

        def forward(self, x):
            x = F.relu(self.layer_1(x))
            x = self.layer_2(x)
            return x

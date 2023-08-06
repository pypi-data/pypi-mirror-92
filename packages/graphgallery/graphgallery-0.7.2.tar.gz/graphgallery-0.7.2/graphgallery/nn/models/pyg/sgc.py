import torch
import torch.nn.functional as F
from torch import optim
from torch.nn import Module, ModuleList, Dropout

from graphgallery.nn.models import TorchKeras
from graphgallery.nn.layers.pytorch.get_activation import get_activation
from graphgallery.nn.metrics.pytorch import Accuracy

from torch_geometric.nn import SGConv


class SGC(TorchKeras):
    def __init__(self,
                 in_channels,
                 out_channels,
                 hids=[],
                 acts=[],
                 K=2,
                 dropout=0.5,
                 weight_decay=5e-5,
                 lr=0.2,
                 use_bias=False):
        super().__init__()

        if hids or acts:
            raise RuntimeError(
                f"Arguments 'hids' and 'acts' are not supported to use in SGC (PyG backend)."
            )

        conv = SGConv(in_channels,
                      out_channels,
                      bias=use_bias,
                      K=K,
                      cached=True,
                      add_self_loops=True)
        self.conv = conv
        self.dropout = Dropout(dropout)
        self.compile(loss=torch.nn.CrossEntropyLoss(),
                     optimizer=optim.Adam(conv.parameters(),
                                          lr=lr,
                                          weight_decay=weight_decay),
                     metrics=[Accuracy()])

    def forward(self, x, edge_index, edge_weight=None):
        x = self.conv(x, edge_index, edge_weight)
        return x

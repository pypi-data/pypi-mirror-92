from tensorflow.keras import Input
from tensorflow.keras.layers import Dropout, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from graphgallery.nn.layers.tensorflow import GraphEdgeConvolution, Gather
from graphgallery.nn.models import TFKeras
from graphgallery import floatx, intx


class EdgeGCN(TFKeras):

    def __init__(self, in_channels, out_channels,
                 hids=[16], acts=['relu'], dropout=0.5,
                 weight_decay=5e-4, lr=0.01, use_bias=False):

        _intx = intx()
        _floatx = floatx()
        x = Input(batch_shape=[None, in_channels],
                  dtype=_floatx, name='node_attr')
        edge_index = Input(batch_shape=[None, 2], dtype=_intx,
                           name='edge_index')
        edge_weight = Input(batch_shape=[None], dtype=_floatx,
                            name='edge_weight')

        h = x
        for hid, act in zip(hids, acts):
            h = GraphEdgeConvolution(hid, use_bias=use_bias,
                                     activation=act,
                                     kernel_regularizer=regularizers.l2(weight_decay))([h, edge_index, edge_weight])

            h = Dropout(rate=dropout)(h)

        h = GraphEdgeConvolution(out_channels, use_bias=use_bias)(
            [h, edge_index, edge_weight])

        super().__init__(inputs=[x, edge_index, edge_weight], outputs=h)
        self.compile(loss=SparseCategoricalCrossentropy(from_logits=True),
                     optimizer=Adam(lr=lr), metrics=['accuracy'])

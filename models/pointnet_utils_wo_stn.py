import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data
import torch.nn.functional as F


def define_layer(in_c, out_c, apply_bn=True, apply_relu=True):
    seq = [torch.nn.Conv1d(in_c, out_c, 1)]
    if apply_bn:
        seq.append(nn.BatchNorm1d(out_c))
    if apply_relu:
        seq.append(nn.ReLU())
    return nn.Sequential(*seq)


def define_mlp(in_c, out_c, *hidden_c, apply_bn=True, apply_relu=True):
    layers = []
    prev_c = in_c

    for c in hidden_c:
        layers.append(define_layer(prev_c, c, apply_bn=True, apply_relu=True))
        prev_c = c

    layers.append(define_layer(prev_c, out_c, apply_bn=apply_bn, apply_relu=apply_relu))

    return nn.Sequential(*layers)

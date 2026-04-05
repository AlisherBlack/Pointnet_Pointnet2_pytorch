import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data
import torch.nn.functional as F
from pointnet_utils_wo_stn import define_mlp


class get_model(nn.Module):
    def __init__(self, num_class, channel=9):
        super(get_model, self).__init__()
        self.k = num_class

        self.mlp1 = define_mlp(channel, 64, 64)
        self.mlp2 = define_mlp(64, 1024, 128, apply_relu=False)
        self.mlp3 = define_mlp(1088, 128, 512, 256)
        self.mlp4 = define_mlp(128, self.k, apply_bn=False, apply_relu=False)

    def forward(self, x):
        # x: (B, C, N)
        B, C, N = x.size()

        # ----- Encoder -----
        # X1: (B, 64, N)
        x1 = self.mlp1(x)

        # X2: (B, 1024, N)
        x2 = self.mlp2(x1)

        # h: (B, 1024, 1)
        h = torch.max(x2, 2, keepdim=True)[0]

        # H: (B, 1024, N)
        H = h.repeat(1, 1, N)

        # X3: concat → (B, 1088, N)
        x3 = torch.cat([x1, H], dim=1)

        # ----- Decoder -----
        # X4: (B, 128, N)
        x4 = self.mlp3(x3)

        # Y logits: (B, k, N)
        x = self.mlp4(x4)

        # reshape to (B, N, k)
        x = x.transpose(2, 1).contiguous()
        x = F.log_softmax(x.view(-1, self.k), dim=-1)
        x = x.view(B, N, self.k)

        return x, None


class get_loss(torch.nn.Module):
    def __init__(self, mat_diff_loss_scale=0.001):
        super(get_loss, self).__init__()
        self.mat_diff_loss_scale = mat_diff_loss_scale

    def forward(self, pred, target, trans_feat, weight):
        loss = F.nll_loss(pred, target, weight=weight)
        total_loss = loss
        return total_loss


if __name__ == "__main__":
    model = get_model(13)
    xyz = torch.rand(12, 3, 2048)
    (model(xyz))

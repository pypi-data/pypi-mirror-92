import torch, svox
t = svox.N3Tree()

t.randn_()
x = t.data.data.clone()

t._push_to_leaf()

print('err', torch.abs(t.data.data - x).max().item())

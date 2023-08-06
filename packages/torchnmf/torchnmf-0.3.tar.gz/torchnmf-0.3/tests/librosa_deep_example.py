import torch
from torch.nn import Module, Conv1d
import librosa
from functools import reduce
from operator import mul

from torchnmf import NMF, NMFD, BetaMu
from torchnmf.metrics import Beta_divergence


class DrumsNet(Module):
    def __init__(self, Vshape, T):
        super().__init__()

        self.components = torch.nn.ModuleList(
            [
                NMF(W=(Vshape[0], 10), rank=10),
                NMFD(W=(10, 3), T=10, rank=4),
                NMF((3, Vshape[1]), rank=1)
            ]
        )

        self.sparse = NMF(Vshape, rank=5)
        self.dense = NMF(Vshape, rank=5)

        self.bias = NMFD(Vshape, T=T, rank=10)

    def forward(self):
        return self.sparse() + self.dense()

if __name__ == '__main__':
    y, sr = librosa.load(librosa.util.example_audio_file())
    y = torch.from_numpy(y)
    windowsize = 2048
    S = torch.stft(y, windowsize, window=torch.hann_window(windowsize)).pow(2).sum(2).sqrt()
    #S = feature.melspectrogram(y, sr, n_fft=windowsize, power=2) ** 0.5
    S[S == 0] = 1e-8
    S = torch.FloatTensor(S).cuda()
    R = 3
    T = 400
    F = S.shape[0] - 1

    #net = NMFD(S.shape, T=T, rank=R).cuda()
    net = DrumsNet(S.shape, T).cuda()
    #trainer = BetaTrainer(net, beta=0., alpha=1e-2)
    optim = BetaMu([{'params': net.sparse.parameters(), 'sparsity': 0.3, 'beta': 1, 'l1_reg': 0.01},
                    {'params': net.dense.parameters(), 'sparsity': 0.9}], beta=0)

    print(net)

    def closure():
        return S, net()

    for i in range(100):
        net.zero_grad()
        optim.step(closure)
        print(i+1, Beta_divergence(net(), S, 0).mul(2).sqrt().item())
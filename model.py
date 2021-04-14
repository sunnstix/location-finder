from torch import nn
import torch 
from torch.nn.utils import rnn

class model(nn.Module):

    def __init__(self, vocab_len, embed_len, hidden_len, output_len, num_layers, dropout, doubleD, init_vectors):
        super().__init__()

        self.embed = nn.Embedding(vocab_len,embed_len)
        self.embed.weight.data.copy_(init_vectors)
        self.lstm = nn.LSTM(embed_len, hidden_len, num_layers = num_layers, bidirectional = doubleD, dropout = dropout)
        self.fc = nn.Linear(hidden_len*2, output_len)

        self.activate = nn.Softmax

    def forward(self,txt,txt_length):
        embedTxt = self.embed(txt)
        packed = rnn.pack_padded_sequence(embedTxt,txt_length,batch_first=True)
        _, (hidden,cell) = self.lstm(packed)
        dense = self.fc(hidden[-1])
        return self.activate(dense)
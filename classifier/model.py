from torch import nn
from torch.nn.utils import rnn

class model(nn.Module):

    def __init__(self, vocab_len, embed_len, hidden_len, output_len, num_layers, dropout, doubleD, init_vectors):
        super().__init__()

        self.embed = nn.Embedding(vocab_len,embed_len,padding_idx=0)
        self.embed.weight.data.copy_(init_vectors)
        
        self.lstm = nn.LSTM(embed_len, hidden_len, num_layers = num_layers, bidirectional = bool(doubleD), dropout = dropout,batch_first = True)
        self.fc = nn.Linear(hidden_len, output_len)

        self.activate = nn.Softmax(dim=1)

    def forward(self,txt,txt_length):
        embedTxt = self.embed(txt)

        packed = rnn.pack_padded_sequence(embedTxt,txt_length,batch_first=True)
    
        _, (hidden,cell) = self.lstm(packed)
        dense = self.fc(hidden[-1])
        out = self.activate(dense)
        return out
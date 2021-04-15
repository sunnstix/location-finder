from model import model
from dataloader import  DEVICE, TOKENIZER, load_vocab
from utils import *
from torch import LongTensor
import torch
from train import extract_pred

VOCAB = load_vocab(config('dumpster.vocab'))

def predict(classifier,txt):
    indices = [VOCAB.stoi[token] for token in TOKENIZER(txt)]
    tensor =LongTensor(indices).to(DEVICE)
    pred = classifier(tensor.unsqueeze(1).T,LongTensor([len(indices)]))
    return extract_pred(pred).item()

if __name__ == '__main__':
    classifier = model(len(VOCAB),config('model.embed_dim'),config('model.hidden_nodes'),config('model.output_nodes'),
                        config('model.num_layers'),config('model.dropout'),config('model.bidirection'),VOCAB.vectors)
    classifier.load_state_dict(torch.load(config('model.param_file')))
    classifier.eval()

    with open('test_input.txt','r') as input:
        for idx,line in enumerate(input.readlines()):
            print("Line {}: {}".format(idx,predict(classifier,line)))

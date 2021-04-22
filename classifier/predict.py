from classifier.model import model
from classifier.dataloader import  DEVICE, TOKENIZER, load_vocab
from utils import *
from torch import LongTensor
import torch
from preprocess.sunnyfileconvert import numberToState

#fetches vocabulary from dataset
VOCAB = load_vocab(config('dumpster.vocab'))

def extract_pred(log):
    return torch.max(log,1)[1]

def predict(classifier,txt):
    #predicts using classifier and input text
    indices = [VOCAB.stoi[token] for token in TOKENIZER(txt)]
    tensor =LongTensor(indices).to(DEVICE)
    pred = classifier(tensor.unsqueeze(1).T,LongTensor([len(indices)]))
    return extract_pred(pred).item()

def predWrapper(classifier,input_file):
    #iterate through input file and generate predictions (wrapped for training)
    with open(input_file,'r') as input:
        for idx,line in enumerate(input.readlines()):
            print("Line {}: {}".format(idx,numberToState[predict(classifier,line)]))

def test(input_file):
    #loads classifier and calls prediction wrapper
    classifier = model(len(VOCAB),config('model.embed_dim'),config('model.hidden_nodes'),config('model.output_nodes'),
                        config('model.num_layers'),config('model.dropout'),config('model.bidirection'),VOCAB.vectors)
    classifier.load_state_dict(torch.load(config('model.param_file')))
    classifier.eval()
    predWrapper(classifier,input_file)



from model import model
from dataloader import load, TXT, LBL, DEVICE
from utils import *
from torch import LongTensor
import spacy
from code import GLOBAL_THING, transform_function

NLP = spacy.load('en')

def predict(classifier,txt):
    indices = [TXT.vocab.stoi[token.text] for token in NLP.tokenizer(txt)]
    tensor =LongTensor(indices).to(DEVICE)
    pred = classifier(tensor.unsqueeze(1).T,LongTensor([len(indices)]))
    return pred.item()

if __name__ == '__main__':
    classifier = model(len(TXT.vocab),config('model.embed_dim'),config('model.hidden_nodes'),config('model.output_nodes'),
                        config('model.num_layers'),config('model.dropout'),config('model.bidirection'),TXT.vocab.vectors)

    with open('test_input.txt','r') as input:
        for idx,line in enumerate(input.readlines()):
            print("Line {}: {}".format(idx,predict(classifier,line)))

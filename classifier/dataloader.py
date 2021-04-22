
import torch
from torchtext.legacy import data
from torchtext.legacy.data.field import Field, LabelField, Pipeline
from preprocess.preprocessing import PreProcess
import random
from utils import *
import torch.optim
import time
import dill
from pathlib import Path
from torchtext.legacy.data import Dataset
import pickle


CSTM_PRPRCSS = False #flag for custom preprocessing
MYSEED = time.time() #seed with time later but using static seed for now

#cuda check
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
TOKENIZER = PreProcess(1).tweet_preprocessor

torch.manual_seed(MYSEED)
torch.backends.cudnn.deterministic = True

def save_vocab(vocab, path):
    #saves vocab pickle object
    with open(path, 'wb') as output:
        pickle.dump(vocab, output)

def load_vocab(path):
    #load vocab pickle object
    with open(path, 'rb') as input:
        return pickle.load(input)

def save_dataset(dataset, path):
    #saves entire dataset
    if not isinstance(path, Path):
        path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    torch.save(dataset.examples, path/"examples.pkl", pickle_module=dill)
    torch.save(dataset.fields, path/"fields.pkl", pickle_module=dill)

def load_dataset(path):
    #loads entire dataset
    if not isinstance(path, Path):
        path = Path(path)
    examples = torch.load(path/"examples.pkl", pickle_module=dill)
    fields = torch.load(path/"fields.pkl", pickle_module=dill)
    return Dataset(examples, fields)

class TwitterData:
    #Dataloader class 
    def __init__(self):
        #define fields
        self.txtField = Field(tokenize=TOKENIZER,batch_first=True,include_lengths=True)
        self.lblField = LabelField(preprocessing = Pipeline(lambda i: int(i.strip())),batch_first = True, dtype = torch.int64)

        #Create and partition data
        myData = data.TabularDataset(path = config('csv_file'), format = 'csv', fields = [('text',self.txtField),('label',self.lblField)], skip_header = True)
        self.trainData,self.validData = myData.split(split_ratio = 0.7, random_state = random.seed(MYSEED))
        save_dataset(self.trainData,config('dumpster.trainData'))
        save_dataset(self.validData,config('dumpster.validData'))

        #utilize glove embeddings
        self.txtField.build_vocab(self.trainData,vectors = 'glove.6B.100d')
        self.lblField.build_vocab(self.trainData)
        save_vocab(self.getVocab(),config('dumpster.vocab'))

    def getVocab(self):
        return self.txtField.vocab

    def load(self):
        return data.BucketIterator.splits((self.trainData, self.validData), batch_size = config('batch_size'), 
                                        sort_key = lambda s: len(s.text), sort_within_batch = True, device = DEVICE)

if __name__ == '__main__':
    #debugging
    TwitterData().load()
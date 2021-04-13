import torch
from torch._C import dtype
from torchtext import data
from preprocessing import PreProcess
import random
from utils import *

import torch.optim

CSTM_PRPRCSS = False #flag for custom preprocessing

MYSEED = 420 #seed with time later but using static seed for now

#cuda check
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

torch.manual_seed(MYSEED)
torch.backends.cudnn.deterministic = True

if not CSTM_PRPRCSS:
    TXT = data.Field(tokenize='spacy',batch_first=True,include_lengths=True)
else:
    TXT = data.Field(preprocessing=PreProcess.preprocessFunction1,batch_first=True,include_lengths=True)
LBL = data.LabelField(dtype = torch.int32,batch_first=True)

def loaderDebug():
    #No. of unique tokens in text
    print("Size of TEXT vocabulary:",len(TXT.vocab))

    #No. of unique tokens in label
    print("Size of LABEL vocabulary:",len(LBL.vocab))

    #Commonly used words
    print(TXT.vocab.freqs.most_common(10))  

    #Word dictionary
    print(TXT.vocab.stoi)


def load(debug):
    #load data in
    jsonFields = {'description':('desc',None),'text':('text',TXT),'location':('label',LBL)}
    myData = data.TabularDataset(path = config('json_file'), format = 'json', fields = jsonFields, skip_header = False)

    #test print
    if debug: print(vars(myData.examples[0]))
    trainData,validData = myData.split(split_ratio = 0.7, random_state = random.seed(MYSEED))

    #utilize glove embeddings
    TXT.build_vocab(trainData,vectors = 'glove.6B.100d', min_freq = 5)
    LBL.build_vocab(trainData)
    if debug: loaderDebug()

    #iterator generator
    return data.BucketIterator.splits((trainData, validData), batch_size = config('batch_size'), 
                                    sort_key = lambda s: len(s.text), sort_within_batch = True, device = DEVICE)

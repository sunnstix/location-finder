import torch
from torchtext.legacy import data
from torchtext.legacy.data.field import Field, LabelField, Pipeline
from preprocessing import PreProcess
import random
from utils import *
import torch.optim


CSTM_PRPRCSS = False #flag for custom preprocessing

MYSEED = 420 #seed with time later but using static seed for now

#cuda check
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
TOKENIZER = PreProcess().tweet_preprocessor

torch.manual_seed(MYSEED)
torch.backends.cudnn.deterministic = True

class TwitterData:
    def __init__(self):
        self.txtField = Field(tokenize=TOKENIZER,batch_first=True,include_lengths=True)
        self.lblField = LabelField(preprocessing = Pipeline(lambda x: int(x)),batch_first = True, dtype = torch.float)
        self.myData = data.TabularDataset(path = config('csv_file'), format = 'csv', fields = [('text',self.txtField),('label',self.lblField)], skip_header = True)


        self.trainData,self.validData = self.myData.split(split_ratio = 0.7, random_state = random.seed(MYSEED))

        #utilize glove embeddings
        self.txtField.build_vocab(self.trainData,vectors = 'glove.6B.100d')
        self.lblField.build_vocab(self.trainData)

    def load(self,debug=False):
        #test print
        if debug: print(vars(self.myData.examples[0]),vars(self.myData.examples[1]))
        if debug: 
            print(vars(self.myData.examples[0]),vars(self.myData.examples[1]))
            print(self.txtField.vocab.vectors)
            print(self.lblField.vocab.vectors)

        #iterator generator
        return data.BucketIterator.splits((self.trainData, self.validData), batch_size = config('batch_size'), 
                                        sort_key = lambda s: len(s.text), sort_within_batch = True, device = DEVICE)

if __name__ == '__main__':
    TwitterData().load(True)
from matplotlib.pyplot import plot
from dataloader import DEVICE, TwitterData
import torch
from model import model
from torch.nn import BCELoss
from utils import *
import numpy as np

MAX_EPOCHS = 100

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def computeCorrect(pred,labels):
    correct = (pred == labels).float()
    return correct.sum().item(), len(labels)

def run_epoch(classifier, input, optimizer, criterion):
    classifier.train() # enter training mode
    for batch in input:
        optimizer.zero_grad() #clear gradience

        text, textSz = batch.text
        pred = classifier(text,textSz) #get prediction
        loss = criterion(pred,batch.label)
        loss.backward()
        optimizer.step()
        

def extract_pred(log):
    return torch.max(log,1)[1]

def eval(classifier, criterion, validLoader, trainLoader, epoch, stats, currPatience = None, prevLoss = None, state_dict= None):
    def computeMetrics(loader):
        correct, total = 0,0
        running_loss = []
        classifier.eval()
        with torch.no_grad():
            for batch in loader:
                text, textSz = batch.text
                out = classifier(text,textSz).squeeze() #get prediction
                pred = extract_pred(out)
                running_loss.append(criterion(out,batch.label).item())
                batchCorrect, batchTotal = computeCorrect(pred,batch.label)
                correct += batchCorrect
                total += batchTotal
        accuracy = correct / total
        loss = np.mean(running_loss)
        return accuracy, loss
    train_acc, train_loss = computeMetrics(trainLoader)
    valid_acc, valid_loss = computeMetrics(validLoader)
    stats.append([train_acc,train_loss, valid_acc, valid_loss])
    logger(epoch,stats)
    if prevLoss is None: return (0, stats[-1][3], None)
    if stats[-1][3] >= prevLoss:
        return (currPatience + 1, prevLoss, state_dict)
    else:
        return (0, stats[-1][3], classifier.state_dict())

def train(classifier, trainLoader, validLoader):
    #cuda optimization of model
    classifier = classifier.to(DEVICE)
    optimizer = torch.optim.Adam(classifier.parameters(),weight_decay=0.02)
    criterion = torch.nn.CrossEntropyLoss().to(DEVICE)
    plotter = TwitterPlotter('Tweet Location Classifier')

    epoch = 0
    stats = []
    patience = config('patience')
    currPatience,prevLoss,state_dict = eval(classifier,criterion,validLoader,trainLoader,epoch,stats)
    plotter.update(epoch,stats)
    while currPatience < patience and epoch < MAX_EPOCHS:
        epoch += 1
        run_epoch(classifier,trainLoader,optimizer,criterion)
        currPatience,prevLoss,state_dict = eval( classifier,criterion, validLoader, trainLoader, epoch, stats, currPatience, prevLoss )
        plotter.update(epoch,stats)

    torch.save(state_dict,config('model.param_file'))
    plotter.save()
    plotter.hold()

    print('Finished training!')

if __name__ == "__main__":
    data = TwitterData()
    trainIter, validIter = data.load()
    classifier = model(len(data.txtField.vocab),config('model.embed_dim'),config('model.hidden_nodes'),config('model.output_nodes'),
                        config('model.num_layers'),config('model.dropout'),config('model.bidirection'),data.txtField.vocab.vectors)

    print(classifier) #inspect model

    print(f'The model has {count_parameters(classifier):,} trainable parameters')

    train(classifier,trainIter,validIter)
    
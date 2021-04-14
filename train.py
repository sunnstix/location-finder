from dataloader import DEVICE, TwitterData
import torch
from model import model
from torch.nn import BCELoss
from utils import *
import numpy as np

MAX_EPOCHS = 420

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def computeCorrect(pred,labels):
    pred = torch.max(pred,1)[1]
    correct = (torch.round(pred) == labels).float()
    return correct.sum(), len(labels)

def run_epoch(classifier, input, optimizer, criterion):
    loss = 0

    classifier.train() # enter training mode
    for batch in input:
        optimizer.zero_grad() #clear gradience

        text, textSz = batch.text
        pred = model(text,textSz).squeeze() #get prediction
        loss += criterion(pred,batch.label).item()
        
        loss.backward() #backpropagation optimization and gradient calculation
        optimizer.step()

def eval(classifier, criterion, validLoader, trainLoader, epoch, stats, currPatience = None, prevLoss = None):
    def computeMetrics(loader):
        correct, total = 0,0
        running_loss = []
        classifier.eval()
        with torch.no_grad():
            for batch in loader:
                text, textSz = batch.text
                pred = classifier(text,textSz).squeeze() #get prediction
                running_loss.append(criterion(pred,batch.label).item())
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
    if prevLoss is None: return (0, stats[-1][3])
    if stats[-1][3] >= prevLoss:
        return (currPatience + 1, prevLoss)
    else:
        torch.save(model.state_dict(),config('param_file'))
        return (0, stats[-1][3])

def train(classifier, trainLoader, validLoader):
    #cuda optimization of model
    classifier = classifier.to(DEVICE)
    optimizer = torch.optim.Adam(classifier.parameters())
    criterion = BCELoss().to(DEVICE)
    plotter = TwitterPlotter('Tweet Location Classifier')

    epoch = 0
    stats = []
    patience = config('patience')
    currPatience,prevLoss = eval(classifier,criterion,validLoader,trainLoader,epoch,stats)
    plotter.update(epoch,stats)

    while currPatience < patience:
        epoch += 1
        run_epoch(classifier,trainLoader,optimizer,criterion)
        currPatience,prevLoss = eval( classifier,criterion, validLoader, trainLoader, epoch, stats, currPatience, prevLoss )
        plotter.update(epoch,stats)
        print('Current Patience:', currPatience)

    print('Finished training!')

if __name__ == "__main__":
    data = TwitterData()
    trainIter, validIter = data.load(True)
    classifier = model(len(data.txtField.vocab),config('model.embed_dim'),config('model.hidden_nodes'),config('model.output_nodes'),
                        config('model.num_layers'),config('model.dropout'),config('model.bidirection'),data.txtField.vocab.vectors)

    print(classifier) #inspect model

    print(f'The model has {count_parameters(classifier):,} trainable parameters')

    train(classifier,trainIter,validIter)
    
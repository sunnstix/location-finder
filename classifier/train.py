from matplotlib.pyplot import plot
from classifier.dataloader import DEVICE, TwitterData
import torch
from classifier.model import model
from utils import *
import numpy as np

MAX_EPOCHS = 50 #Maximum number of epochs for time constraints

def count_parameters(model):
    #common usage of fetching underlying parameter count
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def computeCorrect(pred,labels):
    # evaluate the prediction when compared to the output
    correct = (pred == labels).float()
    return correct.sum().item(), len(correct)

def run_epoch(classifier, input, optimizer, criterion):
    # Code to run a singular epoch for training

    classifier.train() # enter training mode
    for batch in input:
        optimizer.zero_grad() #clear gradience
        text, textSz = batch.text
        pred = classifier(text,textSz) #get prediction
        loss = criterion(pred,batch.label)
        loss.backward() # backpropogation
        optimizer.step()
        

def extract_pred(log): #fetches the prediction from classifier output
    return torch.max(log,1)[1]

def eval(classifier, criterion, validLoader, trainLoader, epoch, stats, currPatience = None, prevLoss = None, state_dict= None):
    def computeMetrics(loader): #evaluates accuracy across multibatched dataset
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
    train_acc, train_loss = computeMetrics(trainLoader) # computes metrics on training data
    valid_acc, valid_loss = computeMetrics(validLoader) # computes metrics on validation data
    stats.append([train_acc,train_loss, valid_acc, valid_loss]) #saves statistics
    logger(epoch,stats) #logs stats
    if prevLoss is None: return (0, stats[-1][3], None)
    if stats[-1][3] >= prevLoss:
        return (currPatience + 1, prevLoss, state_dict) #decreases patience if loss increases
    else:
        return (0, stats[-1][3], classifier.state_dict())

def train(classifier, trainLoader, validLoader):
    #Main training function

    #cuda optimization of model
    classifier = classifier.to(DEVICE)
    optimizer = torch.optim.SGD(classifier.parameters(), lr=4.0)
    criterion = torch.nn.CrossEntropyLoss().to(DEVICE)
    plotter = TwitterPlotter('Tweet Location Classifier')
    
    #epoch initializations
    epoch = 0
    stats = []
    patience = config('patience')
    currPatience,prevLoss,state_dict = eval(classifier,criterion,validLoader,trainLoader,epoch,stats)
    plotter.update(epoch,stats)

    #main training loop
    while currPatience < patience and epoch < MAX_EPOCHS:
        epoch += 1
        run_epoch(classifier,trainLoader,optimizer,criterion)
        currPatience,prevLoss,state_dict = eval( classifier,criterion, validLoader, trainLoader, epoch, stats, currPatience, prevLoss ,state_dict)
        plotter.update(epoch,stats)

    torch.save(state_dict,config('model.param_file')) #save best model to file
    print('Note: Please close the plot to continue...')
    plotter.save()
    plotter.hold()

    print('Finished training!')

def loadAndTrain():
    data = TwitterData()
    trainIter, validIter = data.load()
    classifier = model(len(data.txtField.vocab),config('model.embed_dim'),config('model.hidden_nodes'),config('model.output_nodes'),
                        config('model.num_layers'),config('model.dropout'),config('model.bidirection'),data.txtField.vocab.vectors)

    print(classifier) #inspect model

    print(f'The model has {count_parameters(classifier):,} trainable parameters')

    train(classifier,trainIter,validIter)

if __name__ == "__main__":
    loadAndTrain()
    
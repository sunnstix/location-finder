from classifier.train import loadAndTrain
from classifier.predict import test
from preprocess.sunnyfileconvert import regen

import sys

if __name__ == '__main__':
    #wrapper script to call subimplementations for grader convenience
    if len(sys.argv) < 2:
        print('Need to pass function parameter')
        exit()
    if sys.argv[1] == 'train':
        loadAndTrain()
    elif sys.argv[1] == 'test':
        test('test_input.txt')
    elif sys.argv[1] == 'generate':
        regen()


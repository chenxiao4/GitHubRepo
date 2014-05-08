
import numpy as np
from argparse import *



def argulti():
    parser = ArgumentParser(description = "Discrete Fourier Transformation")

    parser.add_argument("-d",help = "signal array size", 
                        dest = "n", 
                        required = True,
                        type = int)

    return parser.parse_args()

    
def dmat(n):

    k = np.expand_dims(np.arange(n),0)
    wnk = np.exp(-2j*np.pi*k.T*k/n)
    return wnk




args = argulti()
#print args.in
wnk = dmat(args.n)
#x = np.dot(wnk,args.in)
#print x
print wnk


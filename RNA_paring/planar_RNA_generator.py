from typing import List
from dna_generator import generate_single_chain
import numpy as np


def rna_planar(n, s, random_engine=None):

    connres = [set() for _ in range(n)]
    tmp = 0
    while tmp in range(n):   
        bottom = random_engine.randint(0, s/2)
        up = random_engine.randint(3, s+1)
        tmp = tmp + up + bottom
        if(tmp<=n):
            connres[tmp-up] |= set([tmp])
            connres[tmp+1-up] |= set([tmp - 1])
            if(7>up>4):
                add = random_engine.randint(0, 2)
                if(add == 1):
                    connres[tmp+2-up] |= set([tmp-2])
            if(up>6):
                add = random_engine.randint(0, 3)
                if(add == 1):
                    connres[tmp+2-up] |= set([tmp-2])
                if(add == 2):
                    connres[tmp+2-up] |= set([tmp - 2])
                    connres[tmp+3-up] |= set([tmp - 3])
    tmp = 0
    while tmp in range(n):   
        bottom = random_engine.randint(0, s/2)
        up = random_engine.randint(3, s+1)
        tmp = tmp + up + bottom
        if(tmp<=n):
            connres[tmp-up] |= set([tmp])
            connres[tmp+1-up] |= set([tmp - 1])
            if(up>4):
                connres[tmp+2-up] |= set([tmp-2])
    #conn = [sorted(list(x)) for x in connres]
    #print(connres)
    # for i in range(n):
    #     for j in connres[i]:
    
    return connres

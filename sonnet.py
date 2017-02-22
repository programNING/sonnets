#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:02:29 2017

@author: Sith
"""

import csv
import numpy as np
#import HMM 

def read_data(filename):    
    header = 3
    divs = 17
    all_sonnets = []

    with open(filename,'rb') as f:
        reader = csv.reader(f, delimiter = ' ')    
        n = 0
        
        for row_ in reader:            
            row = row_[:]
            if (n < header):
                n = n + 1
            elif (n < divs):
                while ("" in row):
                    row.remove("")
                all_sonnets.append(row)
                n = n + 1
            if (n == divs - 1):
                n = 0
    return np.array(all_sonnets)
    
def get_rhymes(data):
    pass

def seed_rhymes(rdict):
    pass
    
# Function for passing dataset to HMM.
# Should be as simple as passing all of the words,
# and a parameter for how many hidden states we should allow.
# Can probably model this off of TA code from last assignment.
def train_HMM(X, n_states):
    model = HMM.unsupervised_HMM(X, n_states)
    return model

# Hoo boy this is the One.
# This function needs to
#   1. Call a helper function to get seeded lines.
#   2. Generate each word in each line in the sonnet from the last word.
#   3. CHECK to see if the generated word is kosher.
#       a. Check if the word ends on the proper stres/unstress.
#       b. Check that the word does not bring the syllable count to over 10.

def generate_and_test(hmm):
    return 0    

# Main Loop
if __name__ == '__main__':
    shakespeare = read_data("project2data/shakespeare.txt")
    spenser = read_data("project2data/spenser.txt")
    print spenser
"""
    HMM_model = train_HMM(spenser, 2)

    rhyme_dict = get_rhymes(spenser)
    seeded_sonnet = seed_rhymes(rhyme_dict)

    print generate_and_test(HMM_model, seeded_sonnet)
"""
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:02:29 2017

@author: Sith, Sandra

@notes: 
    - took out the first line of sonnet 99 (made it one line too long)
    - took out the entirety of sonnet 126 (was 12 lines total)
"""

import random
import csv
import numpy as np
#import HMM 

def read_data(filename):    
    header = 3
    divs = 18
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

def reverse_data(sonnets):
    reverse = []
    for row in sonnets:
        copy = row[:]
        copy.reverse()
        reverse.append(copy)
    return reverse

# Stores Rhymes in dictionary  
def get_rhymes(data):
    result = {}
    num_sonnets = len(data) / 14
    for i in xrange(0, len(data), 14):
        # Jump between each sonnet and collect the rhymes.
        sonnet = data[i : i + 14]
        print 'sonnet ', i, ' is ', sonnet

        # We hardcode the rhyming pairs of the sonnet because sonnets
        # have a rigid form anyways, so let's take advantage of it.
        rhyming_pairs = []
        rhyming_pairs.append([sonnet[0], sonnet[2]])
        rhyming_pairs.append([sonnet[1], sonnet[3]])
        rhyming_pairs.append([sonnet[4], sonnet[6]])
        rhyming_pairs.append([sonnet[5], sonnet[7]])
        rhyming_pairs.append([sonnet[8], sonnet[10]])
        rhyming_pairs.append([sonnet[9], sonnet[11]])
        rhyming_pairs.append([sonnet[12], sonnet[13]])

        # Each sonnet has 14 lines in the form: abab cdcd efef gg
        for line1, line2 in rhyming_pairs:
            word1 = line1[len(line1) - 1]
            word2 = line2[len(line2) - 1]
            # We will only have one entry of a word in a dict.
            if result.get(word1) == None and result.get(word2) == None:
                result[word1] = [word2]
                result[word2] = [word1]
            elif result.get(word1) == None:
                result[word2].append(word1)
                result[word1] = [word2]
            else:
                if result.get(word2) == None:
                    result[word1].append(word2)
                    result[word2] = [word1]
    return result

def seed_rhymes(rdict):
    result = [[]] * 14
    # 0 (2), 11 (13)
    first_words = random.choice(rdict.keys(), 7)
    rhyme_pairs = []
    for word1 in first_words:
        word2 = random.choice(rdict[word1])
        rhyme_pairs.append((word1, word2))

    # TODO:: finish this function

    
# Function for passing dataset to HMM.
# Should be as simple as passing all of the words,
# and a parameter for how many hidden states we should allow.
# Can probably model this off of TA code from last assignment.
def train_HMM(X, n_states = 10):
    model = HMM.unsupervised_HMM(X, n_states)
    return model

# Hoo boy this is the One.
# This function needs to
#   1. Call a helper function to get seeded lines.
#   2. Generate each word in each line in the sonnet from the last word.
#   3. CHECK to see if the generated word is kosher.
#       a. Check if the word ends on the proper stres/unstress.
#       b. Check that the word does not bring the syllable count to over 10.
# NOT DONE YET
def generate_and_test(hmm):
    emission = ""
    index = np.random.choice(a = HMM.L, p = HMM.A[index])
    
    while (syllable(emission, new_word) > 10):    
        observe = np.random.choice(a = HMM.D, p = HMM.O[index])

    return emission

# Main Loop
if __name__ == '__main__':
    shakespeare = read_data("project2data/shakespeare.txt")
    reverse = reverse_data(shakespeare)
    print reverse
    #spenser = read_data("project2data/spenser.txt")
    #print spenser
    #rhymedic = get_rhymes(shakespeare)
"""
    HMM_model = train_HMM(spenser)

    rhyme_dict = get_rhymes(spenser)
    seeded_sonnet = seed_rhymes(rhyme_dict)

    print generate_and_test(HMM_model, seeded_sonnet)
"""
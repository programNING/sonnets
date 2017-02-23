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
import sys
sys.path.append('./baum_welch')
import HMM 

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

def numerize_data(sonnets):
    counter = 0
    numerized = []
    word_map = {}

    for row in sonnets:
        number_row = []
        for word in row:
            # Store in map if this is a new word
            if (word not in word_map):
                word_map[word] = counter
                counter = counter + 1
            # Append the number in row    
            number_row.append(word_map[word])

        numerized.append(number_row)        
    return (word_map, numerized)

# Returns a word based on the number from word map
def number_to_word(dictionary, number):
    return dictionary.keys()[dictionary.values().index(number)]

# Stores Rhymes in dictionary  
def get_rhymes(data):
    result = {}
    num_sonnets = len(data) / 14
    for i in xrange(0, len(data), 14):
        # Jump between each sonnet and collect the rhymes.
        sonnet = data[i : i + 14]

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

    idx = 0
    while idx < 12:
        word1 = random.choice(rdict.keys())
        if idx % 2 == 0 and idx != 0:
            idx = idx + 2
        if idx != 12:
            result[idx] = [word1]

            result[idx + 2] = [random.choice(rdict[word1])]
            idx += 1
        else:
            result[idx] = [word1]
            result[idx + 1] = [random.choice(rdict[word1])]

    return result

    # TODO:: finish this function
    # 0 -> 2
    # 1 -> 3
    # 4 -> 6 (2 mod 2 = 0 -> 2 * i = new i)
    # 5 -> 7
    # 8 -> 10 (4 mod 2 = 0 -> 2 * i = new i)
    # 9 -> 11
    # 12 -> 13

    
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

# ====== HELPER FUNCTIONS FOR GENERATE/TEST ====== #
def convert_obs_to_word(num):
    pass

def get_syllables(word):
    pass

def get_end_stress(word):
    pass

def get_begin_stress(word):
    pass

# ====== GENERATE / TEST ====== #
def generate_and_test(hmm):
    emission = ""
    line_str = ''
    for line in sonnet:
        # Once we're done with a line / start a new line,
        # add the previous line to the sonnet, properly reversed
        # and formatted with spaces + newlines.
        emission += line_str
        line_str = ''

        # Need to convert the "word" in the sonnet (a number)
        starting_word = convert_obs_to_word(line[0], obsmap)
        line_str = starting_word + '\n'

        # We assume each line is seeded with ONE word.
        num_syllables = get_syllables(line[0])
        while num_syllables < 10:
            # Generate a new word!
            # To do this, first find the state of the previous word
            last_word = line[-1]

            # Generate a random probability.
            rand_prob = random.uniform(0, 1)
            prev_state = 0
            while rand_prob > 0:
                rand_prob -= ourHMM.O[prev_state][last_word]
                prev_state += 1
            prev_state -= 1

            # Given the previous state, find the state of the next word.
            rand_prob = random.uniform(0, 1)
            next_state = 0
            while rand_prob > 0:
                rand_prob -= ourHMM.A[prev_state][next_state]
                next_state += 1
            next_state -= 1

            # Find the next observation based on the next state.
            rand_prob = random.uniform(0, 1)
            next_obs = 0
            while rand_prob > 0:
                rand_prob -= ourHMM.O[next_state][next_obs]
                next_obs += 1
            next_obs -= 1

            # Check to see if this observation will push us over
            # our syllable count. If so, we must try again.
            next_word = convert_obs_to_word(next_obs, obsmap)
            next_syllables = get_syllables(next_word)
            if next_syllables + num_syllables <= 10:
                # Check that the stress is correct.
                end_stress = get_end_stress(next_word)
                previous_word = convert_obs_to_word(last_word, obsmap)
                begin_stress = get_begin_stress(previous_stress)
                if end_stress + begin_stress == 1:
                    # If both the stress is good and it doesn't put us
                    # above our syllable count, then add it to the line!
                    line.append(next_obs)
                    line_str = next_word + ' ' + line_str
                    num_syllables += next_syllables

    return emission

# Main Loop
if __name__ == '__main__':
    shakespeare = read_data("project2data/shakespeare.txt")
    reverse = reverse_data(shakespeare)
    #print reverse
    #spenser = read_data("project2data/spenser.txt")
    #print spenser
    #rhymedic = get_rhymes(shakespeare)
    #print seed_rhymes(rhymedic)
    (word_map, numerized) = numerize_data(reverse)
    print numerized
    
"""
    HMM_model = train_HMM(spenser)

    rhyme_dict = get_rhymes(spenser)
    seeded_sonnet = seed_rhymes(rhyme_dict)

    print generate_and_test(HMM_model, seeded_sonnet)
"""
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
from nltk.corpus import cmudict

CMUdict = cmudict.dict()
THRESHOLD = 0.0001
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

# =========== NLTK HELPER FUNCTIONS ========== #
def convert_obs_to_word(dictionary, number):
    # Returns a word based on the number from word map
    return dictionary.keys()[dictionary.values().index(number)]

def convert_word_to_obs(dictionary, word):
    return dictionary[word]

def numerize_sonnet(sonnet, dictionary):
    result = []
    for line in sonnet:
        numline = []
        for word in line:
            numline.append(dictionary[word])
        result.append(numline)
    return result

# Given a word, strip it of any punctuation (except for possessives(?)
# and those weird apostrophes Shakespeare likes to use bet'ween letters.
# Then, check to see if it is in the NLTK CMUdict.
#   If it is, then COUNT the number of syllables and return that.
#   If it isn't, return some default value for number of syllables (say 1?)
def get_syllables(word):
    word = strip_word(word)
    if CMUdict.get(word) != None:
        lst = CMUdict.get(word)[0]
        syl = 0
        for part in lst:
            if (part[-1].isdigit()):
                syl = syl + 1
        return syl
    return None

# Given a word, strip it of any punctuation
# Then, check to see if it is in the NLTK CMUdict.
#     If it is, then use string parsing to check if its LAST syllable
#        is stressed (return 1) or unstressed (return 0)
#     If it is NOT, then I dunno? Return unstressed???
def get_end_stress(word_):
    word = strip_word(word_)
    # Get the first pronounciation
    lst = CMUdict.get(word)[0]
    lst = [i for i in lst if i[-1].isdigit()]
    end_stress = int(lst[-1][-1])
    return end_stress

# Given a word, strip it of any punctuation
# Then, check to see if it is in the NLTK CMUdict.
#     If it is, then use string parsing to check if its FIRST syllable
#        is stressed (return 1) or unstressed (return 0)
#     If it is NOT, then I dunno? Return unstressed???
def get_begin_stress(word_):
    word = strip_word(word_)
    # Get the first pronounciation
    lst = CMUdict.get(word)[0]
    lst = [i for i in lst if i[-1].isdigit()]
    begin_stress = int(lst[0][-1])
    if begin_stress == 2:
        begin_stress -= 1
    return begin_stress

def strip_word(word_):
    to_strip = [':', ',', '.', '?', '!', '(', ')']
    done = False
    word = word_
    while not done:
        if word[0] in to_strip:
            done = False
            word = word[1:]
        elif word[-1] in to_strip:
            done = False
            word = word[:-1]
        else:
            done = True
    return word.lower()

def in_cmudict(wordarr):
    result = False
    for word_ in wordarr:
        word = strip_word(word_)
        if CMUdict.get(word) != None:
            result = True
    return result

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
        if in_cmudict([word1]) and in_cmudict(rdict[word1]):
            if idx % 2 == 0 and idx != 0:
                idx = idx + 2
            if idx != 12:
                result[idx] = [word1]
                word2 = random.choice(rdict[word1])
                #print word1, ' rhymes with ', rdict[word1]
                while not in_cmudict([word2]):
                    word2 = random.choice(rdict[word1])
                result[idx + 2] = [word2]
                idx += 1
            else:
                result[idx] = [word1]
                word2 = random.choice(rdict[word1])
                while not in_cmudict([word2]):
                    word2 = random.choice(rdict[word1])
                result[idx + 1] = [word2]

    return result

    
# Function for passing dataset to HMM.
# Should be as simple as passing all of the words,
# and a parameter for how many hidden states we should allow.
# Can probably model this off of TA code from last assignment.
def train_HMM(X, n_states = 10, n_iter = 10):
    model = HMM.unsupervised_HMM(X, n_states, n_iter)
    return model

# Hoo boy this is the One.
# This function needs to
#   1. Call a helper function to get seeded lines.
#   2. Generate each word in each line in the sonnet from the last word.
#   3. CHECK to see if the generated word is kosher.
#       a. Check if the word ends on the proper stres/unstress.
#       b. Check that the word does not bring the syllable count to over 10.


# ====== GENERATE / TEST ====== #
def generate_and_test(ourHMM, sonnet, obsmap):
    emission = ""
    line_str = ''
    for line in sonnet:
        # Once we're done with a line / start a new line,
        # add the previous line to the sonnet, properly reversed
        # and formatted with spaces + newlines.
        emission += line_str
        line_str = ''
        state_lst = []

        # Need to convert the "word" in the sonnet (a number)
        starting_word = convert_obs_to_word(obsmap, line[0])
        line_str = starting_word + '\n'

        # Need to give the first word a starting state.
        # Generate a random probability.
        arr = np.array(ourHMM.O)[:, line[0]].tolist()
        starting_state = arr.index(max(arr))
        state_lst.append(starting_state)

        # We assume each line is seeded with ONE word.
        #print 'starting_word is: ', starting_word
        #print 'is the starting word in cmudict?: ', CMUdict.get(starting_word)
        num_syllables = get_syllables(starting_word)
        #print 'is num_syllables == None?: ', num_syllables == None
        while num_syllables < 10:
            # Generate a new word!
            # To do this, first get the state of the previous word
            last_word = line[-1]
            prev_state = state_lst[-1]

            # Given the previous state, find the state of the next word.
            rand_prob = random.uniform(0, 1)
            next_state = 0
            while rand_prob > THRESHOLD:
                rand_prob -= ourHMM.A[prev_state][next_state]
                next_state += 1
            next_state -= 1

            # Find the next observation based on the next state.
            rand_prob = random.uniform(0, 1)
            next_obs = 0
            while rand_prob > THRESHOLD:
                rand_prob -= ourHMM.O[next_state][next_obs]
                next_obs += 1
            next_obs -= 1

            # Check to see if this observation will push us over
            # our syllable count. If so, we must try again.
            next_word = convert_obs_to_word(obsmap, next_obs)
            if in_cmudict([next_word]):
                next_syllables = get_syllables(next_word)
                if next_syllables + num_syllables <= 10:
                    # Check that the stress is correct.
                    previous_word = convert_obs_to_word(obsmap, last_word)
                    begin_stress = get_begin_stress(previous_word)
                    end_stress = get_end_stress(next_word)
                    if end_stress + begin_stress == 1:
                        # If both the stress is good and it doesn't put us
                        # above our syllable count, then add it to the line!
                        line.append(next_obs)
                        line_str = next_word + ' ' + line_str
                        num_syllables += next_syllables
    emission += line_str
    return emission

# Visualize highest probability word for each state
def common_word(HMM, word_map):
    i = 0
    for state in HMM.O:
        num_word = state.index(max(state))
        print "State " + str(i)
        word = convert_word_to_obs(word_map, num_word)
        print "Highest Probability word: " + word
        print "Probability: " + str(max(state))
        print "Syllable Count: " + str(get_syllables(word))
        print "Begin Stress: " + str(get_begin_stress(word))
        print "End Stress: " + str(get_end_stress(word))
        print "\n"
        i = i + 1
    return 0

# Visualize average of each state
def average_word(HMM):
    i = 0
    for state in HMM.O:
        j = 0
        div = 0.0
        prob = 0.0
        syl = 0.0
        begin_stress = 0.0
        end_stress = 0.0
        for num_word in state:
            if (num_word > 0.05):
                word = convert_word_to_obs(word_map, j)
                prob = prob + num_word
                syl = syl + get_syllables(word)
                begin_stress = begin_stress + get_begin_stress(word)
                end_stress = end_stress + get_end_stress(word)
                div = div + 1
            j = j + 1

        print "State " + str(i)    
        print "Average Prob: " + str(prob/div)
        print "Average syllables: " + str(syl/div)
        print "Average Begin Stress: " + str(begin_stress/div)
        print "Average End Stress: " + str(end_stress/div)
        i = i + 1

    return 0

# Main Loop
if __name__ == '__main__':
    shakespeare = read_data("project2data/shakespeare.txt")
    spenser = read_data("project2data/spenser.txt")
    data = np.concatenate((shakespeare, spenser), axis = 0)

    reverse = reverse_data(data)
    #print reverse
    #spenser = read_data("project2data/spenser.txt")
    #print spenser
    rhymedic = get_rhymes(data)
    sonnet = seed_rhymes(rhymedic)
    #print len(sonnet)
    '''
    print sonnet
    for i in sonnet:
        print strip_word(i[0])
        print get_begin_stress(i[0])
        print get_end_stress(i[0])
        print get_syllables(i[0])
    '''
    (word_map, numerized) = numerize_data(reverse)
    num_sonnet = numerize_sonnet(sonnet, word_map)
    #print len(sonnet)
    #print num_sonnet
    #print numerized

    HMM_model = train_HMM(numerized, n_states = 20, n_iter = 500)

    print generate_and_test(HMM_model, num_sonnet, word_map)

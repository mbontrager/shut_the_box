#!/usr/bin/python

from __future__ import division
from random import randint
import csv

################################################################################
# Shut the Box! 
#
# Simulates 'rounds' Shut the Box rounds to find the mean score
# and probability of success. Outputs a csv file with 'rounds' rows
# corresponding to the score from one round
#
# Usage: Run from script directory:
# shut_the_box.py
#
# Author: Martin Bontrager
# Email: mbontrager@gmail.com
################################################################################

#Dictionary of probabilities for rolling 1-12 on two die
probs = {1: 0, 2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
         8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36}
rounds = 1000000 # Rounds of Shut the Box to simulate
score_list = [] # List of scores from all rounds

################################################################################

def subset_sum(numbers, target, partial=[], subs = []):
    """ Given a list of input integers and a target integer, return a list of 
    all subsets of input ints that sum up to the target.

    Keyword arguments:
    numbers -- list of input integers
    target -- target int to be summed to
    partial and sub -- lists for recursion
    """
    s = sum(partial)
    
    # check if the partial sum is equals to target
    if s == target:
        subs.append(partial)
    if s >= target:
        return  [] # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, partial + [n], subs)
    return(subs)
        
def roll(box):
    """Roll either 2 or 1 die, and return the sum of both (or one)."""
    if sum(box) >= 6:
        die_1 = randint(1, 6)
        die_2 = randint(1, 6)
        die_sum = (die_1 + die_2)
    else:
        die_sum = randint(1, 6)
    return(die_sum)
    

def shut_the_box():
    """Main Shut the Box function. Returns a Score from one round of play."""
    box = range(1, 13)
    o = True

    while o:
        if len(box) == 0:
            return(0)
            o = False
            break
        
        dsum = roll(box)
        #print("\nYou rolled a %s" % dsum)
        sub = subset_sum(box, dsum, subs=[])
        
        if len(sub) > 0:
            probRolls = list()
            for i in sub:
                product = 1
                for k in i:
                    product *= probs[k]
                probRolls.append(product)
            #print("You closed %s" % sub[probRolls.index(max(probRolls))])
            if max(probRolls) > 0:
                idx = probRolls.index(max(probRolls))
            else:
                idx = sub.index(max(sub))
            box = [x for x in box if x not in sub[idx]]
        else:
            return(sum(box))
            o = False
            break

################################################################################
                
for i in range(0, rounds):
    score_list.append(shut_the_box())

c = csv.writer(open("box_scores.csv", 'wb'))
for score in score_list:
    c.writerow([score])


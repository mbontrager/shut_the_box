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

probs = {1: 0, 2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
         8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36}
iters = 100000
score_list = []
                                                     
def subset_sum(numbers, target, partial=[], subs = []):
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
    if (x in range(7, 13) for x in box):
        die_1 = randint(1, 6)
        die_2 = randint(1, 6)
        die_sum = (die_1 + die_2)
    else:
        die_sum = randint(1, 6)
    return(die_sum)
    

def shut_the_box():
    box = range(1, 13)
    box_open = True

    while box_open:
        dsum =roll(box)
#        print("\nYou rolled a %s" % dsum)
        sub = subset_sum(box, dsum, subs=[])

        if len(sub) > 0:
            probRolls = list()
            for i in sub:
                product = 1
                for k in i:
                    product *= probs[k]
                probRolls.append(product)
#            print("You closed %s" % sub[probRolls.index(max(probRolls))])
            box = [x for x in box if x not in sub[probRolls.index(max(probRolls))]]
        else:
            box_open = False
            return(sum(box))
                
for i in range(0, iters):
    score_list.append(shut_the_box())

c = csv.writer(open("box_scores.csv", 'wb'))
for score in score_list:
    c.writerow([score])


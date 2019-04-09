#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:11:43 2019

@author: ahmed
"""

def graph(curr, prev):
    x = np.linspace(0, 2, 100)
    for i in range(1):
        plt.plot(curr, prev, label='linear')
    plt.xlabel('density')
    plt.ylabel('flow')
    plt.title("Nasch")
    plt.legend()
    
    plt.show()
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from math import *
from random import uniform, shuffle

def nasch(cells,num_iters,density,vmax,probability):
      
    cars_num = int(density * cells)
    initial = [0] * cars_num + [-1] * (cells - cars_num)
    shuffle(initial)
    iterations = [initial]
    for i in range(num_iters):
        prev = iterations[-1]
        curr = [-1] * cells
        
        for x in range(cells):
            if prev[x] > -1:
                vi = prev[x]
                distance = 1
                while prev[(x + distance) % cells] < 0:
                    distance += 1
                vtemp = min(vi+1, distance - 1, vmax) # increse speed up to max speed, but don't move further than next car
                if uniform(0,1) < probability:
                    velocity = max(0,vtemp-1)
                else:
                    velocity = vtemp
                curr[(x + velocity) % cells] = velocity # perform the move
        iterations.append(curr)

    
    a = np.zeros(shape=(num_iters,cells))
    for i in range(cells):
        for j in range(num_iters):
            if iterations[j][i] > -1:
                a[j,i] = 1
            else:
                a[j,i] = 0
                
    return curr,prev

cells = int(input("enter the number of cells"))
num_iters = int(input("enter the number of iterations"))
density = float(input("enter the density"))
vmax = int(input("enter the maximum velocity"))
probability = float(input("enter the probability to hit the brake"))
type(density)
type(cells)  
curr,prev = nasch(cells,num_iters,density,vmax,probability)
graph(curr,prev)


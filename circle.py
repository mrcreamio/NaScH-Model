#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:32:37 2019

@author: ahmed
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from math import *
from random import uniform, shuffle
def draw(iterations):
    circle = np.linspace(0,2*np.pi,1000)
    x = np.sin(circle)
    y = np.cos(circle)
    plt.plot(x,y,color='black')
    plt.axis('equal')
    for t in range(num_iters):    
        plt.scatter(iterations[t],iterations[t+1],color='red')    
    plt.show()
    

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
                initial_velocity = prev[x]
                distance = 1
                while prev[(x + distance) % cells] < 0:
                    distance += 1
                    # velocity <--min(v+1,Vmax)
                vtemp = min(initial_velocity+1, distance - 1, vmax)
                if uniform(0,1) < probability:
                    # velocity <--max(0,Velocity -1)
                    velocity = max(0,vtemp-1)
                else:
                    velocity = vtemp
                    #adding values to the current
                curr[(x + velocity) % cells] = velocity
        iterations.append(curr)
    print(iterations)
    
    alpha = np.zeros(shape=(num_iters,cells))
    #print (a)
    for i in range(cells):
        for j in range(num_iters):
            if iterations[j][i] > -1:
                alpha[j,i] = 1
            else:
                alpha[j,i] = 0

                
    return iterations
                 

cells = int(input("enter the number of cells"))
num_iters = int(input("enter the number of iterations"))
density = float(input("enter the density"))
vmax = int(input("enter the maximum velocity"))
probability = float(input("enter the probability to hit the brake"))
type(density)
type(cells)  
iterations = nasch(cells,num_iters,density,vmax,probability)
draw(iterations)




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:35:52 2019

@author: ahmed
"""
from time import clock
def NaSch(v_max=None, L=None, N=None, p=None, Te=None, opOut=None):
    # Setting clock
    t0 = clock()

    # Summary in external text file
    if (nargin == 5):
        opOut = 0
    end

    # Code for missing
    keyNA = -999

    # Separators for output file
    sep = print('----------------------------------------------------')
    sep1 = print('****************************************************')

    # ------------------------------------------------------------
    # Checks
    if (N > L):
        print(('*** Number of vehicles must be lower or equal than the size of the road ***'))
    end

    # Density
    rho = N / L

    # Middle point of the road
    Lc = fix(L / 2)

    # Relaxation time (burning sample)
    Tr = 10 * L
    # Total time
    T = Tr + Te

    # Allocation and initial velocities
    v = zeros(T, 1)
    pos = zeros(1, N)
    XV = keyNA * ones(T, L)#State of the road

    #% ------------------------------------------------------------
    # INITIALIZATION

    # Initial positions
    aux = mslice[1:L]
    for j in mslice[1:N]:
        u = select_uniform(1, length(aux))
        pos(j).lvalue = aux(u)
        aux(u).lvalue = mcat([])
    end

    # Relocating initial positions
    pos = sort(pos)

    # Intial condition for matrix time x (velocity at position)
    for j in mslice[1:N]:
        XV(1, pos(j)).lvalue = 0
    end

    # Initial distances (number of cells between vehicles)
    # To move from gradient d to distance we have to subtract 1
    d = mcat([diff(pos), L - pos(end) + pos(1)])
    d = d - 1

    # Dynamics
    for t in mslice[2:T]:
        # Extract velocities and positions observed at t-1
        vel = XV(t - 1, mslice[:])
        I = find(vel != keyNA)
        vel = vel(I)
        pos = I
        # Determining distances
        d = mcat([diff(pos), L - pos(end) + pos(1)])
        d = d - 1
        # Loop on vehicles
        for j in mslice[1:N]:
            # Acceleration
            v1 = min(vel(j) + 1, v_max)
            # Avoiding crashes
            v2 = min(v1, d(j))
            # Random sudden deceleration
            u = rand
            # Updating velocity
            if (u < p):
                vel(j).lvalue = max(v2 - 1, 0)
            else:
                vel(j).lvalue = v2
            end
            # New position
            pos(j).lvalue = pos(j) + vel(j)
            if (pos(j) > L):
                pos(j).lvalue = pos(j) - L
            end
            # Updating XV matrix
            XV(t, pos(j)).lvalue = vel(j)
        end
        v(t).lvalue = mean(vel)
    end#of temporal loop

    # Burning initial Tr observations
    v(mslice[1:Tr]).lvalue = mcat([])
    XV(mslice[1:Tr], mslice[:]).lvalue = mcat([])

    # Global mean
    v_mean = mean(v)
    flow_mean = v_mean * rho

    # ------------------------------------------------------------
    # Elapsed time
    et = etime(clock, t0)

    # ------------------------------------------------------------
    # Generating output

    switch1 = opOut
    if switch == 1:
        print('\\n ')
        print('NaSch MODEL FOR TRAFFIC SIMULATION \\n')
        print('% s\\n', sep)
        print(' Speed limit: %4d\\n ', v_max)
        print('Length of the (circular) road: %4d\\n ', L)
        print('Number of vehicles: %4d\\n ', N)
        print('Probability of sudden stop: %8.4f\\n ', p)
        print('Effective time: %4d\\n ', Te)
        print('Relaxation time: %4d\\n ', Tr)
        print('Total time: %4d\\n ', T)
        print('%s \\n', sep)
        print(' Density: %8.4f \\n ', rho)
        print('Mean velocity: %8.4f\\n ', v_mean)
        print(sep,' \\n')
        print(' Elapsed time: %8.4f\\n ', et)
        print(sep,' \\n')
        print('\\n ')
    else:
        print('*** opOut must be 0 or 1 ***')

    # ------------------------------------------------------------
    #% Loading structure
    res.L = L
    res.N = N
    res.v_max = v_max
    res.p = p
    res.Te = Te
    res.rho = rho
    res.v = v
    res.v_mean = v_mean
    res.flow_mean = flow_mean
    res.XV = XV

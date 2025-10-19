""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
import functools
from time import perf_counter as pc
import concurrent.futures as future

def approximate_pi(n): # Ex1
    in_c = []
    not_in_c = []
    for i in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if (m.sqrt((m.pow(x,2) + m.pow(y,2))) > 1):
             not_in_c.append((x,y))
        else:
             in_c.append((x,y))
    pi_approx = 4 * len(in_c) / n

    print('Approx of Pi:', pi_approx)


    # | Plot result |
    x_red, y_red = zip(*in_c)
    x_blue, y_blue = zip(*not_in_c)

    plt.figure(figsize=(5, 5))
    plt.scatter(x_blue, y_blue, color='blue', label='Blue points')
    plt.scatter(x_red, y_red, color='red', label='Red points')

    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Approximate Pi')
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box') 

    filename = f'Pi_approx_{n}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close() 


    return pi_approx

def sphere_volume(n, d): #Ex2, approximation
    
    # Create n points of dimension d
    points = [(random.uniform(-1, 1) for ii in range(d)) for jj in range(n)]

    in_sphere = 0
    for point in points:

        distance = m.sqrt(functools.reduce(lambda x,y : x+y, map(lambda x : m.pow(x, 2), point)))
        if (distance <= 1):
            in_sphere += 1
        
    volume = lambda x,y : m.pow(2,d) *  x/y 
    
    return volume(in_sphere, n)

def hypersphere_exact(d): #Ex2, real value
    
    pi_exponetial  = m.pow(m.pi, (d/2))
    denominator  = m.gamma((d/2)+1)

    print('actual volume:', pi_exponetial/denominator)

    return pi_exponetial/denominator

def sphere_volume_sequential():
     
     d = 11
     n = 100000

     start = pc()
     volume_sum = 0
     for i in range(10):
          volume_sum += sphere_volume(n, d)
     end = pc()
     avg = volume_sum/10
     print('Average volume:', avg, 'Computational time:', round(end - start))
    
     

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes

    start = pc()

    with future.ProcessPoolExecutor() as ex:
        futures = [ex.submit(sphere_volume, n, d) for _ in range(np)]
        
        volumes = [f.result() for f in futures]


    end = pc()

    print('Computational time for parallel (loop level):' , round(end - start, 2))

    # Optionally return average or all results
    return sum(volumes) / len(volumes)
    
def partial_volume(p_points):
    inside = 0
    for p in p_points: 
        distance = m.sqrt(sum([x**2 for x in p]))
        if (distance <= 1):
            inside += 1
            
    return inside
            
    

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    partial_points = [[[random.uniform(-1,1) for ii in range(d)] for jj in range(n // np)] for kk in range(np)] # [[(x,y,z,...),(...),(...)], [(...),(...),(...)], [(...),(...),(...)]...]
    
    with future.ProcessPoolExecutor() as ex:
        results = ex.map(partial_volume, partial_points)
        
    inside = sum(results)
    
    volume = lambda x,y : m.pow(2,d) *  x/y 
    
        
    return volume(inside, n)
    
def main():
     
    n = 100000
    d = 11
    np = 2
     
    # sphere_volume_parallel1(n, d, np)



    # #Ex1
    # dots = [1000, 10000, 100000]
    # for n in dots:
    #     approximate_pi(n)
    # #Ex2
    # n = 100000
    # d = 2
    # sphere_volume(n,d)
    # print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    # n = 100000
    # d = 11
    # sphere_volume(n,d)
    # print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    # #Ex3
    # n = 100000
    # d = 11
    # start = pc()
    # for y in range (10):
    #     sphere_volume(n,d)
    # stop = pc()
    # print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    # print("What is parallel time?")

    # #Ex4
    # n = 1000000
    # d = 11
    # start = pc()
    # sphere_volume(n,d)
    # stop = pc()
    # print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    # print("What is parallel time?")

    
    

if __name__ == '__main__':
    main()

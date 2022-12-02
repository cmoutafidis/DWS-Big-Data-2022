# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:03:30 2022

@author: Fik
"""

'''
Links used:
    
    Plots:
        https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html#sphx-glr-gallery-mplot3d-scatter3d-py
    
    Deleting numpy arrays:
        https://stackoverflow.com/questions/35316728/does-setting-numpy-arrays-to-none-free-memory
        
    
    Uniform:
        
        https://sparkbyexamples.com/numpy/how-to-use-numpy-random-uniform-in-python/
        https://chris35wills.github.io/courses/PythonPackages_matplotlib/matplotlib_scatter/
    
    Normal:
        
        https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
    
    Correlated & Anti - correlated:
        
        https://www.digitalocean.com/community/tutorials/python-convert-numpy-array-to-list
        https://www.geeksforgeeks.org/numpy-random-rand-python/
        
        https://stackoverflow.com/questions/619335/a-simple-algorithm-for-generating-positive-semidefinite-matrices
        https://stackoverflow.com/questions/16024677/generate-correlated-data-in-python-3-3
        
        
               
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def plot_2dim_scarrerplot(x,y, a_val=1):
    
    plt.scatter(x, y, alpha=a_val )
    plt.show()
    plt.clf()
    plt.close()



def plot_3dim_scarrerplot(x, y, z, a_val=1):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    ax.scatter(x, y, z, alpha=a_val )
    
    ax.set_xlabel('X Label'); ax.set_ylabel('Y Label'); ax.set_zlabel('Z Label')
    
    plt.show()
    plt.clf()
    plt.close()
    
    
    
def create_d_dimPoints_uniform(numPoints, dimPoints, lowVal=0, highVal=1):
    
    arr = np.random.uniform(low = lowVal, high = highVal, size = (numPoints, dimPoints))
    return arr



def create_d_dimPoints_normal(numPoints, dimPoints, mean=0, std=1, mean_list=[], std_list = []):
    
    arr = np.random.normal(loc = mean, scale = std, size = (numPoints, dimPoints))
    return arr
   
    
 
def create_d_dimPoints_corr_antiCorr(numPoints, dimPoints, flag):
        
    # creating a list with mean values, one for each of the variables (i.e. points' dimensions)
    means_list = [0 for k in range(dimPoints)]
    
    # creating a positively defined matrix to be used as covariance matrix
    A = np.random.rand(dimPoints, dimPoints)
    B = np.dot(A, A.transpose())
    
    cov = B.tolist() # covariance 'matrix' (type -> list)
    # deleting completely A and B numpy arrays:
    A, B = None, None; del A, B
    
    #print(cov)
        
    # if flag == True an anti - correlated distribution is created
    if flag:
        for i in range( 1, len(cov[0]) ):
            cov[0][i] *= -1
            cov[i][0] *= -1
    
    #print();print(cov)
    
    L = np.linalg.cholesky(cov)
    
    uncorrelated = np.random.standard_normal( (dimPoints, numPoints) )
    correlated = np.dot(L, uncorrelated) + np.array(means_list).reshape(dimPoints, 1)
    
    #print(np.corrcoef(correlated))
    #print(type(np.corrcoef(correlated)))
    pd.DataFrame( np.corrcoef(correlated) ).to_csv('corrMatrix_'+str(flag)+'_dimPoints_'+str(dimPoints)+'_numPoints_'+str(numPoints)+'.csv') 
    
    return correlated.transpose()
    
    
    
def check_2dim_3dim(numPoints):
    
    np.random.seed(1)
    
    # 2 dimensions - check
    
    # uniform
    arr = create_d_dimPoints_uniform(numPoints, 2)  
    plot_2dim_scarrerplot(arr[:,0],arr[:,1])
    
    # normal
    arr = create_d_dimPoints_normal(numPoints, 2)
    plot_2dim_scarrerplot(arr[:,0],arr[:,1])
    
    # correlated
    arr = create_d_dimPoints_corr_antiCorr(numPoints, 2, False)
    plot_2dim_scarrerplot(arr[:,0],arr[:,1])
    
    # anti - correlated
    arr = create_d_dimPoints_corr_antiCorr(numPoints, 2, True)
    plot_2dim_scarrerplot(arr[:,0],arr[:,1])


    # 3 dimensions - check
    
    arr = create_d_dimPoints_uniform(numPoints, 3) 
    plot_3dim_scarrerplot(arr[:,0],arr[:,1],arr[:,2]) 
    
    arr = create_d_dimPoints_normal(numPoints, 3) 
    plot_3dim_scarrerplot(arr[:,0],arr[:,1],arr[:,2])
    
    arr = create_d_dimPoints_corr_antiCorr(numPoints, 3, False)
    plot_3dim_scarrerplot(arr[:,0],arr[:,1],arr[:,2])

    arr = create_d_dimPoints_corr_antiCorr(numPoints, 3, True)
    plot_3dim_scarrerplot(arr[:, 0], arr[:, 1], arr[:, 2])
    
    
    
def main():
    
    np.random.seed(1)
    
    #numPoints = 1000
    #check_2dim_3dim(numPoints)
    
    numPoints_list = [1000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
    #numPoints_list = [1000, 10000]
    
    dimPoints = 20
    
    for numPoints in numPoints_list:
        
        arr = create_d_dimPoints_uniform(numPoints, dimPoints)
        pd.DataFrame(arr).to_csv('uni_dimPoints_'+str(dimPoints)+'_numPoints_'+str(numPoints)+'.csv')
    
        arr = create_d_dimPoints_normal(numPoints, dimPoints)
        pd.DataFrame(arr).to_csv('norm_dimPoints_'+str(dimPoints)+'_numPoints_'+str(numPoints)+'.csv')

        arr = create_d_dimPoints_corr_antiCorr(numPoints, dimPoints, False)
        pd.DataFrame(arr).to_csv('corr_dimPoints_'+str(dimPoints)+'_numPoints_'+str(numPoints)+'.csv')
    
        arr = create_d_dimPoints_corr_antiCorr(numPoints, dimPoints, True)
        pd.DataFrame(arr).to_csv('anti_dimPoints_'+str(dimPoints)+'_numPoints_'+str(numPoints)+'.csv')
    


if __name__ == "__main__":
#   https://www.quora.com/When-I-import-my-module-in-python-it-automatically-runs-all-of-the-defined-functions-inside-of-it-How-do-I-prevent-it-from-auto-executing-my-functions-but-still-allow-me-to-call-them-in-my-main-script

    '''
    try:
        main()
    except:
        pass
    
    '''
    main()
    #'''
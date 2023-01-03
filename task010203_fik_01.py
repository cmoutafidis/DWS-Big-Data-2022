# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:59:07 2023

@author: Fik
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 22:38:17 2022

@author: Fik
"""

'''

    Links used:
        
        Task 01:
            
        https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list
        https://stackoverflow.com/questions/3724551/uniqueness-for-list-of-lists

        Task 02:  
            
        https://stackoverflow.com/questions/30346356/how-to-sort-list-of-lists-according-to-length-of-sublists
        https://realpython.com/python-sort/
        
        
'''

import pandas as pd


def readData(csvName):
    
    df = pd.read_csv(csvName) #; print(df.head())
    #print(df.columns)
        
    #'''
    df.drop('Unnamed: 0', axis=1, inplace=True) #; print(df.head())
        
    # Here we sort dataframe points by sum of row.
        
    colToSortByName = "sum"
        
    df[colToSortByName] = df.sum(axis=1) #; print(df.head())
    
    df['index_col'] = df.index #; print(df.head())
        
    # convert dataframe to list of lists
    dataPoints_list = df.values.tolist()
    
    return dataPoints_list



# def for dominance
def i_dominates_j(k, z, d):
    for index in range(d):
        if k[index] <= z[index]:
            continue
        else:
            return False
    return True



def sieve_dataPoints(num_of_dims, dataPoints_list, ascOrder_flag = True):
  
    candToSkyline_list = []
    for i in range(len(dataPoints_list)):
        for j in range(i + 1, len(dataPoints_list)):
           
            if i_dominates_j(   dataPoints_list[i], dataPoints_list[j], num_of_dims ):
                candToSkyline_list.append(dataPoints_list[i])
                                
            if i_dominates_j(   dataPoints_list[j], dataPoints_list[i], num_of_dims ):
                candToSkyline_list.append(dataPoints_list[j])
    
    #skyline_list = list(set(skyline_list))
    candToSkyline_list = [list( el ) for el in set(tuple(el) for el in candToSkyline_list)]
    
    print(len(candToSkyline_list))
    
    return candToSkyline_list
  
    
    
def main():
    
    pd.set_option("display.max.columns", None)    
    
    num_of_dims = 20
    
    #csvName_list = ['uni_dimPoints_20_numPoints_1000.csv','norm_dimPoints_20_numPoints_1000.csv','corr_dimPoints_20_numPoints_1000.csv','anti_dimPoints_20_numPoints_1000.csv']
    
    csvName_list  = ['anti_dimPoints_20_numPoints_1000.csv']
    #csvName_list = ['uni_dimPoints_20_numPoints_1000.csv']
    #csvName_list = ['norm_dimPoints_20_numPoints_1000.csv']
    #csvName_list = ['corr_dimPoints_20_numPoints_1000.csv']
    
    
    #'''
    # Task 01
    for csvName in csvName_list:
        
        dataPoints_list = readData(csvName)

        dataPoints_list.sort(key=lambda x: x[-2]) # ascending order is default !!!!!!!!!!!!!!!!!!
        # they remain sorted #!!!!!!!!!!!!!!!!!!!!!!
        # -1 --> index
        # -2 --> sum
               
        skyline_list = sieve_dataPoints(num_of_dims, dataPoints_list)
        
        while(True):
            
            temp_list = sieve_dataPoints(num_of_dims, skyline_list)
            
            if temp_list:
                skyline_list = temp_list
            else:
                break
        
        print(csvName)
        for el in skyline_list: print(el[-1], '\n')
        print(len(skyline_list), '\n\n')
   
    #'''
    
    #'''      
    # Task 02
        
        dominatedPoints_list = [ 0 for i in range(len(dataPoints_list))]
        #print(len(dominatedPoints_lol))
        
        for i in range(len(dataPoints_list)):
            for j in range(i + 1, len(dataPoints_list)):
                
                if i_dominates_j(   dataPoints_list[i], dataPoints_list[j], num_of_dims ):
                    dominatedPoints_list [i]+= 1
                if i_dominates_j(   dataPoints_list[j], dataPoints_list[i], num_of_dims ):
                    dominatedPoints_list [j]+= 1
                
                
        dominatedPoints_sorted_list = sorted(dominatedPoints_list)

        k = 10
        start = len(dominatedPoints_sorted_list)-1
        end = start - k
        
        for i in range(start, end, -1):
            print(dominatedPoints_sorted_list [i], '\n')
        
    #'''    
    
    #'''   
    # Task 03
    
        topK_skylinePoints_list = []
        for i in range(len(skyline_list)):
            point_idx = int(skyline_list[i][-1]) # type float -> convert to int
            #print(type(point_idx))
            topK_skylinePoints_list.append( [point_idx, dominatedPoints_list[point_idx] ] )
    
        topK_skylinePoints_list.sort(key=lambda x: -x[-1])
    
        if k>len(topK_skylinePoints_list):
            k = len(topK_skylinePoints_list)
    
        for i in range(k):
            print(topK_skylinePoints_list[i])
   

    

if __name__ == "__main__":
    
    '''
    try:
        main()
    except:
        pass
    
    '''
    main()
    #'''
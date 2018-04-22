import re
import os
from os import fsync
import subprocess
import csv

#this method writes the summary to a csv. Will create a csv if needed
def write_summary(vals):
    F = open("outputs/mat_inv-gem5-accel_summary",'r')
    data = F.readlines()

    line_num = 0
    fields = []
    for line in data:
        line_num+=1
        if ':' in line:
            value = line.split(':')
            stat = value[1].split()
            fields.append(stat[0])
            print(stat)

    F.close()

    for val in vals:
        fields.append(val)

    with open(r'summary.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    f.close()   


#Updates the filename given a dictionary of [key to change, value]
def updating(filename,dico):


    F = open(filename,'r')
    W = open('test','w')
    output_file = open
    data = F.readlines()
    keys = dico.keys()
    for line in data:

        key_found=None
        for key in keys:
            if key in line:
                key_found = key
        if key_found:
            newline = key_found+str(dico.get(key_found))
            dico.pop(key_found)
            W.write(newline+'\n')
        else:
            W.write(line)
    os.remove(filename)
    os.rename('test',filename)


def main():

    #looping through the matrixs sizes
    for exp_term in range(4,6):
        mat_size = 2**exp_term
        #mat_size = 32
        
        #looping through cache sizes
        cache_sizes = ['32kB']
        for cache_size in cache_sizes:
            
            #looping through cache associativing
            for cache_assoc in range(4,5):

                #looping through cache line sizes
                for cache_line_size in range(63,64):

                    #looping through tlb page sizes
                    tlb_page_sizes = range(12,13)
                    for tlb_page_size_factor in tlb_page_sizes:
                        tlb_page_size = 2**tlb_page_size_factor

                        #looping through unrolling_factor_num
                        for unrolling_factor_num in range(15,16):

                            #looping through unrolling_factor_sub
                            for unrolling_factor_sub in range(15,16):

                        #unrolling_factor_num = 8
                        #unrolling_factor_sub =8
                                vars = ['unrolling,mat_inv,norm_cols,','unrolling,mat_inv,sub_cols,']
                                new_val = [str(unrolling_factor_num),str(unrolling_factor_sub)]
                                what_to_change = dict(zip(vars,new_val))
                                updating('mat_inv.cfg',what_to_change)
                                
                                vars_gem5 =['cache_line_sz =','cache_assoc =', 'cache_size =', 'tlb_page_size =']
                                new_val_gem5 =[str(cache_line_size), str(cache_assoc), cache_size, str(tlb_page_size)]
                                print('gem5',vars_gem5,  new_val_gem5)
                                what_to_change_gem5 = dict(zip(vars_gem5,new_val_gem5))
                                updating('gem5.cfg',what_to_change_gem5)

                                vars_h = ['#define MAT_SIZE ']
                                new_val_h = [str(mat_size)]
                                change= dict(zip(vars_h,new_val_h))
                                updating('mat_inv.h',change)
                                                        
                                all_values = [unrolling_factor_sub, unrolling_factor_num, cache_line_size, cache_assoc, cache_size,mat_size]

                                os.system("make clean")
                                os.system("make all-local-run")
                                write_summary(all_values)
                                #os.system("python summary.py")
        

        #remake trace
        #os.system("make clean")


if __name__ == "__main__":
    main()

import re
import os
from os import fsync
import subprocess
import csv
from sweepables import *
import itertools

# Implementation for generating param sweeps and config files below, 
# as well as processing results into summary csv.

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
def updating(input_filename,output_filename, dico, sep):
    if input_filename == output_filename:
        raise Exception('Must use different filenames!')
    F = open(input_filename,'r')
    W = open(output_filename,'w')
    data = F.readlines()
    F.close()
    keys = dico.keys()
    for line in data:
        for key in keys:
            if key in line:
                line = key+sep+str(dico[key])+'\n'
                break
        W.write(line)
    W.close()
    print("Wrote ",output_filename,'\n')


# Note: the next three functions rely on path being a RELATIVE path, with 
# this script run in the accelerator's base source folder.
def make_aladdin_cfg(params, loop_labels, path):
    # create config file with given parameters:
    with open(path+ACCEL_NAME+".cfg") as acfg:

        # Misc params:
        acfg.write("pipelining,0\n")
        for k in ['ready_mode', 'cycle_time']:
            acfg.write('{},{}\n'.format(k,params[k]))

        # Cache and spad params:
        for array in params['arrays']:
            array_size = (params['mat_size']**2)*SIZEOF_DATA
            # Currently only supporting all cache or all spad, and
            # assuming that arrays are all the same size.
            if params['memory_type'] == 'cache':
                acfg.write('cache,{},{},{}\n'.format(\
                    array, array_size, \
                    SIZEOF_DATA))

            elif params['memory_type'] == 'spad':
                part_type = params['partition']
                factor = params['factors']
                acfg.write('partition,{},{},{},{}\n'.format(\
                    part_type, array, array_size, SIZEOF_DATA))

        # Unroll parameters:
        for group_label, loop_groups in loop_labels:
            factor = params[group_label]
            for loop in loop_groups:
                acfg.write('unrolling,{},{},{}\n'.format(\
                    ACCEL_NAME, loop, factor))


# Write gem5 config file for specific combination of params
def make_gem5_cfg(params, path):
    updating(GEM5_TEMPLATE, path+'gem5.cfg', params, '=')


def make_run_script(params, path):
    # total hack, but should work.
    with open(path+'run.sh') as run:
        run.write(RUN_TEMPLATE.format(path.rstrip("/"), \
            params['cache_line_sz']))

# Write matrix size to header file
def update_mat_size(mat_size):
    fname = ACCEL_NAME+'.h'
    with open(ACCEL_NAME+'_template.h', 'r') as temp:
        f_out = open(fname, 'w')
        for line in temp:
            if '#define MAT_SIZE' in line:
                line = '#define MAT_SIZE {}\n'.format(mat_size)
            f_out.write(line)
        f_out.close()
        print("Wrote ",fname,'\n')


# Create all combinations of parameter sets
def main():
    labels = ['mat_size','cycle_time', 'memory_type','arrays']
    for k in labels:
        param_sets[k] = param_ranges[k]

    param_sets.update(param_ranges['unrolling'])

    loop_labels = param_ranges['unroll_loop_labels']

    # Get relevant parameters for the selected memory type:
    if param_ranges['memory_type'] == 'spad':
            param_sets.update(param_ranges['spad_params'])
    elif param_ranges['memory_type'] == 'cache':
        param_sets.update(param_ranges['cache_params'])

    # Permutations:
    keys, values = zip(*param_sets.items())
    exp_num = 0
    last_mat_size = None
    experiments = []
    for v in itertools.product(*values):
        experiment = dict(zip(keys, v))
        # run the experiment in its own directory:
        os.mkdir(str(exp_num))

        # Regenerate the trace if mat_size has changed:
        if last_mat_size != experiment['mat_size']:
            # Update header:
            update_mat_size()
            # generate new trace:
            os.system("make clean")
            if experiment['memory_type'] == 'cache':
                os.system("make all-local")
            elif experiment['memory_type'] == 'spad':
                os.system("make all-local-dma")

        exp_path = str(exp_num)+'/'

        # copy latest trace to experiment directory
        os.system("cp dynamic_trace.gz {}".format(exp_path))
        # copy gem5 accel executable to experiment directory
        os.system("cp {}-gem5-accel {}".format(ACCEL_NAME, exp_path))

        # create aladdin cfg in experiment folder:
        make_aladdin_cfg(experiment, loop_labels, exp_path)

        # create gem5 cfg in experiment folder:
        make_gem5_cfg(experiment, exp_path)

        # create run.sh script in experiment folder:
        make_run_script(experiment, exp_path)

        # TODO: preallocate list for memory efficiency
        experiments.append(experiment)
        exp_num += 1

    print("Generated ",exp_num," different accelerators from parameter space.") 
    # Done creating experiments

    # if RUN_EXPERIMENTS:
    #     for i in range(len(experiments)):
    #         os.chdir()

    # Done running experiments


if __name__ == "__main__":
    main()

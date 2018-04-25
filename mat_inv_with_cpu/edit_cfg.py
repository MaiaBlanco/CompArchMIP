import re
import os
from os import fsync
import subprocess
import csv
import sweepables as sw
import cacti_writer as cw
import itertools
import pandas as pd

RUN_EXPERIMENTS=True

# Implementation for generating param sweeps and config files below, 
# as well as processing results into summary csv.


#this method parses aladdin summary to a dict.
def get_summary(experiment_path):
    try:
        F = open(experiment_path+"outputs/{}-gem5-accel_summary".format(sw.ACCEL_NAME),'r')
        data = F.readlines()
        F.close()
        line_num = 0
        fields = {}
        for line in data:
            if ':' in line:
                value = line.split(':')
                stat = value[1].strip().split()
                fields[value[0]] = stat[0].strip()
        return fields
    except:
        print("Cacti params not valid");
        return {}


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
                print("Key: ", key)
                print("Val: ", dico[key])
                line = key+sep+str(dico[key])+'\n'
                break
        W.write(line)
    W.close()
    print("Wrote ",output_filename,'\n')


# Note: the next three functions rely on path being a RELATIVE path, with 
# this script run in the accelerator's base source folder.
def make_aladdin_cfg(params, loop_labels, path):
    # create config file with given parameters:
    fname = path+sw.ACCEL_NAME+".cfg"
    with open(fname, 'w') as acfg:

        # Misc params:
        acfg.write("pipelining,0\n")
        for k in ['cycle_time', 'ready_mode']:
            if k in params:
                acfg.write('{},{}\n'.format(k,params[k]))

        # Cache and spad params:
        for array in params['arrays']:
            # Uppercase means matrix:
            if array.isupper():
                array_size = (params['mat_size']**2)*sw.SIZEOF_DATA_T
            # lowercase means vector:
            else:
                array_size = (params['mat_size'])*sw.SIZEOF_DATA_T
            # Currently only supporting all cache or all spad, and
            # assuming that arrays are all the same size.
            if params['memory_type'] == 'cache':
                acfg.write('cache,{},{},{}\n'.format(\
                    array, array_size, \
                    sw.SIZEOF_DATA_T))

            elif params['memory_type'] == 'spad':
                part_type = params['partition']
                factor = params['factors']
                acfg.write('partition,{},{},{},{},{}\n'.format(\
                    part_type, array, array_size, \
                    sw.SIZEOF_DATA_T, factor))

            else:
                raise Exception("Invalid memory type: ", \
                    params['memory_type'])

        # Unroll parameters:
        for group_label, loop_groups in loop_labels.items():
            factor = params[group_label]
            for loop in loop_groups:
                acfg.write('unrolling,{},{},{}\n'.format(\
                    sw.ACCEL_NAME, loop, factor))

    print("Wrote {}\n".format(fname))


# Write gem5 config file for specific combination of params
def make_gem5_cfg(params, path):
    updating(sw.GEM5_TEMPLATE, path+'gem5.cfg', params, '=')


def make_run_script(params, path):
    # total hack (see sweepables.py), but should work:
    fname = path+'run.sh'
    with open(fname, 'w') as run:
        if 'cache_line_sz' in params:
            run.write(sw.RUN_TEMPLATE.format(path, \
                params['cache_line_sz']))
        else: 
            run.write(sw.RUN_TEMPLATE.format(path, 64))
    os.chmod(fname, 0777)

    print("Wrote ",fname,'\n')


# Write matrix size to header file
def update_mat_size(mat_size):
    fname = sw.ACCEL_NAME+'.h'
    with open('template_'+sw.ACCEL_NAME+'.h', 'r') as temp:
        f_out = open(fname, 'w')
        for line in temp:
            if '#define MAT_SIZE' in line:
                line = '#define MAT_SIZE {}\n'.format(mat_size)
            f_out.write(line)
        f_out.close()

    print("Wrote ",fname,'\n')


# Create all combinations of parameter sets
def main():
    param_sets = {}
    labels = ['mat_size','cycle_time', 'memory_type','arrays']
    for k in labels:
        param_sets[k] = sw.param_ranges[k]

    param_sets.update(sw.param_ranges['unrolling'])

    loop_labels = sw.param_ranges['unroll_loop_labels']

    # Get relevant parameters for the selected memory type:
    if sw.param_ranges['memory_type'][0] == 'spad':
        param_sets.update(sw.param_ranges['spad_params'])
        # make dummy cache params for cacti to use:
        keys, values = zip(*sw.param_ranges['cache_params'].items())
        v = list(itertools.product(*values))[0]
        dummy_cache_vals = dict(zip(keys, v))
    
    elif sw.param_ranges['memory_type'][0] == 'cache':
        param_sets.update(sw.param_ranges['cache_params'])
    
    else:
        raise Exception("Invalid memory type: ", \
            params['memory_type'])

    # Permutations:
    keys, values = zip(*param_sets.items())
    exp_num = 0
    last_mat_size = None
    last_trace_path = None
    experiments = []
    for v in itertools.product(*values):
        experiment = dict(zip(keys, v))
        # run the experiment in its own directory:
        os.mkdir(str(exp_num))

        exp_path = './'+str(exp_num)+'/'
        
        # Regenerate the trace if mat_size has changed:
        if last_mat_size != experiment['mat_size']:
            # Update header:
            update_mat_size(experiment['mat_size'])
            # generate new trace:
            os.system("make clean")
            if experiment['memory_type'] == 'cache':
                os.system("make all-local")
            elif experiment['memory_type'] == 'spad':
                os.system("make all-local-dma")
            last_trace_path = exp_path
            # Copy trace this time, but hardlink in future runs with the same mat size
            # to reduce disk space usage.
            os.system("cp dynamic_trace.gz {}".format(exp_path))
        
        else:
            # link latest trace to experiment directory
            os.link(last_trace_path+"dynamic_trace.gz", exp_path+"dynamic_trace.gz")
        
        
        # copy gem5 accel executable to experiment directory (this is inexpensive
        # in terms of disk space, so no need to create a hard link)
        os.system("cp {}-gem5-accel {}".format(sw.ACCEL_NAME, exp_path))

        # create aladdin cfg in experiment folder:
        make_aladdin_cfg(experiment, loop_labels, exp_path)
        
        # write cacti config files:
        cacti_config_files={
            'cache':exp_path+sw.ACCEL_NAME+"_cacti_cache.cfg",
            'tlb':exp_path+sw.ACCEL_NAME+"_cacti_tlb.cfg",
            'queue':exp_path+sw.ACCEL_NAME+"_cacti_queue.cfg"
        }
        cw.writeAllCactiConfigs(experiment, cacti_config_files)
        if experiment['memory_type'] == 'cache':
            cw.writeAllCactiConfigs(experiment, cacti_config_files)
        elif experiment['memory_type'] == 'spad':
            cw.writeAllCactiConfigs(dummy_cache_vals, cacti_config_files)

        # create gem5 cfg in experiment folder:
        #experiment['cacti_cache_config']=cacti_config_files['cache']
        #experiment['cacti_tlb_config']=cacti_config_files['tlb']
        #experiment['cacti_lq_config']=cacti_config_files['queue']
        #experiment['cacti_sq_config']=cacti_config_files['queue']
        make_gem5_cfg(experiment, exp_path)

        # create run.sh script in experiment folder:
        make_run_script(experiment, exp_path[2:])

        # TODO: preallocate list for memory efficiency
        experiments.append(experiment)
        exp_num += 1
        last_mat_size = experiment['mat_size']
   
    exp_frame = pd.DataFrame(experiments)
    exp_frame.to_csv('param_sweep_results.csv')
    print("Generated ",exp_num," different accelerators from parameter space.") 
    with open('cleanup.sh','w') as clean_file:
        clean_file.write("rm -r {{0..{}}}\n".format(exp_num-1))
    os.chmod('cleanup.sh', 0777)
    # Done creating experiments

    # Run experiments and get summaries into one csv at the end:
    if RUN_EXPERIMENTS:
        # Run each experiment (could be parallelized)
        for i in range(len(experiments)):
            os.chdir(str(i))
            os.system('./run.sh')
            os.chdir("..")
                
        # Done running all experiments; write out the results to csv:
        results = [0]*len(experiments)
        for i in range(len(experiments)):
            exp_path = './'+str(i)+'/'
            res = get_summary(exp_path)
            results[i] = res
            print("Added experiment {} to record.".format(i))
        
        # Create dataframe of results and join with previous dataframe
        # of experiment parameters:
        print("Writing experiment records to csv.")
        results_df = pd.DataFrame(results)
        final_df = pd.merge(exp_frame, results_df, left_index=True, right_index=True)
        # Write out to the csv file:
        final_df.to_csv('param_sweep_results.csv')

        # Done writing results


if __name__ == "__main__":
    main()

# Accel name:
ACCEL_NAME="mat_inv"

#Template cfg files:
GEM5_TEMPLATE="template_"+"gem5.cfg"
RUN_TEMPLATE=\
"""#!/usr/bin/env bash

bmk_exec=mat_inv-gem5-accel
echo Running $bmk_exec

bmk_home=${{ALADDIN_HOME}}/integration-test/with-cpu/mat_inv/{}
gem5_dir=${{ALADDIN_HOME}}/../..

${{gem5_dir}}/build/X86/gem5.opt \
  --debug-flags=HybridDatapath,Aladdin \
  --outdir=${{bmk_home}}/outputs \
  ${{gem5_dir}}/configs/aladdin/aladdin_se.py \
  --l2cache \
  --num-cpus=1 \
  --enable_prefetchers \
  --mem-size=8GB \
  --mem-type=DDR3_1600_8x8  \
  --sys-clock=2GHz \
  --cpu-type=DerivO3CPU \
  --caches \
  --cacheline_size={} \
  --accel_cfg_file=${{bmk_home}}/gem5.cfg \
  -c ${{bmk_home}}/${{bmk_exec}} \
  | gzip -c > stdout.gz
"""


# size in bytes of datatype used by accelerator:
SIZEOF_DATA_T=4

# Sweepable parameters:
############################################
param_ranges = { 
'mat_size' : [64], #[16, 32, 64, 100],
'cycle_time' : [5, 10],

#############################
# Loop unroll parameters:
'unrolling': {
    'unrolling_factor_cols' : [8,16,32],
    'unrolling_factor_row_sub' : [1,8] # linear
},

# This dict is used to link unroll parameters together by associating the key in the
# param_ranges dict (above) to multiple loop labels in the accelerator code.
'unroll_loop_labels' : {
    'unrolling_factor_cols' : ['norm_cols_A', 'norm_cols_I', 'sub_cols_A', 'sub_cols_I'],
    'unrolling_factor_row_sub' : ['sub_rows']
},


'memory_type' : ['spad'], # cache or spad
'arrays' : [['A','I']],
#############################
# Parameters for cache-based accelerator:
# NOTE: latencies and bandwidths are currently defaults in template gem5.cfg
'cache_params': {
    'cache_size' : ['8kB', '16kB', '32kB'], #2, 1.5, 1],   ##explore (UDPDATE TO USE DIVISOR) 
    'cache_bandwidth' : [4, 16],   # number of ports on cache
    'cache_queue_size' : [32],
    'cache_assoc' : [1,16],
    'cache_line_sz' : [64],
    # tlb params for cache based system
    'tlb_page_size' : [4096], # in bytes
    'tlb_entries' : [0],
    'tlb_max_outstanding_walks': [4],
    'tlb_assoc': [0],
    'load_bandwidth' : [1],  # Number of r/w ports on load queue.
    'store_bandwidth' : [1],  # Number of r/w ports on store queue.
    'tlb_bandwidth' :  [1]  # Number of r/w ports on TLB
},

#########################
# parameters for scratchpad/DMA accelerator:
'spad_params' : {
    'ready_mode' : [1],
    # Right now block is (very!) broken, so just use cyclic
    'partition' : ['block','cyclic'],
    'factors' : [16,32],
    'spad_ports' : [4,16],
    'pipelined_dma' : ['True'],
    'dma_chunk_size' : [256]
}
}
# End of sweepable params dictionary
#############################################

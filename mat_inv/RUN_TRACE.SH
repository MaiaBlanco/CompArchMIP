make clean-trace
export WORKLOAD=gje_inv
clang -g -O1 -S -fno-slp-vectorize -fno-vectorize -fno-unroll-loops -fno-inline -emit-llvm -o mat_inv.llvm mat_inv.c
opt -S -load=/workspace/LLVM-Tracer/build/full-trace/full_trace.so -fulltrace mat_inv.llvm -o mat_inv-opt.llvm
llvm-link -o full.llvm mat_inv-opt.llvm /workspace/LLVM-Tracer/build/profile-func/trace_logger.llvm 
llc -filetype=asm -o full.s full.llvm 
gcc -fno-inline -o mat_inv-instrumented full.s -lm -lz
./mat_inv-instrumented 

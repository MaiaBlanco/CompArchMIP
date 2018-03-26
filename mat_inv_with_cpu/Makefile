ACCEL_NAME = mat_inv
SRCS = mat_inv.c
BMARK_SPECIFIC_CFLAGS = -DDMA_INTERFACE_V3
export WORKLOAD=mat_inv

clean: clean-trace clean-gem5

all-local: run-trace gem5

include ../../common/Makefile.tracer
include ../../common/Makefile.gem5

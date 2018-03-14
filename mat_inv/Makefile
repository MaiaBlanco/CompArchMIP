SCS=mat_inv.c

ACCEL_NAME = mat_inv
TEST_BIN = $(ACCEL_NAME)
export TRACE_OUTPUT_DIR=$(ACCEL_NAME)
ifndef WORKLOAD
  export WORKLOAD=gje_inv
endif
include ../common/Makefile.common
include ../common/Makefile.tracer

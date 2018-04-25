ACCEL_NAME = mat_soln
SRCS = mat_soln.c
BMARK_SPECIFIC_CFLAGS = -DDMA_INTERFACE_V3
export WORKLOAD=mat_soln

clean: clean-trace clean-gem5
	rm -f ${ACCEL_NAME}-test
	rm -f labelmap
	rm -rf outputs
	rm -f out.csv
	rm -f *.out
	rm -f stdout.gz

all-local-dma: dma-trace-binary
	./${ACCEL_NAME}-instrumented
	make gem5

all-local: run-trace gem5

all-local-dma-run: all-local-dma
	./run.sh

all-local-run: all-local
	./run.sh

include ../../common/Makefile.tracer
include ../../common/Makefile.gem5


test:
	clang ${SRCS} -o ${ACCEL_NAME}-test -I$(ALADDIN_HOME) -I$(COMMON_DIR) -I$(ALADDIN_HOME)/gem5 


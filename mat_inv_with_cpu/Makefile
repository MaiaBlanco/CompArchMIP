ACCEL_NAME = mat_inv
SRCS = mat_inv.c
BMARK_SPECIFIC_CFLAGS = -DDMA_INTERFACE_V3
export WORKLOAD=mat_inv

clean: clean-trace clean-gem5
	rm ${ACCEL_NAME}-test
	//rm labelmap

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


ACCEL_NAME=mat_soln
GIT_DIR=/workspace/CompArchMIP/${ACCEL_NAME}_with_cpu/
SRC_DIR=/workspace/gem5-aladdin/src/aladdin/integration-test/with-cpu/${ACCEL_NAME}/
CMD=rsync
$CMD ${GIT_DIR}*.py $SRC_DIR
$CMD ${GIT_DIR}*.c $SRC_DIR
$CMD ${GIT_DIR}*.cfg $SRC_DIR
$CMD ${GIT_DIR}*.h $SRC_DIR
$CMD ${GIT_DIR}Makefile $SRC_DIR
$CMD ${GIT_DIR}copy_to_repo.sh $SRC_DIR

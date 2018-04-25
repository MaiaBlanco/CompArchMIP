GIT_DIR=/workspace/CompArchMIP/mat_inv_with_cpu/
CMD=rsync
$CMD *.py $GIT_DIR
$CMD *.c $GIT_DIR
$CMD *.cfg $GIT_DIR
$CMD *.h $GIT_DIR
$CMD Makefile $GIT_DIR
$CMD copy_to_repo.sh $GIT_DIR

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
//#include <time.h>
// For FLT_EPSILON in near-equality checking function:
#include <float.h>
#include "aladdin_sys_connection.h"
#include "aladdin_sys_constants.h"

#ifdef DMA_MODE
#include "gem5/dma_interface.h"
#endif

#define CACHELINE_SIZE 64

#define DATA_T float
#define MAT_SIZE 16

void mat_inv( DATA_T * A, DATA_T * I ); 
bool almost_equal( DATA_T d, DATA_T target);

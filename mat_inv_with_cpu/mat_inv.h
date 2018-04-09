#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <float.h>
#include "aladdin_sys_connection.h"
#include "aladdin_sys_constants.h"

#ifdef DMA_MODE
#include "gem5/dma_interface.h"
#endif

#define CACHELINE_SIZE 64

#define PARTITION 1
#define OFFSET_STRIDE (MAT_SIZE*MAT_SIZE/PARTITION)
#define DATA_T float
#ifndef MAT_SIZE
#define MAT_SIZE 256 
#endif

void mat_inv( DATA_T * a, DATA_T * I ); 
bool almost_equal( DATA_T d, DATA_T target);

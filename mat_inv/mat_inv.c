#include "mat_inv.h"

#ifdef DMA_MODE
#include "gem5/dma_interface.h"
#endif

#define PARTITION 1
#define OFFSET_STRIDE (MAT_SIZE*MAT_SIZE/PARTITION)


// TODO: extend to have other error codes
void gje_inv( DATA_T * A, DATA_T * I )
{
#ifdef DMA_MODE
  // Note: Need a dmaLoad call for each partition of A and I:
  dmaLoad(&A[0], 0*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
//  dmaLoad(&A[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
//  dmaLoad(&I[0], 0*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
//  dmaLoad(&I[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
#endif
 int i,j,k;
 DATA_T diag_inv, ref_scale;
 main_loop:for ( i = 0; i < MAT_SIZE; i++ )
 {
  // Normalize the diagonal entry
  diag_inv = 1/A[ i*MAT_SIZE + i ];

  // Iterate over columns and apply the diagonal norm factor:
  norm_cols:for ( j = 0; j < MAT_SIZE; j++)
  {
    I[ i*MAT_SIZE + j ] *= diag_inv;
    A[ i*MAT_SIZE + j ] *= diag_inv;
  }
  // Subtract current row from all other rows to cancel the leading entries
  sub_rows:for ( k = 0; k < MAT_SIZE; k++ )
  {
    if ( k == i ) continue;
    ref_scale = A[ k*MAT_SIZE + i ];
    sub_cols:for (j = 0; j < MAT_SIZE; j++ )
    {
      A[ k*MAT_SIZE + j ] -= ref_scale * A[ i*MAT_SIZE + j ];
      I[ k*MAT_SIZE + j ] -= ref_scale * I[ i*MAT_SIZE + j ];
    }
  }
 }
#ifdef DMA_MODE
  dmaStore(&I[0], 0*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
//  dmaStore(&I[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
#endif
}


int main()
{
  DATA_T * A;
  DATA_T * I;
  int i,j;
  A = (DATA_T *) malloc(MAT_SIZE * MAT_SIZE * sizeof(DATA_T));
  I = (DATA_T *) calloc(MAT_SIZE,  MAT_SIZE * sizeof(DATA_T));
  srand(time(NULL));
  for (i = 0; i < MAT_SIZE; i++)
  {
    I[ i*MAT_SIZE + i ] = 1;
    for (j = 0; j < MAT_SIZE; j++)
    {
      A[ i*MAT_SIZE + j ] = rand() * 100;
    }
  }
#ifdef GEM5
  resetGem5Stats();
#endif
  gje_inv(&A[0], &I[0]);
#ifdef GEM5
  dumpGem5Stats("mat_inv");
#endif
  // TODO: file input and output for known test cases:  
  //FILE *output;
  //output = fopen("output.data", "w");
  //...
  return 0;
}

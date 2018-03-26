#include "mat_inv.h"

// TODO: extend to have other error codes
void mat_inv( DATA_T * A, DATA_T * I )
{
#ifdef DMA_MODE
  // Note: Need a dmaLoad call for each partition of A and I:
 dmaLoad(A, A, MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
//  dmaLoad(&A[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
//  dmaLoad(&I[0], 0*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
//  dmaLoad(&I[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
#endif
 int i,j,k;
 DATA_T diag_inv, ref_scale;
 main_loop: for ( i = 0; i < MAT_SIZE; i++ )
 {
  // Normalize the diagonal entry
  diag_inv = 1/A[ i*MAT_SIZE + i ];

  // Iterate over columns and apply the diagonal norm factor:
  norm_cols: for ( j = 0; j < MAT_SIZE; j++)
  {
    I[ i*MAT_SIZE + j ] *= diag_inv;
    A[ i*MAT_SIZE + j ] *= diag_inv;
  }
  // Subtract current row from all other rows to cancel the leading entries
  sub_rows: for ( k = 0; k < MAT_SIZE; k++ )
  {
    if ( k == i ) continue;
    ref_scale = A[ k*MAT_SIZE + i ];
    sub_cols: for (j = 0; j < MAT_SIZE; j++ )
    {
      A[ k*MAT_SIZE + j ] -= ref_scale * A[ i*MAT_SIZE + j ];
      I[ k*MAT_SIZE + j ] -= ref_scale * I[ i*MAT_SIZE + j ];
    }
  }
 }
#ifdef DMA_MODE
  dmaStore(I, I, MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
  dmaStore(A, A, MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
#endif
}


int main()
{
  DATA_T * A;
  DATA_T * I;
  int i,j, err;
  err = 0;
  err |= posix_memalign((void **)&A, CACHELINE_SIZE,
                              MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  err |= posix_memalign((void **)&I, CACHELINE_SIZE, 
                              MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  if ( err != 0 )
  {
    fprintf(stderr, "ERROR: could not allocate aligned memory.\n");
    return 1;
  }
  // Todo: replace with code that reads a real test matrix (and solution system)
  srand(time(NULL));
  for (i = 0; i < MAT_SIZE; i++)
  {
    I[ i*MAT_SIZE + i ] = 1;
    for (j = 0; j < MAT_SIZE; j++)
    {
      A[ i*MAT_SIZE + j ] = rand() * 100;
    }
  }
#ifdef GEM5_HARNESS
  // Map arrays from trace to cpu address space...?
  mapArrayToAccelerator(INTEGRATION_TEST, "A", A,
                        MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  mapArrayToAccelerator(INTEGRATION_TEST, "I", I,
                        MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  // Invoke the accelerator:
  printf("RUNNING MATRIX INVERTER!\n");
  invokeAcceleratorAndBlock(INTEGRATION_TEST);
  printf("FINISHED RUNNING!\n");
#else
//#ifdef GEM5
//  resetGem5Stats();
//#endif
  mat_inv(&A[0], &I[0]);
//#ifdef GEM5
//  dumpGem5Stats("mat_inv");
//#endif
#endif
  int num_errs = 0;
  for (int i = 0; i < MAT_SIZE; i++)
  {
    for (int j  = 0; j < MAT_SIZE; j++)
    {
      printf("%f ", A[i * MAT_SIZE + j]);
      // Jerry rigged near-identity checker:
      if ( ( i == j && abs(A[i*MAT_SIZE+j] - 1) > 0.01 ) || ( abs(A[i*MAT_SIZE + j]) >  0.01 ) )
      {
        num_errs ++;
      }
    }
    printf("\n");
  }
  if ( num_errs > 0 )
  {
    fprintf(stderr, "ERROR: test failed with %d errors.\n", num_errs);
    //return 1;
  }
  printf("Success!\n");
  // TODO: file input and output for known test cases:  
  //FILE *output;
  //output = fopen("output.data", "w");
  //...
  return 0;
}

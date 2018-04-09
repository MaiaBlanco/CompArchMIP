#include "mat_soln.h"

// TODO: extend to have other error codes
void mat_soln( DATA_T * A, DATA_T * b, DATA_T * x )
{
 int i,j,k;
 DATA_T diag_inv, ref_scale;
#ifdef DMA_MODE
  // Note: Need a dmaLoad call for each partition of A and I:
    dmaLoad(A, A, MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
//  dmaLoad(&A[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
    
    // Copy the b vector provided by the host to the x (solution)
    // vector on the accelerator, using DMA
    dmaLoad(&(x[0]), &(b[0]), MAT_SIZE*sizeof(DATA_T));
//  dmaLoad(&I[0], 1*OFFSET_STRIDE*sizeof(DATA_T), PAGE_SIZE);
#else
  // If we are not doing DMA, then manually copy given b into x:
  setup_loop: for ( i = 0; i < MAT_SIZE; i ++ )
  { 
    x[ i ] = b[ i ];
  }
#endif
 main_loop: for ( i = 0; i < MAT_SIZE; i++ )
 {
  // Normalize the diagonal entry
  diag_inv = 1/A[ i*MAT_SIZE + i ];

  // Iterate over columns and apply the diagonal norm factor:
  norm_cols: for ( j = 0; j < MAT_SIZE; j++)
  {
    A[ i*MAT_SIZE + j ] *= diag_inv;
  }
  x[ i ] *= diag_inv;
  
  // Subtract current row from all other rows to cancel the leading entries
  sub_rows: for ( k = 0; k < MAT_SIZE; k++ )
  {
    if ( k == i ) continue;
    ref_scale = A[ k*MAT_SIZE + i ];
    sub_cols: for (j = 0; j < MAT_SIZE; j++ )
    {
      A[ k*MAT_SIZE + j ] -= ref_scale * A[ i*MAT_SIZE + j ];
    }
    x[ k ] -= x[ i ] * ref_scale;
  }
 }
#ifdef DMA_MODE
  // Store the result vector from accelerator's solution, x
  // into the host's x memory location.
  dmaStore(&(x[0]), &(x[0]), MAT_SIZE*sizeof(DATA_T));
  //dmaStore(A, A, MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
#endif
}


int main()
{
  DATA_T * A;
  DATA_T * b;
  DATA_T * x;
  int i,j, err;
  err = 0;
  err |= posix_memalign((void **)&A, CACHELINE_SIZE,
                              MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  err |= posix_memalign((void **)&b, CACHELINE_SIZE, 
                              MAT_SIZE * sizeof(DATA_T) );
  err |= posix_memalign((void **)&x, CACHELINE_SIZE, 
                              MAT_SIZE * sizeof(DATA_T) );
  if ( err != 0 )
  {
    fprintf(stderr, "ERROR: could not allocate aligned memory.\n");
    return 1;
  }
  // Todo: replace with code that reads a real test matrix (and solution system)
  srand(time(NULL));
  for (i = 0; i < MAT_SIZE; i++)
  {
    x[ i ] = 0.0;
    b[ i ] = rand()*100;
    for (j = 0; j < MAT_SIZE; j++)
    {
      A[ i*MAT_SIZE + j ] = rand() * 100;
    }
  }
#ifdef GEM5_HARNESS
  // Map arrays from trace to cpu address space...?
  mapArrayToAccelerator(INTEGRATION_TEST, "A", A,
                        MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  mapArrayToAccelerator(INTEGRATION_TEST, "b", b,
                        MAT_SIZE * sizeof(DATA_T) );
  mapArrayToAccelerator(INTEGRATION_TEST, "x", x,
                        MAT_SIZE * sizeof(DATA_T) );
  // Invoke the accelerator:
  printf("RUNNING MATRIX INVERTER!\n");
  invokeAcceleratorAndBlock(INTEGRATION_TEST);
  printf("FINISHED RUNNING!\n");
#else
//#ifdef GEM5
//  resetGem5Stats();
//#endif
  mat_soln(&A[0], &b[0], &x[0]);
//#ifdef GEM5
//  dumpGem5Stats("mat_soln");
//#endif
#endif
  int num_errs = 0;
  num_errs = matvecmul_test(A, x, b);
  if ( num_errs > 0 )
  {
    fprintf(stderr, "ERROR: test failed with %d errors.\n", num_errs);
    return 1;
  }
  printf("Success!\n");
  // TODO: file input and output for known test cases:  
  //FILE *output;
  //output = fopen("output.data", "w");
  //...
  return 0;
}


// Implements near-equality check for DATA_T, which for this project is either
// float or double
// TODO: Check for better/safer ways to compare floats:
// https://bitbashing.io/comparing-floats.html
bool almost_equal(DATA_T d, DATA_T target)
{
  return abs(d - target) < FLT_EPSILON;
}


// Helper function to verify that Ax=b for matrix A,
// vector x, and vecor b. x and b are expected to be row-major.
int matvecmul_test(DATA_T * A, DATA_T * x, DATA_T * b)
{
  int i, j, k, err_count;
  DATA_T test_b[MAT_SIZE] = {0};
  for ( i = 0; i < MAT_SIZE; i++ )
  {
      for ( j = 0; j < MAT_SIZE; j++ )
      {
        test_b[i] += A[ i * MAT_SIZE + j] * x[j];
      }
  }

  err_count = 0;
  for ( i = 0; i < MAT_SIZE; i ++ )
  {
    err_count += (int)(!almost_equal(test_b[i], b[i]));
  }

  return err_count;
}

#include "mat_soln.h"
#define CHECK_VALS 0

void mat_soln( DATA_T * A, DATA_T * b, DATA_T * x )
{
 int i,j,k;
 DATA_T diag_inv, ref_scale;
#ifdef DMA_MODE
    dmaLoad(A, A, MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
    // Copy the b vector provided by the host to the x (solution)
    // vector on the accelerator, using DMA
    dmaLoad(&(x[0]), &(b[0]), MAT_SIZE*sizeof(DATA_T));
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

  A[ i*MAT_SIZE + i ] *= (DATA_T)1;
  // Iterate over columns and apply the diagonal norm factor:
  norm_cols: for ( j = i; j < MAT_SIZE; j++)
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
  DATA_T test_x[MAT_SIZE];
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
  srand(time(NULL));
  for (i = 0; i < MAT_SIZE; i++)
  {
    x[ i ] = 0.0;
    test_x[ i ] = (DATA_T)rand()*10;
    for (j = 0; j < MAT_SIZE; j++)
    {
      A[ i*MAT_SIZE + j ] = (DATA_T)rand() * 1000;
      if (i == j) A[ i*MAT_SIZE + j] += (DATA_T)rand()*10; 
    }
  }
  // Generate b:
  matmul(A, test_x, b);
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
#if CHECK_VALS
int num_errs = 0;
  num_errs = array_test(test_x, x);
  if ( num_errs > 0 )
  {
    fprintf(stderr, "ERROR: test failed with %d errors.\n", num_errs);
    return 1;
  }
  printf("Success!\n");
#endif
  return 0;
}


// Implements near-equality check for DATA_T, which for this project is either
// float or double
// TODO: Check for better/safer ways to compare floats:
// https://bitbashing.io/comparing-floats.html
bool almost_equal(DATA_T d, DATA_T target)
{
#define SMALL_FLOAT 0.0001
  DATA_T max_f;
  if (fabs(d) > fabs(target)) max_f = fabs(d);
  else max_f = fabs(target);
  d /= max_f;
  target /= max_f;
  if ( fabs(d - target) < SMALL_FLOAT)
  {
    return true;
  }
  fprintf(stderr, "%f != %f\n", d, target);
  return false;
}


void matmul(DATA_T * A, DATA_T * x, DATA_T * b)
{
  int i,j;
  for ( i = 0; i < MAT_SIZE; i++ )
  {
    b[i] = (DATA_T)0;
  }
  for ( i = 0; i < MAT_SIZE; i++ )
  {
      for ( j = 0; j < MAT_SIZE; j++ )
      {
        b[i] += A[ i * MAT_SIZE + j] * x[j];
      }
  }
}


// Helper function to verify that Ax=b for matrix A,
// vector x, and vecor b. x and b are expected to be row-major.
int array_test(DATA_T * test_b, DATA_T * b)
{
  int i, err_count;
  err_count = 0;
  for ( i = 0; i < MAT_SIZE; i ++ )
  {
    if (!almost_equal(test_b[i], b[i])) 
    {
      err_count ++;
    }
  }
  return err_count;
}

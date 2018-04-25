#include "mat_inv.h"

// TODO: extend to have other error codes
void mat_inv( DATA_T * A, DATA_T * I )
{
#ifdef DMA_MODE
  // dmaload takes destination address, host source address, and size in bytes
  dmaLoad(&(A[0]), &(A[0]), MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
  dmaLoad(&(I[0]), &(I[0]), MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
#endif
 DATA_T diag_inv, ref_scale;
 main_loop: for ( int i = 0; i < MAT_SIZE; i++ )
 {
  // Normalize the diagonal entry
  diag_inv = 1/A[ i*MAT_SIZE + i ];
  //A[ i*MAT_SIZE + i ] = (DATA_T)1.0;

  // Iterate over columns and apply the diagonal norm factor:
  norm_cols_A: for ( int j = 0; j < MAT_SIZE; j++)
  {
    A[ i*MAT_SIZE + j] *= diag_inv;
  }
  norm_cols_I: for ( int j = 0; j < i; j++)
  {
    I[ i*MAT_SIZE + j ] *= diag_inv;
  }
 
  // Subtract current row from all other rows to cancel the leading entries
  sub_rows: for ( int k = 0; k < MAT_SIZE; k++ )
  {
    if ( k == i ) continue;
    ref_scale = A[ k*MAT_SIZE + i ];
    sub_cols_A: for ( int j = 0; j < MAT_SIZE; j++ )
    {
      A[ k*MAT_SIZE + j ] -= ref_scale * A[ i*MAT_SIZE + j ];
    }
    sub_cols_B: for (int j = 0; j < MAT_SIZE; j++ )
    {
      I[ k*MAT_SIZE + j ] -= ref_scale * I[ i*MAT_SIZE + j ];
    }
  }
 }
#ifdef DMA_MODE
  // dmastore (v3) takes destination host address, source, and size in bytes.
//  dmaStore(&(A[0]), &(A[0]), MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
  // Note for real application only need to return the final inverse.
  dmaStore(&(I[0]), &(I[0]), MAT_SIZE*MAT_SIZE*sizeof(DATA_T));
#endif
}


int main()
{
  DATA_T *A, *I;
  int i,j, err=0;
  fprintf(stdout, "FYI, DATA_T is of size %d bytes.\n", (int)sizeof(DATA_T) );
  err = posix_memalign((void**)&A, CACHELINE_SIZE,
                              MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  
  assert(err == 0 && "Failed to allocate memory for A!");
  err = posix_memalign((void**)&I, CACHELINE_SIZE, 
                              MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );

  assert(err == 0 && "Failed to allocate memory for I!");
  for (i = 0; i < MAT_SIZE; i++)
  {
    for (j = 0; j < MAT_SIZE; j++)
    {
      if (i == j) 
      {
        A[ i*MAT_SIZE + j ] = (DATA_T)(1+rand()) * 100;
      }
      else
      {
        A[ i*MAT_SIZE + j ] = (DATA_T)rand() * 100;
      }
      I[ i*MAT_SIZE + j] = (DATA_T)(i==j);
    }
  }
#ifdef GEM5_HARNESS
  // Map arrays from trace to cpu address space:
  mapArrayToAccelerator(INTEGRATION_TEST, "A", &(A[0]),
                        MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  mapArrayToAccelerator(INTEGRATION_TEST, "I", &(I[0]),
                        MAT_SIZE * MAT_SIZE * sizeof(DATA_T) );
  // Invoke the accelerator:
  printf("RUNNING MATRIX INVERTER!\n");
  invokeAcceleratorAndBlock(INTEGRATION_TEST);
  printf("FINISHED RUNNING!\n");
#else
//#ifdef GEM5
//  resetGem5Stats();
//#endif
  mat_inv(A, I);
//#ifdef GEM5
//  dumpGem5Stats("mat_inv");
#endif
#ifdef TEST
  int num_errs = 0;
  // Check A
  for (int i = 0; i < MAT_SIZE; i++)
  {
    for (int j  = 0; j < MAT_SIZE; j++)
    {
      if (MAT_SIZE <=32) printf("%f ", A[i * MAT_SIZE + j]);
      // near-identity checks:
      if ( i==j && !almost_equal(A[i * MAT_SIZE + j], (DATA_T)1.0) )
      {
        num_errs ++;
      }
      else if ( i != j && !almost_equal(A[i * MAT_SIZE + j], (DATA_T)0.0) )
      {
        num_errs ++;
      }
    }
    if (MAT_SIZE <= 32) printf("\n");
  }
  // Report number of errors:
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
#define SMALL_FLOAT 0.000001
  if ( fabs(d - target) < SMALL_FLOAT)
  {
    return true;
  }
  fprintf(stderr, "%f != %f\n", d, target);
  return false;
}

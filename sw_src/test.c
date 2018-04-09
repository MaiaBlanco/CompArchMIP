#include <stdio.h>
#include <stdlib.h>

#define MAT_SIZE 16

void main()
{ 
  int i,j;
  float * I = malloc( MAT_SIZE * MAT_SIZE * sizeof(float) );
  for ( i = 0; i < MAT_SIZE; i ++ )
  {
    for ( j = 0; j < MAT_SIZE; j ++ )
    {
      I[i * MAT_SIZE + j ] = (float)(i==j);
    }
  }


  for ( i = 0; i < MAT_SIZE; i ++ )
  {
    for ( j = 0; j < MAT_SIZE; j ++ )
    {
      printf("%f ", I[i * MAT_SIZE + j ]);
    }
    printf("\n");
  }
}

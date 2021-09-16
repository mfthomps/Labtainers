/*
 * Source: Daniel Thomasset and Michael Grobe.
 * Introduction to the Message Passing Interface (MPI) Using C.
 * Online Tutorial Document, Academic Computing Services, 
 * The University of Kansas, November 2013. 
 * URL: http://condor.cc.ku.edu/~grobe/docs/intro-MPI-C.shtml
 */

#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) 
{
  int ierr;
  
  ierr = MPI_Init(&argc, &argv);
  printf("Hello world\n"); 
  
  ierr = MPI_Finalize();
  return 0;
}

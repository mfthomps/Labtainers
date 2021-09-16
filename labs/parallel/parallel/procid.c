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
  int ierr, num_procs, my_id;

  ierr = MPI_Init(&argc, &argv);

  /* find out MY process ID, and how many processes were started. */

  ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
  ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

  printf("Hello world! I'm process %i out of %i processes\n", 
         my_id, num_procs);

  ierr = MPI_Finalize();
}

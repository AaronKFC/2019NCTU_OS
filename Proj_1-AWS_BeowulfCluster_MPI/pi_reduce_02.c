#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
#include <time.h>
//#define iteration 10000000

#define seed 123

int main(int argc, char *argv[])
{
    int iter_in=1, chk_input=1;
    int proc_rank, proc_size;
	double start, finish, loc_elapsed, elapsed, piEstimate;

    int iter=1;
    unsigned long long in_circle_cnt_sum = 0;
    unsigned long long in_circle_cnt_t = 0;


    srand(seed);
  
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc_size);
    //////////////////
	/*
    if(proc_rank == 0){
      for (int i = 0; i < argc; i++)
        printf("Parameter[%0d]: %s  size=%0d \n", i , argv[i], argc);
    }
	*/

    //if(proc_rank == 0){
    if(argc !=2){
      chk_input = 0;
    }
    else{
      iter_in = atoi (argv[1]);
      if(iter_in <= 0)
        chk_input = 0;
      else{
        //if(proc_rank == 0)
          //printf(" --> iter_in=%0d \n", iter_in);

        if(proc_size > 1){
          iter = iter_in/proc_size;
          if(proc_rank == 0)
            iter = iter + 1;
        }
        else
          iter = iter_in;
      }

    }
    if(!chk_input){
      if( proc_rank == 0)
        printf("Usage: mpirun -n <total cpu number> ./<program name> <number of tosses>\n");
      MPI_Finalize();
      return 0;
    }





	start = MPI_Wtime();
    ///////////////////////
    ///*
    for(int i = 0 ; i < iter ; i++)
    {
        double x = (double)rand() * 2 / RAND_MAX + (-1);
        double y = (double)rand() * 2 / RAND_MAX + (-1);
        double dis_sqr = x*x + y*y;
        if(dis_sqr <= 1)
            in_circle_cnt_t++;
    }
	//printf("Temp_cnt=%llu from proc_%0d,size=%0d\n", in_circle_cnt_t, proc_rank, proc_size);
	finish = MPI_Wtime();
	loc_elapsed = finish - start;
	MPI_Reduce(&loc_elapsed, &elapsed, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    ///////////////////////
    MPI_Reduce(&in_circle_cnt_t, &in_circle_cnt_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    //if( proc_rank == 0)
      //printf("Total_cnt=%llu from size=%0d\n", in_circle_cnt_sum, proc_size);

    if( proc_rank == 0){
      double pi = ((double)in_circle_cnt_sum / iter_in) * 4;
      printf("pi = %lf,duration = %f \n",pi, elapsed);

    }
    //*/

    MPI_Finalize();
    return 0;
}


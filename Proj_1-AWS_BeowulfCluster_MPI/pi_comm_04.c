#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

//#define iteration 10000000
#define seed 123
int main(int argc, char *argv[])
{
    unsigned long long in_circle_cnt = 0;
    unsigned long long in_circle_cnt_t0 = 0;
    //unsigned long long *in_circle_cnt_t;
    int iter=1, iter2 = 1, proc_rank, proc_size;
	int iter_in = 1, chk_input = 1;
	double start, finish, loc_elapsed, elapsed, piEstimate;
    /*
    if (argc >= 3 && strcmp (argv[2],"on") == 1){
      printf("Usage: mpirun -n <total cpu number> ./<program name> <number of tosses> \n");

    }
    */



    srand(seed);


    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc_size);

    //printf("rank=%0d size=%0d \n", proc_rank, proc_size);

    /*
    if(proc_rank == 0){
      for (int i = 0; i < argc; i++)
        printf("Parameter %0d of %0d: %s  \n", i , argc, argv[i]);
      printf("\n===========\n");
    }
    */

    //in_circle_cnt_t = (unsigned long long*)malloc(sizeof(unsigned long long)*proc_size);
    //iter = iteration;
	/*iter2 = atoi(argv[1]);
    if(proc_size > 1){
      iter = iter2 /proc_size;
      if(proc_rank == 0)
        iter = iter + 1;
    }*/

	if (argc != 2) {
		chk_input = 0;
	}
	else {
		iter_in = atoi(argv[1]);
		if (iter_in <= 0)
			chk_input = 0;
		else {
			//if(proc_rank == 0)
			//printf(" --> iter_in=%0d \n", iter_in);

			if (proc_size > 1) {
				iter = iter_in / proc_size;
				if (proc_rank == 0)
					iter = iter + 1;
			}
			else
				iter = iter_in;
		}

	}
	if (!chk_input) {
		if (proc_rank == 0)
			printf("Usage: mpirun -n <total cpu number> ./<program name> <number of tosses>\n");
		MPI_Finalize();
		return 0;
	}


	start = MPI_Wtime();

    ///////////////////////
    for(int i = 0 ; i < iter ; i++)
    {
        double x = (double)rand() * 2 / RAND_MAX + (-1);
        double y = (double)rand() * 2 / RAND_MAX + (-1);
        double dis_sqr = x*x + y*y;
        if(dis_sqr <= 1)
            in_circle_cnt_t0++;
    }
    

    //in_circle_cnt_t0 = proc_rank+1;
    //printf("-->temp_result = %llu\n", in_circle_cnt_t0);

    in_circle_cnt = in_circle_cnt + in_circle_cnt_t0;

    ///////////////////////

	//MPI_Send(&loc_elapsed, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);


    if(proc_size > 1){
      if (proc_rank != 0){
        MPI_Recv(&in_circle_cnt_t0,  1, MPI_UNSIGNED_LONG_LONG, proc_rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        //printf("Proc %0d Recv %llu from proc %0d, size=%0d \n", proc_rank, in_circle_cnt_t0, proc_rank-1, proc_size);
        in_circle_cnt = in_circle_cnt + in_circle_cnt_t0;
      }

      if (proc_rank != (proc_size-1)){
        in_circle_cnt_t0 = in_circle_cnt;
        MPI_Send(&in_circle_cnt_t0, 1, MPI_UNSIGNED_LONG_LONG,  proc_rank+1, 0, MPI_COMM_WORLD);
        //printf("Send %llu from proc %0d to %0d, size=%0d \n", in_circle_cnt_t0, proc_rank, proc_rank+1, proc_size);
      }

      

    }

    if(proc_rank == (proc_size-1) ){
      //printf("test_result = %llu\n", in_circle_cnt);
      double pi = ((double)in_circle_cnt / iter_in) * 4;

	  finish = MPI_Wtime();
	  loc_elapsed = finish - start;
	  printf("pi = %lf\n", pi);
	  printf("duration = %f \n", loc_elapsed);
    }

    MPI_Finalize();
    return 0;
}

/*
MPI_Send(void* data, int count, MPI_Datatype datatype,
          int destination, int tag, MPI_Comm communicator)

MPI_Recv(void* data, int count, MPI_Datatype datatype,
          int source , int tag, MPI_Comm communicator, MPI_Status* status)

MPI_Send(&ping_pong_count, 1, MPI_INT, partner_rank, 0,
                 MPI_COMM_WORLD);

MPI_Recv(&ping_pong_count, 1, MPI_INT, partner_rank, 0,
         MPI_COMM_WORLD, MPI_STATUS_IGNORE);

*/

/*

    if (proc_rank != 0){
      if(proc_size > 1){

        //MPI_Send(&in_circle_cnt_t[proc_rank], 1, MPI_UNSIGNED_LONG_LONG, 0, proc_rank, MPI_COMM_WORLD);
      }
    }
    else {
      //in_circle_cnt = in_circle_cnt + in_circle_cnt_t;
      //printf("Collect %llu of processor %d of %d \n", in_circle_cnt_t[proc_rank], proc_rank, proc_size);

      for(int j = 1; j < proc_size ; j++){
        //MPI_Recv(in_circle_cnt_t, 10, MPI_UMSIGNED_LONG_LONG, j, j, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        //printf("Recv %llu from processor %d of %d \n", in_circle_cnt_t, j, proc_size);
        //in_circle_cnt = in_circle_cnt + in_circle_cnt_t;
      }

      //double pi = ((double)in_circle_cnt / iteration) * 4;
      //printf("pi = %lf\n",pi);
    }
    */
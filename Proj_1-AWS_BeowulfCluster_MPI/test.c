#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define iteration 10000000
#define seed 123
int main(void)
{
	srand(seed);
	unsigned long long in_circle_cnt = 0;
	for(int i = 0 ; i < iteration ; i++)
	{
		double x = (double)rand() * 2 / RAND_MAX + (-1);
		double y = (double)rand() * 2 / RAND_MAX + (-1);
		double dis_sqr = x*x + y*y;
		if(dis_sqr <= 1)
			in_circle_cnt++;
	}
	double pi = ((double)in_circle_cnt / iteration) * 4;
	printf("pi = %lf\n",pi);
	return 0;
}

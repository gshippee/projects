#ifndef __REMOVERFI_H__
#define __REMOVERFI_H__

#include <stdbool.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <errno.h>
#include <dirent.h>
#include <sys/stat.h>

#ifndef _RAND_NUM_GEN_
//#include "rand_num_generator.h"
#endif /* _RAND_NUM_GEN_ */

#ifndef __CRABDATABUF_H__
//#include "crab_databuf.h"
#endif /* __CRABDATABUF_H__*/

#ifndef __FILTERBANK_H__
#include "filterbank.h"
#endif /* __FILTERBANK_H__ */

#ifndef _ACQ_UDP_INCLUDED_
#include "acq_udp.h"
#endif /* _ACQ_UDP_INCLUDED_ */

#define START_CHANNEL 280			//1800 if spectrum contains 4096 channels, 300 (240) if 1536 channels
#define STOP_CHANNEL 1200			//2730 if spectrum contains 4096 channels, 1230 (1264) if 1536 channes 2270-2730
#define NCHAN 1536			//1536 or 4096

typedef struct{ 
	short int *data;
	double *input;
	short int *output;
	double *avg;
	double *sd;
	double *window;
	double thresh_limit;
	double new_M;
	double current_SD;
	double current_M;
	long num_samples;
	long seed;
	int counter;
	int window_size; 
	int channel_width;
	int start_channel;
	int end_channel;
	bool stats_done; 
	bool replace_data;  
	bool record_stats;
}DataStruct;


float gasdev(long *idum);
float ran1(long *idum);

char *process_filterbank_file(char infile[], int pol, int bad_channel_flag, int narrowband_rfi_flag, 
                             int broadband_rfi_flag, int zero_nonbandpass_flag);
char *process_raw_data_files(char dirname[], int pol, int bad_channel_flag, int narrowband_rfi_flag,
                             int broadband_rfi_flag, int zero_nonbandpass_flag);

DataStruct *create_DataStruct(long num_samples);
void free_DataStruct(DataStruct *dsp);

void remove_rfi(DataStruct *dsp);
void remove_broadband_rfi(DataStruct *dsp);
void remove_narrowband_rfi(DataStruct *dsp);

void init_struct(DataStruct *dsp, int channel_width, int window_size, 
                 int thresh_limit, int replace_data, int record_stats);

void calc_first_window_stats(DataStruct *dsp);
void write_stats(DataStruct *dsp, long long current_sample);

void read_data(DataStruct *dsp, long long data_size, int pol, FILE *fp);
void prepare_input(DataStruct *dsp);
void process_first_window(DataStruct *dsp);
void process_remainder(DataStruct *dsp);
void adjust_data(DataStruct *dsp, long long current_sample, double current_avg, double current_sd);

short int get_data(DataStruct *dsp, long loc);
double get_input(DataStruct *dsp, long loc);
short int get_output(DataStruct *dsp, long loc);
long get_num_samples(DataStruct *dsp);

# endif /* __REMOVERFI_H__ */

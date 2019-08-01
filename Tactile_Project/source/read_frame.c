/*
 * read_frame.c

* called by interrupt on SyncOut, reads 1 frame, prints and returns *
 *  Created on: Jul 25, 2019
 *      Author: ronf
 */
#include <stdio.h>

/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"

/* Freescale includes. */
#include "fsl_debug_console.h"

#include "fsl_port.h"
#include "fsl_gpio.h"
#include "fsl_common.h"
#include "board.h"
#include "pin_mux.h"
#include "clock_config.h"

static int sensor_frame[8][8];
#define MAX_LOG_LENGTH 64
static char log[MAX_LOG_LENGTH + 1];

extern int read_chan(void);
/*prototypes */
void read_frame(void);
void wait_edge(void);
extern void log_add(char *);

void read_frame()
{ int i,j;
	double frame_time;

	LED_RED_ON(); // reading frame

	frame_time = (double)(xTaskGetTickCountFromISR()/10000.0); // with ticks at 100 us, convert to sec

/* row is scanned first */
/* 2/1/94:  input switches on falling edge, so sample on rising edge */
    for (j = 0; j < 8; j++)
      for(i= 0; i < 8; i++)
      {
     	  wait_edge();
    	  sensor_frame[i][j]= read_chan(); 	/* read one element */
      }
	sprintf(log, "Frame at %10.3f sec\n\r", frame_time);
	log_add(log);
    /* now print read array */
	// use buffer to concatenate all values
	// int snprintf ( char * s, size_t n, const char * format, ... );
   // PRINTF("Frame at %10.3f sec\n\r", frame_time);
    for (j = 0; j < 8; j++)
    {     for(i= 0; i < 8; i++)
          {
    		snprintf(log+5*i,MAX_LOG_LENGTH-5*i,"%5d", sensor_frame[i][j]);
 //        	sprintf(log,"%5d", sensor_frame[i][j]);
          }
//    	sprintf(log,"\n\r");
    	snprintf(log+5*8,MAX_LOG_LENGTH-5*8,"\n\r");
 //   	PRINTF("log entry is %s", log);
    	log_add(log);
    }
    LED_RED_OFF();
}

/* poll on ScanClk for rising edge, which is middle of cell */
void wait_edge(void)
{
	while(GPIO_PinRead(GPIOD, (uint32_t) 6) == 1); // wait for low
	while(GPIO_PinRead(GPIOD, (uint32_t) 6) == 0); // wait for rising edge
}


// read PTD6, Scan_CLK
void read_scan_clk(void)
{ 	uint32_t scan_clk;
	scan_clk = GPIO_PinRead(GPIOD, (uint32_t) 6);
	PRINTF("ScanClk=%d", scan_clk);

}

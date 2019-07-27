/*
 * task2.c
 *
 *  Created on: Dec 31, 2017
 *      Author: ronf
 */

/*System includes.*/
#include <stdio.h>
#include <math.h>

/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"

/* Freescale includes. */
#include "fsl_device_registers.h"
#define DEBUG_CONSOLE_TRANSFER_NON_BLOCKING
#include "fsl_debug_console.h"
#include "board.h"
#include "fsl_pit.h"  /* periodic interrupt timer */

#include "pin_mux.h"
#include "clock_config.h"

/* globals */
extern volatile uint32_t systime; //systime updated very 100 us = 4 days ==> NEED OVERFLOW protection
extern float sqrt_array[1000]; // to hold results

/*******************************************************************************
 * Definitions
 ******************************************************************************/

//#define MAX_LOG_LENGTH 20
#define MAX_LOG_LENGTH 64
//sizeof("Task1 Message 1, ticks 655535, z=3.14159  \n\r    ")

/*******************************************************************************
 * Prototypes
 ******************************************************************************/
/* Application API */
void tactile_task(void *pvParameters);
void show_help(void);

extern void analog_test();
extern void read_frame(void);
extern void read_scan_clk(void);

/* Logger API */
extern void log_add(char *log);
extern void log_task(void *pvParameters);


/*!
 * @brief write_task_2 function
 */
void tactile_task(void *pvParameters)
{   TickType_t tick_start, tick_now;
	const TickType_t xDelay10ms = pdMS_TO_TICKS( 10 );
	const TickType_t xDelay700ms = pdMS_TO_TICKS( 700 );
    char log[MAX_LOG_LENGTH + 1];

    char c;
    PRINTF("Capacitive Array Processing Program\n\r");

    show_help();

    c = ' ';
    while(c != 'q')
    {	PRINTF("\n*");
    	c = ' '; // erase previous character
    	while (c == ' ' || c == '\n')
    	{ DbgConsole_TryGetchar(&c);  // read character without blocking
    		vTaskDelayUntil( &tick_start, xDelay10ms );
    		taskYIELD();  // make sure other tasks can run
    	}
    	PUTCHAR(c); // for checking what was input
       	switch (c)
    	{
        	case '?': show_help();
       	    break;

        	case 'a': analog_test();
        	break;

        	case 's': read_frame();
        	break;

        	case 'c': read_scan_clk();
        	        	break;

       	    default: PUTCHAR('?');
       	    break;
       	}
     }
           PRINTF("QUIT\n");

    tick_now = xTaskGetTickCount();
    sprintf(log, "Tactile Task done. tick_now %d\n\r",
        		 (long)tick_now);
    log_add(log); // add message to print queue
    vTaskSuspend(NULL);
}

void show_help()
{
    PRINTF("\n?     show this message\r\n");
    PRINTF("a  read a/d channel 1               s  scan sensor\n\r");
    PRINTF("c  read scan_clk\n\r");
}




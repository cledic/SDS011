#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <errno.h>
#include <math.h>
#include <stdint.h>

/*
        http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/Documentation/i2c/dev-interface
        apt-get install i2c-tools
        apt-get install libi2c-dev
*/

#include "BME280_lib.h"

int main( void)
{
	float temperatura, pressione, umidita;

	BME280_Init( "/dev/i2c-0");

	if ( BME280_Get_AllValues( &pressione, &temperatura, &umidita))
	{
		printf("0.0,0.0,0.0\n");
	}
	
	printf("%.2f,%.2f,%.2f\n", temperatura, pressione/100, umidita);
}


# SDS011 sensor and Terra Board

The SDS011 sensor is an Air Quality Sensor developed by inovafit.
This are the specifications for the SDS011:

  * Output: PM2.5, PM10 
  * Measuring Range: 0.0-999.9μg/m3 
  * Input Voltage:5V 
  * Maximum Current: 100mA 
  * Sleep Current:2mA 
  * Response Time1 second 
  * Serial Data Output Frequency: 1 time/second 
  * Particle Diameter Resolution:≤0.3μm 
  * Relative Error:10% 
  * Temperature Range:-20~50°C 
  * Physical Size: 71mm*70mm*23mm 

The UART communication protocol requires a bit rate of 9600 baud, with 8 data bit, no parity and one stop bit.

I connect a [Terra board, from ACME Systems,](https://acmesystems.it/terra)
 to this sensor to check the air quality of my city. I check also the temperature and the Atmosferic Pressure. 

The script **sds011_v5.py** read every 5 minutes the sensor and save the values on a SQLITE DB. The data is stable when the sensor works after 30 seconds. After the acquisition the sensor is put into sleep again.

The script **sds011_sleep.py** is used at boot time to put the sensor to sleep.

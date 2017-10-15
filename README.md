# rPi-engraver
Raspberry Pi-Controlled Laser Engraver

**_Note:_** *the project is still in beta version.*

## About the project
The project consists of two separate applications: a driver (in Python) launched on Raspberry Pi and an application for Windows (in C# using WPF).
### User application
User application allows to convert the input colored image to grayscale, and then it performs binarization and generates control instructions (similar to G code). You can find the whole project here: https://github.com/zwolinski/rPi-engraver-userApp
### Driver 
The driver, based on received data, controls the motors, laser and power supply. You can find the code in this repo.

#### Launching the driver
You can run the driver as a standalone Python script. It will print some information that may help in debugging.
Type `drv.py <filename>` to start engraving image using instructions saved in the `filename` file.

_Note: if you type `drv.py` without any parameters, the script will look for default file name - gcode.txt_

#### Useful information
The script will inform you about currently performed action. Example is shown below (currently only in Polish).
```
Graweruje gcode.txt total: 1
Szacowany czas grawerowania: 600 s, 10 m
Zasilanie włączone
X: 300
Y: 350
Program zakonczyl dzialanie
Zasilanie wyłączone
```

### Device
Third part of the project is the device - a small-sized laser engraver.

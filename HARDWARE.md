# Hardware

This file contains technical specifications of the electronic components and instrunctions for building the electronic circuits.

## What is needed?

The following components are required:
1. Resistors: 5 pcs
2. Buttons: 3 pcs
3. [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/)
4. RGB LED-Strip (with 3 pins for RGB and 1 pin for 12V DC)
5. N-channel MOSFETs IRLB8721PBF TO-220: 3 pcs for controlling the LEDs
6. [Adafruit MAX98357 I2S Class-D Mono Amp](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)
7. Potentiometer 91A1A-B28-A25L for controlling the volume
8. Speaker FRWS 5 2210 - 8 ohm 
9. [ADC MCP3008](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)
10. White led (head diameter = 3mm): 3 pcs
11. Green led (head diameter = 5mm): 1 pcs
12. Jumper wires (male-to-male) for connecting the components 
13. Jumper wires (male-to-female) for the connection to the Raspberry Pi
14. DC-DC step up boost converter MT3608-I/P to supply the LED-Strip (12V DC ~2A)
15. Breadboard for plugging the components
16. Micro SD Memory Card 16GB

## How to connect components to the Raspberry Pi?

Here is an overview of the GPIO pins of the Raspberry Pi and their connections to different components.

![GPIO pins of the Raspberry Pi](/images/GPIO-Pinout-Diagram.png)

Breadboard schema
![Breadboard schema](/images/schema.png)

## What's next?


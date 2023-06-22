# Hardware

This file contains the list of the required electronic components (and their technical specifications) needed to build Sherlock. Visual instructions for assembling the electronic circuit board and the 3D-printed case follow below.

## Shopping List

To build Sherlock's electronic circuit board, the following are the required components:
* x1 [RaspberryPi Model 3B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) (or with at least the same specs).
* x1 [Adafruit MAX98357 I2S Class-D Mono Amp](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)
* x1 [ADC MCP3008](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)
* x1 N-Channel MOSFET (e.g., IRLB8721PBF TO-220).
* x1 Potentiometer (e.g., 91A1A-B28-A25L).
* x1 8Ohm, 5W Speaker (e.g., FRWS 5 2210) (size should not exceed 50mmx50mm, else the 3D model must be modified).
* x1 DC-DC Step-Up Boost Converter 12V DC~2A (e.g., MT3608-I/P).
* x1 MicroSD Memory Card 16GB.
* x1 USB-A Drive (size should be enough to fit the tracks to be played).
* x1 RGB (or White-only) LED Strip (w/ 3 pins for RGB and 1 pin for 12V DC).
* x5 Resistors.
* x3 Buttons.
* x1 Breadboard or x1 Stripboard.
* Jumper wires (M2M, M2F), as needed.

Additionally, **soldering** and **3D-printing** equipment might be needed if you want to fully build a Sherlock device.


## Electronic Circuit Board

Below you can find a schematic of the RaspberryPi 3B's GPIO pins numbering (source: [RaspberryPi official website](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)).

![GPIO pins of the Raspberry Pi](/images/GPIO-Pinout-Diagram.png)

Accordingly, here is the breadboard schema of the Sherlock system. The placement and connection of the pins does not necessarily need to be the same as the one pictured here, but it is important you note down which component connect to which pin as you will need this information in order to correctly control Sherlock.

![Breadboard schema](/images/schema.png)

Finally, make sure you update the [`config/sherlock_parameters.yaml`](./config/sherlock_parameters.yaml) configuration file with the correct pin numbering for each component. 

**Note**: the pin numbers must refer to the progressive numbering you can see in the middle in the first picture, NOT to the GPIO number (in the default configuration file, we put the GPIO naming as a comment).


## 3D-Printed Casing

If you also wish you 3D print our own designed Sherlock casing, you can use the following [`.stl` files](https://drive.google.com/drive/folders/1JhiT_K2lRhx8s-bbv2tqJ34ZVo5pxSb8?usp=sharing).

Below you can find a gallery of how the casing looks like.

![3D Concept Rough](/images/3d_concept_1.png)

![3D Concept Section](/images/taglio.png)

![3D Concept Nice](/images/3d_concept.png)
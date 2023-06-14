# Hardware

This file contains technical specifications of the electronic components and instrunctions for building the electronic circuits.

## What is needed?
### Parts
The following components are required:
- 4pcs resistors (220 ohm x 3pcs for LEDs, 100k ohm x 1pc for ampl) 
- 3pcs buttons for interaction
- 3pcs white LEDs (head diameter = 3mm)
- RGB LED-Strip (with 3 pins for RGB and 1 pin for 12V DC)
- 3pcs N-channel MOSFETs for LED-Strip control (ex. [IRLB8721PBF TO-220](https://www.amazon.it/dp/B087PLH4CF/ref=cm_sw_em_r_mt_dp_1ECYTS9GJSFTMCS22SKY?_encoding=UTF8&psc=1))
- DC-DC step up boost converter to supply the LED-Strip (12V DC ~2A) (ex. [MT3608-I/P](https://www.amazon.it/dp/B079H3YD8V/ref=cm_sw_em_r_mt_dp_AR0BF0BRPGJPTESRRRQ0))
- Speaker of 8 ohm for audio (ex. FRWS 5 2210)
- [Adafruit MAX98357 I2S Class-D Mono Amplifier](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)
- Potentiometer for volume control (ex. 91A1A-B28-A25L) [[Amazon](https://www.amazon.it/TECNOIOT-MAX98357-Amplificatore-decodificatore-filtrato/dp/B098R76CZX/ref=sr_1_2?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=337I5PKBAKPLP&keywords=MAX98357+I2S&qid=1686766851&sprefix=max98357+i2s%2Caps%2C154&sr=8-2)]
- [Analog-to-Digital Converter (ADC) MCP3008](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)
- [Jumper wires (male-to-male, male-to-female, female-to-female)](https://www.amazon.it/dp/B074P726ZR/ref=cm_sw_em_r_mt_dp_AZ8CZX0F8EN6JBA1W3QY) for connecting components and Raspberry Pi
- [Thermo-shrinkable polystyrene coatings](https://www.amazon.it/dp/B071D7LJ31/ref=cm_sw_em_r_mt_dp_28CDEAYFMQ3A130N26F7?_encoding=UTF8&psc=1)
- [Double sided PCB](https://www.amazon.it/dp/B073WR78M6/ref=cm_sw_em_r_mt_dp_dl_XRYPJ6CZ77HKW5WWWYAT) for plugging components
- 16GB Micro SD Memory Card with Raspberry Pi OS operating system on it (Otherwise you can install it following the [guide](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system))
- [Bluetooth 4.0 USB Adapter](https://www.sabrent.com/product/BT-UB40/usb-bluetooth-4-0-micro-adapter-pc-v4-0-class-2-low-energy-technology/#description)
- [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/)
- Power supply for Raspberry Pi 3 (with micro USB and at least 2.5 amps provided)

### Tools & Supplies
The following tools and supplies will get you started on your build:
- 3D printer
- Soldering iron and wire
- Flush diagonal cutters
- Scissors 
- Screwer
- Multimeter (nice to have to check connections in between components, but not required)
- Lighter


## How to connect components and Raspberry Pi?
### Circuit diagram
Here you can find an overview of the GPIO pins of the Raspberry Pi and their connections to different components.

![GPIO pins of the Raspberry Pi](/images/GPIO_Pinout_Diagram_with_labels_legend.png)

Now make sure to build your electronic circuit on PCB according the presented schema.

![PCB schema](/images/schema.png)

When all components are in place, carefully solder the connections to ensure that a steady contact is provided in between different elements.
In order to prevent establishing unwanted connections, it is best practice to insulate all exposed conducting parts by means of electrical insulation coatings. 

## 3D printing
The case ...

### Customize solids
If your interested in removing/adding/reshaping components, the original solids of the design are available for free to edit on Autodesk 123D at this [link]().

### Slicer settings
We recommend using the slice settings below. For really great quality prints, we recommend using PLA over ABS.

settings missing

## What's next?
Well done! You have just completed the hardware set up for this project.
Next, you will need to run some commands in order to install and make sure that also the software is ready.


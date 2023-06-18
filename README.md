<p align="center">
  <a href="https://github.com/Quellichenonsannofareuncazzo/Sherlock.git" alt="Sherlock Repository">
    <img src="images/sherlock_logo_3.png" height="150">
  </a>
  <h1 align="center">Hackability@Sherlock</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-alpha-yellow.svg" />
  <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-informational.svg">
</p>

<table align="center" style="background-color:rgba(0,0,0,0);">
  <tr style="background-color:rgba(0,0,0,0);">
    <td>A project by:</th>
    <td>In partnership with:</th>
  </tr>
  <tr style="background-color:rgba(0,0,0,0);">
    <td><a href="http://www.hackability.it/" alt="Hackability Website" target="_blank">
  		<img src="images/hackability_logo.svg" alt="Hackability Logo" width=200>
  	  </a></th>
    <td><a href="https://www.fondazionebrodolini.it/" alt="FGB Website" target="_blank">
		<img src="images/fgb_logo.png" alt="FGB Logo" width=200>
	  </a>
	  <a href="https://www.subvedenti.it/" alt="ANS Website" target="_blank">
		<img src="images/ans_logo.png" alt="ANS Logo" height=80 style="padding-right:20px;padding-left:20px">
	  </a>
	  <a href="https://www.interreg-central.eu/Content.Node/ECOS4IN.html" alt="ECOS4IN Website" target="_blank">
		<img src="https://www.interreg-central.eu/Content.Node/ECOS4IN-RGB.jpg" alt="ECOS4IN Logo" width=150>
	  </a></th>
</table>

## Introduction

This is the official repository for the **Hackability@Sherlock** project. 

The goal is to develop a **3D printed design object** which easily lets **visually impaired people** (but also normally sighted people) get a quick and informative **audio description of a small indoor space** - such as an hotel room, to get an understanding of where and which objects are present in the room.

Sherlock will be composed of the following components:
* an **audio speaker**.
* an **electronic circuit** to "read" the user's input (through the pressing of **buttons**).
* a **Raspberry Pi** to control everything.
* a **3D printed casing**, with buttons and Braille text.

We will try to make Sherlock as simple and yet configurable as possible, where users can just drag-and-drop their audio tracks to be reproduced and Sherlock will be able to reproduce them.

Our vision is to create an object which integrates well into any environment and is able to make any person feel welcome and at home in any new indoor space.

## Installation

0. Make sure your electronic circuit and PCB is built following the schema in `SherlockSketch.fzz`.

1. Open a terminal window in your RaspberryPi (you can either connect through `SSH` or directly to the device).

2. Clone the repository into your preferred location:
```
cd /path/to/your/folder
git clone https://github.com/Quellichenonsannofareuncazzo/Sherlock
cd Sherlock
```
3. **[Optional]** Create a virtual environment for the project:
```
python3 -m venv <your-venv-name>
source <your-venv-name>/bin/activate 
```
4. Install project dependencies:
```
pip3 install -r requirements.txt
```

## Usage
1. Check and update the [`config/sherlock_parameters.yaml`](config/sherlock_parameters.yaml) configuration file with the actual pins used and with your preferred settings. More details on individual settings can be found in the `Sherlock` class [docstring](src/sherlock.py#L8).

2. From the command line, run:
```
python3 src/main.py 
```
and enjoy the experience! 

**N.B.**: at the moment, only `.mp3` audio files are supported. Please, do convert your audio files to the supported file formats.

## To-do List

Below, a non-comprehensive list of stuff we should do in the future:
* **[MEDIUM]** Update `README.md` with the exact RaspberryPi model used for prototyping and testing (including Ubuntu distro, Python version, etc.) for reproducibility purposes.
* **[LOW]** Create a file with detailed technical specifications of the electronic components (resistors, LEDs, etc.). [here](./HARDWARE.md)
* **[MEDIUM]** Clean and update `requirements.txt` and check all dependencies (eventually try to see if we can work with the latest releases to get better long-term support).
* **[LOW]** Use conda venvs instead of python venv, so that we can also control the Python version
* **[MEDIUM]** Add the outer case 3D CAD model file to the repository.
* **[LOW]** Add images of Sherlock's final prototype, and possibly of videos of it working. Also, add other images to use in the `README.md` file (e.g., ~~Sherlock and Hackability logos~~, electronic circuit, 3D CAD model, etc.).
* **[VERY LOW]** Add shields for release, license, etc.
* **[HIGH]** Implement fast-backward.
* **[HIGH]** Test fast-for/backward functions when end/start of track is reached.

Use GH Issues to open MRs/PRs for new improvements and adding functionalities.

Task priorities are in brackets.

## Acknowledgements

The Sherlock project was realized by [Hackability@Milano](http://www.hackability.it/hackabilitymilano/), in partnership with [Fondazione G. Brodolini](https://www.fondazionebrodolini.it/) and [Associazione Nazionale Subvedenti](https://www.subvedenti.it/), whose contributions were essential for the brainstorming and development of Sherlock. 

Therefore, we would like to thank both the associations and the involved people: **Debora**, **Rosa**, **Monica**, and **Marco**. Also, many thanks to **Francesco De Rosa**, **Roberto Frisina**, and **Federico Zucca** for partipating and giving your feedbacks during the Workshop. 

The project was initially ideated in the context of the [EU's ECOS4IN project](https://www.interreg-central.eu/Content.Node/ECOS4IN.html), whose aim is to 
> promote sustainable and close cooperation among innovation actors and stakeholders, in order to improve and better equip European regions to face changes brought by the advent of the Industry 4.0. The goal of the project is to build a tool called **ECOS4IN Knowledge Base**, which will be tested in pilots as an essential source of information to raise awareness about Industry 4.0.

Sherlock is a byproduct of the **ECOS4IN Workshop** organized by Fondazione G. Brodolini with makers from Hackability@Milano, and inclusion stakeholders from Associazione Nazionale Subvedenti. 

## Contacts
If you have any questions, want to contribute, or want more information, feel free to reach out to us.
* **Hackability@Milano**, [milano@hackability.it](mailto:milano@hackability.it)
* Teo Bistoni, [@TeoBistoni](https://github.com/TeoBistoni)
* Dario Comini, [@mrDaerio](https://github.com/mrDaerio)
* Tam Huynh, [@mtdhuynh](https://github.com/mtdhuynh)
* Rossella Indaco, [@rossinda](https://github.com/rossinda)
* Francesco Rodighiero
* Luca Bocedi

## License

The Sherlock project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa], as found in the [LICENSE.md](LICENSE.md) file.

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png

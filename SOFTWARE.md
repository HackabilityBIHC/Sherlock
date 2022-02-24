# Software

## Installation

Make sure your electronic circuit and PCB is built following the schema in `SherlockSketch.fzz`.

Open a terminal window in your RaspberryPi (you can either connect through `SSH` or directly to the device).

Clone the repository into your preferred location:
```
cd /path/to/your/folder
git clone https://github.com/Quellichenonsannofareuncazzo/Sherlock
cd Sherlock
```
**[Optional]** Create a virtual environment for the project:
```
python3 -m venv <your-venv-name>
source <your-venv-name>/bin/activate 
```
Install project dependencies:
```
pip install -r requirements.txt
```

## Usage

From the command line, run:
```
python3 main.py 
```
and enjoy the experience! 

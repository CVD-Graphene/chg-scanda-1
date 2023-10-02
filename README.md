# cvd-graphene
PyQt6 realisation

### Installation and running

1. Create python3.9 venv
2. run cmd: `source venv/bin/activate`
   1. For ubuntu: 
      1. `sudo apt install qt5-default`
      2. `sudo python3 -m pip install --upgrade pip`
      3. `python -m pip install --upgrade setuptools`
3. install requirements, run cmd: `pip install -r requirements.txt`
4. start project:
   1. in Pycharm add config with start `app.py`
   2. or in cmd: `python app.py`
5. **Done!**


## Core module

### Components hierarchy

↓ **Communication methods** - python realization of send/receive/setup  
↓ **Communicators** - algorithms of communication between device and main system  
↓ **Devices** - analog of real device to communicate with  
↓ **Controllers** - device controllers with realization of sequences of commands, algorithms, single commands and so on  
↓ **System** - main administrator for management all communicators with realization of logging, analysis exceptions, run tasks and so on  


### Notes

 - Install PyQt5 on mac with homebrew: `export PATH="/opt/homebrew/opt/qt5/bin:$PATH"` && `pip install pyqt5 --config-settings --confirm-license= --verbose`
 - 
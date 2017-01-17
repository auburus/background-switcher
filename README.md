# Background Switcher

Pet project to update my screen background using the photo of the day
provided by [fuckinghomepage](http://fuckinghomepage.com)

Note: I've got an XFCE desktop

## Installation
This program requires Python3 to work.

Run the following commands:

    git clone git@github.com:auburus/background-switcher.git
    cd background-switcher
    source ./venv/bin/activate
    pip install -r requirements.txt
    python3 main.py # Check that runs without errors
    deactivate

After that, a new file called `image` should be present in the folder.
Set this file as the background, and run the `background-switcher`
executable at startup (Settings Manager > Session and Startup > Application
Autostart > Add).

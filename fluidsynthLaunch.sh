#!/bin/bash
#cd /usr/share/sounds/sf2
#fluidsynth -i -s -a alsa FluidR3_GM.sf2

#pgrep -d',' fluidsynth to get PID
#kill PID
cd /home/pi/Documents/Fireplace/Soundfonts && fluidsynth -i -s -a alsa Spacesweep.sf2

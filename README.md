# Haptic speech
## _enhancement & training_
Examines the effect of vibrotactile feedback on speech intelligibility using a training paradigm

#### Folder descriptions:
```
/stimuli : directory of all .wav stimuli (PLACE STIMULI IN THE ROOT OF THIS FOLDER)
/responses : contains participant responses, organized in directories that are labeled by participant ID. Also contains helper scripts to easily pull/push stuff from the SPIN server
/old : contains old scripts from previous versions of this study. Kept just in case.
/minpairs : tools for prepping a database of minimal pairs (folder is not relevant for the experiment proper)
```

#### Module structure:
```
main.py (experiment control flow)
	|- utilities.py (helper functions)
	|- playback.py (playback functions)
	|- parameters.py (static variables)
	|- textdisplay.py (text rendering)
	|- voicingfilter.py (detects voicing)
```

---

### This program generates a sine wave coupled to the RMS amplitude of a sound file.

- Left channel: input signal (i.e. speech)  
- Right channel: output signal (i.e. sine wave)  

The right channel may be piped to a vibrotactile actuator for a haptic representation of vocal amplitude.

### Running the software:
- In terminal run `python main.py`
- You may specify windowed mode with the `-w` flag (`python main.py -w`)
- You may run without calibrating with the `-nc` (no calibration) flag (`python main.py -nc`)

#### Requirements:

- [Python 2.7](https://python.org)  
- Pygame  
- Pyaudio 

#### Setup instructions:
You can install modules using the pip package manager:
- pygame: `pip install pygame`
- pyaudio: `pip install pyaudio` (NOTE: PyAudio is Python bindings for PortAudio, so you may need to install PortAudio if you don't have it yet)


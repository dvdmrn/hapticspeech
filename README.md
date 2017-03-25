# Haptic speech

### Generates a sine wave coupled to the RMS amplitude of a sound file.

- Left channel: input signal (i.e. speech)  
- Right channel: output signal (i.e. sine wave)  

The right channel may be piped to a vibrotactile actuator for a haptic representation of vocal amplitude.

### Running the software:
- In terminal run `python main.py`
- You may specify windowed mode with the `-w` flag (`python main.py -w`)

#### Requirements:

- [Python 2.7](https://python.org)  
- Pygame  
- Pyaudio  

#### Setup instructions:
You can install modules using the pip package manager:
- pygame: `pip install pygame`
- pyaudio: `pip install pyaudio` 

#### Module structure:
```
main.py
	|- utilities.py (helper functions)
	|- playback.py (playback functions)
	|- recorder.py (recording functions)
	|- parameters.py (static variables)
	|- textdisplay.py (text rendering)
```

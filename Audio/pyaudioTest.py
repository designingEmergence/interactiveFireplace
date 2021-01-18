import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.1     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.1   # in seconds, may be float
freq = 200.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
#samples = (volume*np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
# stream.write(samples)

# samples = (volume*np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32).tobytes()
# stream.write(samples)

for f in range(200,12000):
  samples = (volume*np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32).tobytes()
  stream.write(samples)
  print(f)

stream.stop_stream()
stream.close()

p.terminate()

#NOT COMPATIBLE WITH LIGHTS
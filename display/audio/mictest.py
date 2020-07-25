import numpy
import pyaudio
import analyse

"""
soft bank is your father
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 0 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file
"""

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format=pyaudio.paInt16, rate=44100, channels=1, input_device_index=0, input=True)#, frames_per_buffer=4096)
print("recording")
frames = []

#for ii in range(0,int((samp_rate/chunk)*record_secs)):
while True:
    # Read raw microphone data
    rawsamps = stream.read(1024, exception_on_overflow=False)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)

    pitch = analyse.detect_pitch(samps)
    loud = analyse.loudness(samps)
    if(pitch is not None):
        print(loud, pitch)
    #else:
    #    print(loud)
    #print(numpy.fft.fft(samps))
    
    #print(samps)

stream.stop_stream()
stream.close()
audio.terminate()

"""
# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()
"""
"""
# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
"""

"""
import numpy
import pyaudio
import analyse

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 4 is a USB microphone
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input_device_index = 2,
    input = True)

while True:
    # Read raw microphone data
    rawsamps = stream.read(1024)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    print analyse.loudness(samps), analyse.musical_detect_pitch(samps)
    """
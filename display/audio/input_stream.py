import pyaudio


class InputStream:
    p = pyaudio.PyAudio()
    stream = None
    data = None

    chunk_size = None

    def init_input_stream(self, chunk_size, frame_rate):
        self.chunk_size = chunk_size
        self.stream = self.p.open( format = pyaudio.paInt16,
                                   channels = 1,
                                   rate = frame_rate,
                                   input = True)
        self.data = self.stream.read(self.chunk_size, exception_on_overflow=False)

    def tick_input_stream(self):
        self.data = self.stream.read(self.chunk_size, exception_on_overflow=False)

    def get_input_data(self):
        return self.data

    def stop_input_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


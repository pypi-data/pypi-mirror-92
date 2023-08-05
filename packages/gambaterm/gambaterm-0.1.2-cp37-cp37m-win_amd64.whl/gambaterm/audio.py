from queue import Queue, Empty, Full
from contextlib import contextmanager

import samplerate
import sounddevice
import numpy as np


class AudioOut:

    input_rate = 60 * 35112
    output_rate = 48000
    buffer_size = output_rate // 60

    def __init__(self, speed=1.0):
        self.speed = speed
        self.queue = Queue(maxsize=2)
        self.resampler = samplerate.Resampler("linear", channels=2)
        self.buffer = np.full((self.buffer_size, 2), 0.0, np.int16)
        self.offset = 0
        self.to_send = None

    @property
    def ratio(self):
        return self.output_rate / self.input_rate / self.speed

    def send(self, audio):
        # Set the right type and shape
        (length,) = audio.shape
        audio.dtype = np.int16
        audio.shape = (length, 2)
        # Resample to output rate
        data = self.resampler.process(audio, self.ratio).astype(np.int16)
        # Write the current buffer
        stop = min(self.buffer_size, self.offset + len(data))
        self.buffer[self.offset : stop] = data[: stop - self.offset]
        # Current buffer is not full
        if stop != self.buffer_size:
            self.offset = stop
            return
        # Decrease volume
        self.buffer //= 4
        # Current buffer is full, send without blocking
        try:
            self.queue.put_nowait(self.buffer)
        # Schedule blocking send for next call to sync
        except Full:
            self.to_send = self.buffer
        # Create new buffer
        self.buffer = np.full((self.buffer_size, 2), 0.0, np.int16)
        # Fill the extra data
        extra_data = data[stop - self.offset :]
        self.offset = len(extra_data)
        self.buffer[: self.offset] = extra_data

    def sync(self):
        if self.to_send is not None:
            self.queue.put(self.to_send)
            self.to_send = None

    def stream_callback(self, output_buffer, *args):
        try:
            output_buffer[:] = self.queue.get_nowait()
        except Empty:
            output_buffer.fill(0.0)


@contextmanager
def audio_player(speed_factor=1.0):
    audio_out = AudioOut(speed_factor)
    with sounddevice.OutputStream(
        samplerate=audio_out.output_rate,
        dtype="int16",
        channels=2,
        latency="low",
        blocksize=audio_out.buffer_size,
        callback=audio_out.stream_callback,
    ):
        yield audio_out


@contextmanager
def no_audio(speed_factor=1.0):
    yield None

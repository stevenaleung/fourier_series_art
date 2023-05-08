from matplotlib import pyplot as plt
import numpy as np


class FreqComponentArtist:
    def __init__(self, amplitude, phase, angular_freq, time_step_per_frame, ax):
        self.position = np.array([0.0, 0.0])
        self.amplitude = amplitude
        self.phase = phase
        self.angular_freq = angular_freq
        self.time_step_per_frame = time_step_per_frame
        self.circle_drawing = ax.plot([], [], linewidth=0.5)[0]
        self.line_drawing = ax.plot([], [], linewidth=2, color=self.circle_drawing.get_color())[0]

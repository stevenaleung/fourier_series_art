import utils
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

    def update(self, new_position):
        self._update_position(new_position)
        self._update_phase()

    def _update_position(self, new_position):
        self.position = new_position

    def _update_phase(self):
        self.phase = self.phase + (self.angular_freq * self.time_step_per_frame)

    def draw(self):
        self._draw_circle()
        self._draw_line()

    def _draw_circle(self):
        x_center, y_center = self.position
        x_coords, y_coords = utils.get_circle_coordinates(x_center, y_center, self.amplitude)
        self.circle_drawing.set_data(x_coords, y_coords)

    def _draw_line(self):
        x_center, y_center = self.position
        x_endpoints = np.array([0, self.amplitude*np.cos(self.phase)]) + x_center
        y_endpoints = np.array([0, self.amplitude*np.sin(self.phase)]) + y_center
        self.line_drawing.set_data(x_endpoints, y_endpoints)

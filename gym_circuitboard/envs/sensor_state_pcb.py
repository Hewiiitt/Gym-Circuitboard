import numpy as np

import matplotlib.pyplot as plt

from gym import spaces

from gym_circuitboard.common import generate_empty_baord
from gym_circuitboard.envs.basic_premade_pcb import DefaultPCB


class SensorStatePCB(DefaultPCB):

    def __init__(self, columns, rows, traces, view_window=(5,5), max_steps=50):
        rng = np.random.RandomState()
        padding = np.floor(np.array(view_window)/2).astype(int)

        board, goal_info = generate_empty_baord(rng, rows, columns, traces, padding)

        super(SensorStatePCB, self).__init__(rng, board, goal_info, view_window, max_steps=max_steps)

    @property
    def observation_space(self):
        return spaces.Box(
            np.zeros(10) - 256,
            np.zeros(10) + 256,
            dtype=np.float64
        )

    def exlore_laser(self, current_pos, direction):

        for i in range(1, 100):
            offset = direction * i
            pos = current_pos + offset
            if self.board_clone[pos[1], pos[0]] == 1:
                return np.sqrt(offset[1]**2 + offset[0]**2) - 1.0

        return 200

    dir = [
        np.array([-1, -1]),  # 0
        np.array([-1, 0]),  # 1
        np.array([-1, 1]),  # 2
        np.array([0, -1]),  # 3
        np.array([0, 1]),  # 4
        np.array([1, -1]),  # 5
        np.array([1, 0]),  # 6
        np.array([1, 1]),  # 7
    ]

    def _get_obs(self):
        lasers = np.zeros(8, dtype=float)

        for i in range(8):
            lasers[i] = self.exlore_laser(self.current_position, SensorStatePCB.dir[i])

        return np.append(
            lasers,
            self.traces[self.current_trace].get_end() - self.current_position
        ).flatten()

        # return self.board_clone[
        #     int(self.edge_padding[0]):-int(self.edge_padding[0]),
        #     int(self.edge_padding[0]):-int(self.edge_padding[0])
        # ].flatten()


if __name__ == '__main__':

    env = SensorStatePCB(6, 6, 1, (7, 7))
    images = []
    obs = env.reset()
    print(obs)
    img = env.render()
    plt.figure()
    plt.imshow(img)
    plt.show()
    print('hi')

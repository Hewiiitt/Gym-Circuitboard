import numpy as np

from gym import spaces

from gym_circuitboard.common import generate_empty_baord
from gym_circuitboard.envs.basic_premade_pcb import DefaultPCB


class FullStatePCB(DefaultPCB):

    def __init__(self, columns, rows, traces, view_window=(5,5), max_steps=50):
        rng = np.random.RandomState()
        padding = np.array([0, 0])

        board, goal_info = generate_empty_baord(rng, rows, columns, traces, padding)

        super(FullStatePCB, self).__init__(rng, board, goal_info, view_window, max_steps=max_steps)

    @property
    def observation_space(self):
        s = self.board_clone[
            int(self.edge_padding[0]):-int(self.edge_padding[0]),
            int(self.edge_padding[0]):-int(self.edge_padding[0])
        ].flatten().shape[0]
        return spaces.Box(
            np.zeros(s) - 256,
            np.zeros(s) + 256,
            dtype=np.float64
        )

    def _get_obs(self):
        return self.board_clone[
            int(self.edge_padding[0]):-int(self.edge_padding[0]),
            int(self.edge_padding[0]):-int(self.edge_padding[0])
        ].flatten()


# if __name__ == '__main__':
#
#     env = FullStatePremadePCB('../test_files/dummy_env.txt')
#     images = []
#     obs = env.reset()
#     obs_space = env.observation_space
#     img = env.render()
#     images.append(img)
import copy

# import imageio

import numpy as np

from gym_circuitboard.envs.pcb_default import DefaultPCB

from gym_circuitboard.common import generate_empty_baord, Trace

import matplotlib.pyplot as plt


class BasicResetPCBEnv(DefaultPCB):

    def __init__(self, columns, rows, traces, view_window=(5,5), max_steps=50):

        rng = np.random.RandomState()
        self.padding = np.floor(np.array(view_window)/2).astype(int)

        self.rows = rows
        self.cols = columns
        self.traces_count = traces

        board, goal_info = generate_empty_baord(rng, rows, columns, traces, self.padding)

        super(BasicResetPCBEnv, self).__init__(rng, board, goal_info, view_window, max_steps=max_steps)

    def _reset_(self):
        self.current_trace = 0

        board, goal_info = generate_empty_baord(self.rng, self.rows, self.cols, self.traces_count, self.padding)

        self.base_board = board
        self.board_clone = copy.deepcopy(self.base_board)
        self.goal_info = goal_info

        starts = []
        for idx in range(self.n_traces):
            goal, available_inits = self.goal_info[idx]
            for s in starts:
                try:
                    available_inits = available_inits.remove(s)
                except:
                    pass
            i = self.rng.choice(np.linspace(0, len(available_inits) - 1, len(available_inits), dtype=np.int),
                                1, replace=False)
            start = available_inits[i.item()]
            self.board_clone[start[1], start[0]] = 1
            self.board_clone[goal[1], goal[0]] = 1
            trace = Trace(start, goal)
            self.traces[idx] = trace

        self.current_position = self.traces[0].get_start()
        self.traces[self.current_trace].add(self.current_position)
        self.board_clone[self.current_position[1], self.current_position[0]] = 3
        goal = self.traces[0].get_end()
        self.board_clone[goal[1], goal[0]] = 2

        # print(self._get_obs()[:-2].reshape(7, 7))

        return self._get_obs()

if __name__ == '__main__':

    env = BasicResetPCBEnv(6, 6, 1, (7,7))
    images = []
    obs = env.reset()
    img = env.render()
    images.append(img)
    # obs, rwd, done, _ = env.step(0)
    for i in range(1000):
        plt.figure()
        plt.imshow(obs[:-2].reshape(7,7))
        plt.show()
        action = int(input('0 3 5\n1   6\n2 4 7\n'))
        obs, rwd, done, _ = env.step(action)
        img = env.render(mode='rgb_array')
        images.append(img)
        print(rwd)
        if done:
            break


    print('hi')

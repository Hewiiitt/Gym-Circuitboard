# import imageio

import numpy as np

from gym_circuitboard.envs.pcb_default import DefaultPCB

from gym_circuitboard.common import generate_empty_baord

import matplotlib.pyplot as plt


class BasicPCBEnv(DefaultPCB):

    def __init__(self, columns, rows, traces, view_window=(5,5), max_steps=50):

        rng = np.random.RandomState()
        padding = np.floor(np.array(view_window)/2).astype(int)

        board, goal_info = generate_empty_baord(rng, rows, columns, traces, padding)

        super(BasicPCBEnv, self).__init__(rng, board, goal_info, view_window, max_steps=max_steps)


if __name__ == '__main__':

    env = BasicPCBEnv(6, 6, 1, (7,7))
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

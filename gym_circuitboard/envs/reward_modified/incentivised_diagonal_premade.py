import numpy as np

import matplotlib.pyplot as plt

from gym import spaces

from gym_circuitboard.common import generate_empty_baord
from gym_circuitboard.envs.sensor_state_premade_pcb import SensorStatePremadePCB
# from gym_circuitboard.envs.basic_pcb import BasicPCBEnv


class IncentivisedDiagonal(SensorStatePremadePCB):

    def __init__(self, file_path, view_window=(5,5), max_steps=50):
        super(IncentivisedDiagonal, self).__init__(file_path, view_window=view_window, max_steps=max_steps)

    def _get_reward(self, step_info):

        reward = 0

        action_selected = step_info['action']

        total_action_val = np.abs(action_selected).sum()

        if total_action_val < 2:
            if np.all(step_info['original_pos'] == step_info['final_pos']):
                reward = -1
            else:
                reward = -0.5
        else:
            if np.all(step_info['original_pos'] == step_info['final_pos']):
                reward = -1
            else:
                reward = -0.15

        reward += 5 if step_info['goal_reached'] else 0
        reward += 10 if step_info['done'] and step_info['goal_reached'] else 0
        return reward


if __name__ == '__main__':

    env = IncentivisedDiagonal(6, 6, 1, (7, 7))
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

import numpy as np

import matplotlib.pyplot as plt

from gym import spaces

from gym_circuitboard.common import generate_empty_baord
from gym_circuitboard.envs.sensor_state_pcb import SensorStatePCB
# from gym_circuitboard.envs.basic_pcb import BasicPCBEnv


class ShapedReward(SensorStatePCB):

    def __init__(self, columns, rows, traces, view_window=(5,5), max_steps=50):
        super(ShapedReward, self).__init__(columns, rows, traces, view_window=view_window, max_steps=max_steps)

    def euclideon_dist(self, vect):
        return np.sqrt(vect[0]**2 + vect[1]**2)

    def _get_reward(self, step_info):
        start_dist = self.euclideon_dist(step_info['original_pos'] - self.traces[self.current_trace].get_end())
        end_dist = self.euclideon_dist(step_info['final_pos'] - self.traces[self.current_trace].get_end())

        reward = (-np.sqrt(2) + (start_dist - end_dist)) / (2*np.sqrt(2))
        reward += 5 if step_info['goal_reached'] else 0
        reward += 10 if step_info['done'] and step_info['goal_reached'] else 0
        return reward


if __name__ == '__main__':

    env = ShapedReward(6, 6, 1, (7, 7))
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

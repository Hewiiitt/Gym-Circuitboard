# import imageio

import numpy as np

from gym_circuitboard.envs.pcb_default import DefaultPCB

from gym_circuitboard.common import load_premade_env

import matplotlib.pyplot as plt


class PremadePCBEnv(DefaultPCB):

    def __init__(self, file_path, view_window=(5,5), max_steps=50):

        rng = np.random.RandomState()
        padding = np.floor(np.array(view_window)/2).astype(int)

        board, goal_info = load_premade_env(file_path, padding)

        super(PremadePCBEnv, self).__init__(rng, board, goal_info, view_window, max_steps=max_steps)

    # def _get_obs(self):
    #     count = 2
    #     for trace in self.traces:
    #         s = trace.get_start()
    #         e = trace.get_end()
    #         self.base_board[s[1], s[0]] = count
    #         self.base_board[e[1], e[0]] = count
    #         count += 1
    #     return self.base_board


# if __name__=="__main__":
#     env = PremadePCBEnv('./test.csv', (7, 7))
#     obs = env.reset()
#     plt.figure()
#     plt.imshow(obs)
#     plt.show()

# if __name__ == '__main__':
#
#     env = BasicPCBEnv(7, 7, 2, (7,7))
#     images = []
#     obs = env.reset()
#     img = env.render()
#     images.append(img)
#     # obs, rwd, done, _ = env.step(0)
#     for i in range(1000):
#         plt.figure()
#         plt.imshow(obs[:-2].reshape(7,7))
#         plt.show()
#         action = int(input('0 3 5\n1   6\n2 4 7\n'))
#         obs, rwd, done, _ = env.step(action)
#         img = env.render(mode='rgb_array')
#         images.append(img)
#         print(rwd)
#         if done:
#             break
# 
#     imageio.mimsave('output.gif', [np.array(img) for i, img in enumerate(images)], fps=29)
#
#
#     print('hi')
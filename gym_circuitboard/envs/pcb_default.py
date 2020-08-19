import numpy as np

from gym import spaces

from PIL import Image, ImageDraw

from gym_circuitboard.common import DiscretePCBBaseEnv, Trace


class DefaultPCB(DiscretePCBBaseEnv):

    def __init__(self, rng, board, goal_info, view_window=(5,5), max_steps=50):
        super(DefaultPCB, self).__init__(rng, board, goal_info, max_steps=max_steps)

        self.view_window = view_window
        self.edge_padding = np.floor(np.array(self.view_window)/2)

        self.actions = [
            np.array([-1, -1]),  # 0
            np.array([-1, 0]),  # 1
            np.array([-1, 1]),  # 2
            np.array([0, -1]),  # 3
            np.array([0, 1]),  # 4
            np.array([1, -1]),  # 5
            np.array([1, 0]),  # 6
            np.array([1, 1]),  # 7
        ]

    @property
    def observation_space(self):
        s = self.view_window[0] * self.view_window[1] + 2
        return spaces.Box(
            np.zeros(s) - 256,
            np.zeros(s) + 256,
            dtype=np.float64
        )

    @property
    def action_space(self):
        return spaces.Discrete(
            len(self.actions)
        )

    def _reset_(self):
        self.current_trace = 0

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

    def _step_(self, action):
        step_info = self._step_env(action)
        reward = self._get_reward(step_info)

        # print(self._get_obs()[:-2].reshape(7, 7))

        return self._get_obs(), reward, step_info['done'], step_info

    def _step_env(self, action):
        a = self.actions[action]
        new_position = self.current_position + a

        step_info = {
            'action': a,
            'original_pos': self.current_position,
            'final_pos': self.current_position,
            'step_success': False,
            'goal_reached': False,
            'total_traces': self.n_traces,
            'done': False
        }

        if 0 <= new_position[0] < self.base_board.shape[1] and \
                0 <= new_position[1] < self.base_board.shape[1] and \
                self.board_clone[new_position[1], new_position[0]] != 1:

            valid = False

            if action in [1, 3, 4, 6]:
                valid = True
            else:
                if action == 0:
                    if self.board_clone[self.current_position[1] - 1, self.current_position[0]] == 0 and \
                            self.board_clone[self.current_position[1], self.current_position[0] - 1] == 0:
                        valid = True
                elif action == 5:
                    if self.board_clone[self.current_position[1] - 1, self.current_position[0]] == 0 and \
                            self.board_clone[self.current_position[1], self.current_position[0] + 1] == 0:
                        valid = True
                elif action == 2:
                    if self.board_clone[self.current_position[1] + 1, self.current_position[0]] == 0 and \
                            self.board_clone[self.current_position[1], self.current_position[0] - 1] == 0:
                        valid = True
                elif action == 7:
                    if self.board_clone[self.current_position[1] + 1, self.current_position[0]] == 0 and \
                            self.board_clone[self.current_position[1], self.current_position[0] + 1] == 0:
                        valid = True
                else:
                    valid = False

            if valid:
                step_info['step_success'] = True
                self.board_clone[self.current_position[1], self.current_position[0]] = 1
                self.current_position = new_position
                self.traces[self.current_trace].add(self.current_position)
                self.board_clone[self.current_position[1], self.current_position[0]] = 3

        if np.all(self.current_position == self.traces[self.current_trace].get_end()):
            self.traces[self.current_trace].add(self.current_position)
            self.board_clone[self.current_position[1], self.current_position[0]] = 1
            step_info['goal_reached'] = True
            # self.paths.append(self.current_path)
            if self.current_trace >= self.n_traces - 1:
                # reward += 10
                step_info['done'] = True
                # print('Len of Paths {} and given reward {}'.format(len(self.paths), reward))
            else:
                self.current_trace += 1
                self.current_position = self.traces[self.current_trace].get_start()
                self.board_clone[self.current_position[1], self.current_position[0]] = 3
                goal = self.traces[self.current_trace].get_end()
                self.board_clone[goal[1], goal[0]] = 2
                self.traces[self.current_trace].add(self.current_position)

        elif self.timesteps > self.max_steps:
            step_info['done'] = True

        step_info['final_pos'] = self.current_position

        return step_info

    def _render_(self, mode):
        # print('Len of Paths {} at render'.format(len(self.paths)))
        img = Image.new('RGB', (self.board_clone.shape[1] * 25, self.board_clone.shape[0] * 25), color=(41, 110, 1))
        d = ImageDraw.Draw(img)

        for trace in self.traces:
            g = trace.get_end()
            s = trace.get_start()
            self.base_board[g[1], g[0]] = 0
            self.base_board[s[1], s[0]] = 0

        for y in range(self.base_board.shape[1]):
            for x in range(self.base_board.shape[0]):
                if self.base_board[x, y] == 1:
                    d.rectangle([(y * 25, x * 25), ((y + 1) * 25), (x + 1) * 25], fill=(60, 60, 60),
                                outline=(30, 30, 30))

        pixel_center = [np.floor(25 / 2), np.floor(25 / 2)]

        count = 0
        for trace in self.traces:
            start, end, path = trace.get_path()
            for i in range(1, len(path)):
                x_1 = (path[i - 1][0]) * 25 + pixel_center[0]
                y_1 = (path[i - 1][1]) * 25 + pixel_center[1]

                x_2 = (path[i][0]) * 25 + pixel_center[0]
                y_2 = (path[i][1]) * 25 + pixel_center[1]
                d.line([(x_1, y_1), (x_2, y_2)], fill=self.colors[count], width=3)
            count += 1

        count = 0
        for trace in self.traces:
            s = trace.get_start()
            g = trace.get_end()
            x_1 = (s[0]) * 25 + pixel_center[0]
            y_1 = (s[1]) * 25 + pixel_center[1]

            d.ellipse([(x_1 - 5, y_1 - 5), (x_1 + 5, y_1 + 5)], fill=self.colors[count], width=10)

            x_1 = (g[0]) * 25 + pixel_center[0]
            y_1 = (g[1]) * 25 + pixel_center[1]

            d.ellipse([(x_1 - 5, y_1 - 5), (x_1 + 5, y_1 + 5)], fill=self.colors[count], width=10)

            count += 1

        return img

    def _get_obs(self):
        return np.append(
            self.board_clone[
                int(self.current_position[1] - self.edge_padding[1]):int(self.current_position[1] + self.edge_padding[1]) + 1,
                int(self.current_position[0] - self.edge_padding[0]):int(self.current_position[0] + self.edge_padding[0]) + 1
            ].reshape(-1),
            self.traces[self.current_trace].get_end() - self.current_position
        ).flatten()

    def _get_reward(self, step_info):
        reward = -0.1
        reward += 5 if step_info['goal_reached'] else 0
        reward += 10 if step_info['done'] and step_info['goal_reached'] else 0
        return reward

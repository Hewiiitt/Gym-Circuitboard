import gym
import copy

from abc import ABC, abstractmethod

from .util import Colors


class DiscretePCBBaseEnv(gym.Env):

    def __init__(self, rng, board, goal_info, max_steps=50):
        self.rng = rng
        self.base_board = board
        self.board_clone = copy.deepcopy(self.base_board)
        self.goal_info = goal_info
        self.n_traces = len(goal_info)
        self.traces = [None] * self.n_traces
        self.current_trace = 0
        self.current_position = None
        self.colors = Colors()
        self.max_steps = max_steps
        self.timesteps = 0

    def reset(self):
        self.timesteps = 0
        self.board_clone = copy.deepcopy(self.base_board)
        return self._reset_()

    def step(self, action):
        self.timesteps += 1
        return self._step_(action)

    def render(self, mode='human'):
        return self._render_(mode)

    @property
    @abstractmethod
    def observation_space(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def action_space(self):
        raise NotImplementedError()

    @abstractmethod
    def _reset_(self):
        raise NotImplementedError()

    @abstractmethod
    def _step_(self, action):
        raise NotImplementedError()

    @abstractmethod
    def _render_(self, mode):
        raise NotImplementedError()

    @abstractmethod
    def _step_env(self, action):
        raise NotImplementedError()

    @abstractmethod
    def _get_obs(self):
        raise NotImplementedError()

    @abstractmethod
    def _get_reward(self, step_info):
        raise NotImplementedError()

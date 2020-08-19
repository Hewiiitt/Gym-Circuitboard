import numpy as np

from gym.envs.registration import register

register(
    id='auto-v0',
    entry_point='gym_circuitboard.envs:BasicPCBEnv',
    kwargs={
        'rows': 5,
        'columns': 5,
        'traces': 1,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)

register(
    id='premade-v0',
    entry_point='gym_circuitboard.envs:PremadePCBEnv',
    kwargs={
        'file_path': None,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)

register(
    id='premade-v1',
    entry_point='gym_circuitboard.envs:PremadePCBEnvAllBoardState',
    kwargs={
        'file_path': None,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)
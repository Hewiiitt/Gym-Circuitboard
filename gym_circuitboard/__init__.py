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

# register(
#     id='auto-v2',
#     entry_point='gym_circuitboard.envs:BasicResetPCBEnv',
#     kwargs={
#         'rows': 5,
#         'columns': 5,
#         'traces': 1,
#         'view_window': np.array([7, 7]),
#         'max_steps': 50
#     }
# )

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
    entry_point='gym_circuitboard.envs:FullStatePremadePCB',
    kwargs={
        'file_path': None,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)

register(
    id='auto-v1',
    entry_point='gym_circuitboard.envs:FullStatePCB',
    kwargs={
        'rows': 5,
        'columns': 5,
        'traces': 1,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)

register(
    id='auto-v2',
    entry_point='gym_circuitboard.envs:SensorStatePCB',
    kwargs={
        'rows': 5,
        'columns': 5,
        'traces': 1,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)

register(
    id='premade-v2',
    entry_point='gym_circuitboard.envs:SensorStatePremadePCB',
    kwargs={
        'file_path': None,
        'view_window': np.array([7, 7]),
        'max_steps': 50
    }
)
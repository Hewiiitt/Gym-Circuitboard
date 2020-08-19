import os

import copy

import numpy as np

from noise import snoise2

FAIL_OUT_COUNT = 20


def load_premade_env(file_path, padding):

    if os.path.exists(file_path) is False:
        raise FileNotFoundError()

    tmp = np.genfromtxt(file_path, delimiter=',', dtype=np.int)

    board = np.zeros((tmp.shape[0] + 2 * padding[1], tmp.shape[1] + 2 * padding[0])) + 1
    board[padding[1]:-padding[1], padding[0]:-padding[0]] = tmp

    goal_info = []
    for i in range(2, 1000000):
        trace_points = np.argwhere(board == i)
        if len(trace_points) == 0: break
        if len(trace_points) > 2:
            raise Exception("A trace must only have 2 points, a start and an end")

        if len(trace_points) == 1:
            goal = trace_points[0]
            goal[0], goal[1] = goal[1], goal[0]
            empty_spaces = np.argwhere(board == 0)
            available_inits = empty_spaces
            goal_info.append((goal, available_inits))
            board[goal[1], goal[0]] = 0

        else:
            goal = trace_points[0]
            goal[0], goal[1] = goal[1], goal[0]
            start = trace_points[1]
            start[0], start[1] = start[1], start[0]
            available_inits = [start]
            goal_info.append((goal, available_inits))
            board[goal[1], goal[0]] = 0
            board[start[1], start[0]] = 0

    return board, goal_info


def generate_pre_made_env():

    board = np.zeros((7 + 2 * 3, 7 + 2 * 3)) + 1

    board[3:-3, 3:-3] = np.array([
        np.array([0, 0, 0, 0, 1, 0, 1]),
        np.array([0, 2, 0, 0, 0, 0, 0]),
        np.array([0, 0, 0, 1, 0, 1, 1]),
        np.array([0, 0, 0, 0, 0, 0, 0]),
        np.array([0, 0, 1, 0, 0, 0, 0]),
        np.array([1, 0, 0, 0, 0, 2, 0]),
        np.array([1, 1, 0, 0, 0, 0, 0])
    ])

    traced_board = copy.deepcopy(board)
    empty_spaces = np.argwhere(board == 0)
    starts = [
        np.array([4, 4]),
        np.array([8, 8])
    ]

    return board, empty_spaces, starts

def generate_empty_baord(rng, columns, rows, traces, padding):
    board = None
    valid_baord = False
    attempt = 0
    #
    while not valid_baord and attempt < FAIL_OUT_COUNT:

        board = np.zeros((columns + 2 * padding[0], rows + 2 * padding[1])) + 1
        board[padding[0]:-padding[0], padding[1]:-padding[1]] = generate_noise(columns, rows)
        # board[3:-3, 3:-3] = np.array(
        #     [np.array([0, 0, 0, 0, 0]),
        #     np.array([0, 0, 0, 0, 0]),
        #     np.array([0, 0, 1, 0, 0]),
        #     np.array([1, 0, 1, 1, 1]),
        #     np.array([0, 0, 1, 0, 0])]
        # )
        traced_board = copy.deepcopy(board)
        empty_spaces = np.argwhere(board == 0)
        idx = np.linspace(0, len(empty_spaces) - 1, len(empty_spaces), dtype=int)
        start_points = rng.choice(idx, size=traces, replace=False)
        traced = True

        start = [empty_spaces[start_points[i]] for i in range(len(start_points))]
        # start = np.array([6, 3])
        # available_positions = recursive_search((start[0], start[1]), board, [])

        start_positions = [(start[i], recursive_search((start[i][0], start[i][1]), board, [])) for i in range(len(start))]

        valid_baord = True

        for i in range(len(start_positions)):

            if len(start_positions[i][1]) < 1:
                valid_baord = False
                break

            start_positions[i][1].remove(tuple(start_positions[0][0]))

            board[start_positions[i][0][1], start_positions[i][0][0]] = 2

    # cmap = colors.ListedColormap(['white', 'black', 'yellow', 'blue'])
    # bounds = [0, 1, 2, 3, 4]
    # norm = colors.BoundaryNorm(bounds, cmap.N)
    #
    # f, axarr = plt.subplots(2, 1)
    # axarr[0].imshow(board, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
    # axarr[1].imshow(traced_board, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
    # plt.show()
    #
    #     if traced:
    #         valid_baord = True
    #     else:
    #         attempt += 1
    #
    # if attempt >= FAIL_OUT_COUNT:
    #     raise Exception('Unable to create valid environment with selected '
    #                     'parms:\n\tcols:{}\trows:{}\ttraces')

    return board, start_positions


def recursive_search(current_pos, grid, accessible_nodes):
    x, y = current_pos

    if current_pos in accessible_nodes or x < 0 or x > grid.shape[1]-1 or y < 0 or y > grid.shape[0]-1:
        return accessible_nodes

    if grid[y, x] == 0:
        accessible_nodes.append(current_pos)
    else:
        return accessible_nodes

    accessible_nodes = recursive_search((x-1, y), grid, accessible_nodes)
    accessible_nodes = recursive_search((x+1, y), grid, accessible_nodes)
    accessible_nodes = recursive_search((x, y-1), grid, accessible_nodes)
    accessible_nodes = recursive_search((x, y+1), grid, accessible_nodes)

    return accessible_nodes


def generate_new_environment(rng, columns, rows, num_traces):

    board = None
    valid_baord = False
    attempt = 0

    while not valid_baord and attempt < FAIL_OUT_COUNT:

        board = generate_noise(columns, rows)
        traced_board = copy.deepcopy(board)
        empty_spaces = np.argwhere(board != 0)
        idx = np.linspace(0, len(empty_spaces) - 1, len(empty_spaces), dtype=int)
        start_points = rng.choice(idx, size=num_traces, replace=False)
        traced = True

        for i in range(len(start_points)):
            start = empty_spaces[start_points[i]]
            depth = rng.randint(6, 10)
            traced_board[start[0], start[1]] = i + 2
            completed_trace, traced_board, end = recusivley_trace_route(rng, start, traced_board, start, depth, i + 2)

            if not completed_trace:
                traced = False
                break
            traced_board[end[0], end[1]] = i + 2

            board[start[0], start[1]] = i + 2
            board[end[0], end[1]] = i + 2

        if traced:
            valid_baord = True
        else:
            attempt += 1

    if attempt >= FAIL_OUT_COUNT:
        raise Exception('Unable to create valid environment with selected '
                        'parms:\n\tcols:{}\trows:{}\ttraces:{}'
                        .format(columns, rows, num_traces))

    # print(traced_board)
    #
    #
    # plt.figure()
    # f, axarr = plt.subplots(1, 2)
    # axarr[0].imshow(board)
    # axarr[1].imshow(traced_board)
    # plt.show()

    return board


def generate_noise(width, height, freq=3, octave=1, threshold=0.5):
    arr = np.zeros((width*3, height*3))

    for y in range(height*3):
        for x in range(width*3):
            z = snoise2(x / freq, y / freq, octave)
            arr[x, y] = z > threshold

    return arr[width:width*2, height:height*2]

def recusivley_trace_route(rng, start, traced_board, location, depth_left, id):

    if depth_left > 0:
        available_actions = get_available_actions(traced_board, location)
        if len(available_actions) < 1:
            return False, traced_board, None
        dst_weighted_p = [np.linalg.norm(a-start) for a in available_actions]
        norm_probs = dst_weighted_p / np.linalg.norm(dst_weighted_p, ord=1)
        idx = np.linspace(0, len(available_actions) - 1, len(available_actions), dtype=int)
        i = rng.choice(idx, 1, p=norm_probs)
        action = available_actions[i[0]]
        traced_board[action[0], action[1]] = id

        return recusivley_trace_route(rng, start, traced_board, action, depth_left - 1, id)
    else:
        return True, traced_board, location


def get_available_actions(traced_board, location):

    available = []

    l_x = location[0]
    l_y = location[1]

    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x == y == 0:
                continue

            loc_x = l_x + x
            loc_y = l_y + y
            if 0 < loc_x < traced_board.shape[0] and 0 < loc_y < traced_board.shape[1]:
                if np.abs(x) == np.abs(y) == 1:
                    if traced_board[x, y] == 0:
                        if traced_board[l_x + x, l_y + 0] == 0 and traced_board[l_x + 0, l_y + y] == 0:
                            available.append([loc_x, loc_y])
                else:
                    if traced_board[loc_x, loc_y] == 0:
                        available.append([loc_x, loc_y])

    return available
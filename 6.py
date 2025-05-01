import heapq
import copy
class PuzzleNode:
  def __init__(self, state, parent=None, move=None, g=0, h=0):
      self.state = state
      self.parent = parent
      self.move = move
      self.g = g
      self.h = h
      self.f = g + h

  def __lt__(self, other):
      return self.h < other.h
def print_state(node):
    state = node.state
    g_str = f"g={node.g}"
    h_str = f"h={node.h}"
    f_str = f"f={node.f}"

    value_lines = [g_str, h_str, f_str]

    for i, row in enumerate(state):
        row_str = " ".join(str(num) if num != 0 else " " for num in row)
        value_display = value_lines[i] if i < len(value_lines) else ""
        print(f"{row_str}   {value_display}")

    print("-" * 15)
def print_states_with_values(nodes):
    states = [node.state for node in nodes]
    moves = [node.move if node.move else "Start" for node in nodes]
    g_values = [f"g={node.g}" for node in nodes]
    h_values = [f"h={node.h}" for node in nodes]
    f_values = [f"f={node.f}" for node in nodes]

    print("  ".join(f"{move:^6}" for move in moves))

    for row in range(3):
        print("   ".join(" ".join(str(num) if num != 0 else " " for num in state[row]) for state in states))

    print("     ".join(g_values))
    print("     ".join(h_values))
    print("     ".join(f_values))
    print("-" * (len(states) * 22))

def reconstruct_path(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent # backtrack to the parent node
    return path[::-1]
def heuristic_function(state, goal):
    h = 0
    for i in range(3):
        for j in range(3):
            if (goal[i][j] == '*'):
                continue
            # check if the cell doesn't match with the goal
            if state[i][j] != goal[i][j]:
                h += 1
    return h
def flatten(state):
    return tuple(sum(state, []))
def get_neighbors(state, visited):
    neighbors = []
    moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    zero_x = -1
    zero_y = -1
    # finding empty cell
    for i in range(3):
        for j in range(3):
            if state[i][j] == '*':
                zero_x, zero_y = i, j
                break

    #iterate in four direction of empty cell
    for move, (dx, dy) in moves.items():
        new_x, new_y = zero_x + dx, zero_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(state)
            new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]

            # check if the state is already visited or not
            if flatten(new_state) in visited:
                continue
            neighbors.append((new_state, move))

    return neighbors
def heuristic_search(start, goal):
    pq = [] # priority queue to give priority to lowest heuristic value state
    heapq.heappush(pq, PuzzleNode(start, None, None, 0, heuristic_function(start, goal)))
    visited = set() # a set of already visited states

    while pq:
        current_node = heapq.heappop(pq)
        print("Current State:")
        print_state(current_node)

        if current_node.state == goal: # checking if the current state is the goal state or not
            return reconstruct_path(current_node)
        visited.add(flatten(current_node.state)) # mark current state as a visited state

        #generate neighbors
        neighbors = get_neighbors(current_node.state, visited)
        neighbor_nodes = []
        for neighbor, move in neighbors:
            g = current_node.g + 1
            h = heuristic_function(neighbor, goal)
            heapq.heappush(pq, PuzzleNode(neighbor, current_node, move, g, h))
            neighbor_nodes.append(PuzzleNode(neighbor, current_node, move, g, h))

        # print neighbors
        if neighbor_nodes:
            print("Generated Neighbors:")
            print_states_with_values(neighbor_nodes)
            print('\n')
    return None
start_state = [['2', '8', '3'], ['1', '6', '4'], ['7', '*', '5']]  # initial state
goal_state = [['1', '2', '3'], ['8', '*', '4'], ['7', '6', '5']]   # Goal state

solution = heuristic_search(start_state, goal_state)
if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")
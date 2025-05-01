import heapq
class BestFirstSearch:
    def __init__(self):
        self.graph = {}
        self.heuristic = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def best_first_search(self, start, goal):
        open_list = []   # Priority queue
        close_list = []  # List to track expanded nodes
        parent = {}      # Store parent nodes to reconstruct the path
        heapq.heappush(open_list, (self.heuristic[start], start))
        parent[start] = None

        print(f"Initialization:")
        print(f"Open List: {[node for _, node in open_list]}")
        print(f"Close List: {close_list}\n")

        while open_list:
            _, current = heapq.heappop(open_list)
            close_list.append(current)

            print(f"Expanding Node: {current}")
            print(f"Close List: {close_list}")

            if current == goal:
                print("\nGoal Reached!")
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                print(f"Final Path: {' → '.join(path)}")
                return

            for neighbor in self.graph.get(current, []):
                if neighbor not in close_list:
                    # Check if the neighbor is already in the open list
                    if not any(n[1] == neighbor for n in open_list):
                        heapq.heappush(open_list, (self.heuristic[neighbor], neighbor))
                        parent[neighbor] = current

            # Sort open list by heuristic to ensure priority queue order
            open_list.sort(key=lambda x: x[0])

            print(f"Open List: {[node for _, node in open_list]}\n")

        print("Goal not reachable.")
if __name__ == "__main__":
    bfs = BestFirstSearch()

    # Adding edges
    bfs.add_edge('S', 'A')
    bfs.add_edge('S', 'B')
    bfs.add_edge('A', 'C')
    bfs.add_edge('A', 'D')
    bfs.add_edge('B', 'E')
    bfs.add_edge('B', 'F')
    bfs.add_edge('E', 'H')
    bfs.add_edge('E', 'I')
    bfs.add_edge('F', 'G')  # Goal node

    # Setting heuristic values
    heuristic_values = {
        'S': 14, 'A': 12, 'B': 5, 'C': 7, 'D': 3, 'E': 8,
        'F': 2, 'H': 4, 'I': 9, 'G': 0
    }
    bfs.set_heuristic(heuristic_values)

    # Running Best-First Search
    bfs.best_first_search('S', 'G')
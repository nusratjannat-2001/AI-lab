import heapq
class Graph:
    def __init__(self):
        self.graph = {}
    # Adding edges
    def add_edge(self, u, v, cost):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, cost))

    # A* Search Algorithm
    def a_star_search(self, start, goal, heuristic):
        pq = []

        # (f(n) = g(n) + h(n), g(n), node)
        heapq.heappush(pq, (heuristic[start], 0, start))

        g_costs = {start: 0}  # storing the actual costs (g(n))
        parent = {start: None}  # tracking the shortest path

        while pq:
            # Taking the node with the lowest f(n)
            f_cost, g_cost, node = heapq.heappop(pq)
            if node == goal:
                path = []
                while node:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                print("Shortest Path:", " -> ".join(path))
                print("Total Cost:", g_costs[goal])
                return

            for neighbor, edge_cost in self.graph.get(node, []):
                new_g_cost = g_cost + edge_cost

                # If new g(n) is better then the current or neighbor is not yet visited
                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    f_cost = new_g_cost + heuristic[neighbor]
                    heapq.heappush(pq, (f_cost, new_g_cost, neighbor))
                    parent[neighbor] = node

        print("No path found from", start, "to", goal) # If the goal is unreachable
# Creating the graph
graph = Graph()

# Static Input for edges
edges = [
    ("S", "A", 1),
    ("S", "G", 10),
    ("A", "C", 1),
    ("A", "B", 2),
    ("C", "D", 3),
    ("C", "G", 4),
    ("B", "D", 5),
    ("D", "G", 2)
]

# Adding edges
for u, v, cost in edges:
    graph.add_edge(u, v, cost)

# Given heuristic values
heuristic = {
    "S": 5,
    "A": 3,
    "B": 4,
    "C": 2,
    "D": 6,
    "G": 0
}

# Start and goal nodes
start = "S"
goal = "G"

print("Start of Searching " + start)
print("Goal of Searching " + goal)
print("\nExecuting A* Search...")
graph.a_star_search(start, goal, heuristic)

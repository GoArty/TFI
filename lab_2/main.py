import random
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class FiniteAutomaton:
    def __init__(self):
        self.states = {}
        self.initial_state = None
        self.final_states = []
        self.alphabet = {'L', 'R'}

    def add_transition(self, from_state, to_state, label):
        if from_state not in self.states:
            self.states[from_state] = {}
        self.states[from_state][label] = to_state

    def set_initial_state(self, state):
        self.initial_state = state

    def add_final_state(self, state):
        self.final_states.append(state)

    def check_path(self, path):
        current_state = self.initial_state
        for step in path:
            if step not in self.alphabet or current_state not in self.states or step not in self.states[current_state]:
                return False
            current_state = self.states[current_state][step]
        print(current_state+1)
        return current_state in self.final_states

def read_parameters(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        max_branchings = int(lines[0].strip())
        exits = int(lines[1].strip())
    return max_branchings, exits

class GraphGenerator:
    def __init__(self, max_depth, num_exits):
        self.max_depth = max_depth
        self.num_exits = num_exits
        self.edges = []
        self.vertices = ["A"]
        self.current_vertex_id = 0
        self.exits_created = 0

    def generate(self):
        self._create_tree("A", 0)
        return self.edges

    def _create_tree(self, current_vertex, depth):

        if depth >= self.max_depth:
            return
        if self.exits_created > self.num_exits:
            return
        
        left_child = self._get_next_vertex()
        right_child = self._get_next_vertex()

        self.edges.append((current_vertex, left_child))
        self.edges.append((current_vertex, right_child))
        
        if random.random() < 0.5:
            self._create_tree(left_child, depth + 1)
        else:
            self.exits_created += 1
            self.edges.append((left_child, left_child)) 
           
            
        if random.random() < 0.5:
            self._create_tree(right_child, depth + 1)
        else:
            self.exits_created += 1 
            self.edges.append((right_child, right_child))   

    def _get_next_vertex(self):
        self.current_vertex_id += 1
        new_vertex = chr(ord('A') + self.current_vertex_id)
        self.vertices.append(new_vertex)
        return new_vertex

def graph_to_automaton(edges):
    fa = FiniteAutomaton()
    state_map = {}
    state_counter = 0

    fa.set_initial_state(state_counter)
    state_map['A'] = state_counter
    state_counter += 1

    queue = deque(['A'])
    while queue:
        current_vertex = queue.popleft()
        current_state = state_map[current_vertex]

        for edge in edges:
            if edge[0] == current_vertex:
                if edge[1] not in state_map:
                    state_map[edge[1]] = state_counter
                    state_counter += 1
                    queue.append(edge[1])

                if edge[1] == chr(ord(current_vertex) + 1):
                    fa.add_transition(current_state, state_map[edge[1]], 'R')
                elif edge[1] == chr(ord(current_vertex) + 2):
                    fa.add_transition(current_state, state_map[edge[1]], 'L')

                if edge[0] == edge[1]:
                    print(edge[0])
                    fa.add_final_state(state_map[edge[1]])
    return fa

if __name__ == "__main__":
    max_branchings, exits = read_parameters('parameters.txt')

    generator = GraphGenerator(max_branchings, exits)
    edges = generator.generate()
    while generator.exits_created < 1: 
        generator = GraphGenerator(max_branchings, exits)
        edges = generator.generate()

    fa = graph_to_automaton(edges)

    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)  
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=20)
    nx.draw_networkx_edges(G, pos, width=2)
    plt.axis("off")  
    plt.savefig('graf.png',bbox_inches='tight', pad_inches=0)  
    
    print(edges)
    print(generator.vertices)
    print(generator.exits_created)

    while(True):
        test_path = input("Enter a path (sequence of L and R)(example: lrlr): ").upper()
        result = fa.check_path(test_path)
        print(f"The path {'belongs' if result else 'does not belong'} to the language.")

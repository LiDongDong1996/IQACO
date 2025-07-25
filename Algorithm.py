import copy
import numpy as np

class Ant:
    def __init__(self, start, end, max_step, q_importance) -> None:
        self.max_step = max_step  # Maximum steps the ant can take
        self.q_importance = q_importance  # Importance coefficient for Q values
        self.start = start  # Starting position [y, x] = [0, 0], y first due to list indexing
        self.destination = end  # Default destination node (redefined in run method)
        self.successful = True  # Flag indicating if ant reached destination
        self.path_record = [start]  # Record of path nodes
        self.greedy = True if np.random.rand() < (1 - q_importance) else False

    def run(self, map_data, q_data):
        self.position = copy.deepcopy(self.start)
        # Step 1: Continuously find the next node until reaching destination or exhausting steps
        for _ in range(self.max_step):
            result = self.select_next_node(map_data, q_data)
            if result is False:
                self.successful = False
                break
            else:
                if self.position == self.destination:
                    break
        else:
            self.successful = False

    def select_next_node(self, map_data, q_data):
        '''
        Function:
        ---------
        Selects the next node, updates self.position, and returns a status (True/False) indicating success.
        '''
        y_1 = self.position[0]
        x_1 = self.position[1]
        # Step 1: Calculate theoretical surrounding nodes
        nodes_to_select = [
            [y_1-1, x_1-1], [y_1-1, x_1], [y_1-1, x_1+1],  # Upper layer
            [y_1, x_1-1],                 [y_1, x_1+1],    # Same layer
            [y_1+1, x_1-1], [y_1+1, x_1], [y_1+1, x_1+1],  # Lower layer
        ]
        # Step 2: Filter out invalid or obstacle nodes
        valid_nodes = []
        for node in nodes_to_select:
            if node[0] < 0 or node[1] < 0:
                continue
            if node[0] >= len(map_data) or node[1] >= len(map_data):
                continue
            if map_data[node[0]][node[1]] == 0:
                valid_nodes.append(node)
        if not valid_nodes:  # If no valid nodes, terminate selection
            return False
        if self.destination in valid_nodes:  # If next to destination, select it
            self.position = self.destination
            self.path_record.append(copy.deepcopy(self.position))
            map_data[self.position[0]][self.position[1]] = 1
            return True
        # Step 3: Calculate distances to destination for heuristic factor
        distances = []  # Distance heuristic factor
        for node in valid_nodes:
            dist = ((self.destination[0] - node[0])**2 + (self.destination[1] - node[1])**2)**0.5
            distances.append(dist)
        # Step 3.1: Invert distances
        for j in range(len(distances)):
            distances[j] = 1 / distances[j]

        # Step 4: Calculate selection probabilities
        probabilities = []
        for i in range(len(valid_nodes)):
            p = (1 - self.q_importance) * distances[i] + self.q_importance * (1 + q_data[valid_nodes[i][0], valid_nodes[i][1]])
            probabilities.append(p)
        # Step 5: Roulette wheel selection
        if np.random.rand() < (1 - self.q_importance):
            prob_sum = sum(probabilities)
            probabilities = [p / prob_sum for p in probabilities]
            rand_key = np.random.rand()
            for k, prob in enumerate(probabilities):
                if rand_key <= prob:
                    break
                else:
                    rand_key -= prob
        else:
            k = np.array(probabilities).argmax()
        # Step 6: Update current position, record it, and mark previous position as impassable
        self.position = copy.deepcopy(valid_nodes[k])
        self.path_record.append(copy.deepcopy(self.position))
        map_data[self.position[0]][self.position[1]] = 1
        return True

class IQACO:
    def __init__(self, map_data, start=[0,0], end=[19,19], max_iter=100, ant_num=50, q_importance=0.5) -> None:
        '''
        Parameters:
        -----------
            q_importance : Importance coefficient for Q values
            start        : Starting position [y, x]
            end          : Destination position [y, x]
            max_iter     : Maximum number of iterations
            ant_num      : Number of ants
        '''
        # Step 0: Initialize parameters
        self.max_iter = max_iter  # Maximum iterations
        self.ant_num = ant_num  # Number of ants
        self.ant_params = {  # Parameters for ant initialization
            'q_importance': q_importance,
            'start': start,
            'end': end
        }
        self.map_data = map_data.copy()  # Map data
        self.map_length = self.map_data.shape[0]  # Map size, used for max steps
        self.q_data = np.zeros(shape=[self.map_length, self.map_length])  # Q matrix, initialized to 0
        self.q_data[end[0], end[1]] += 1
        self.avg_path_lengths = []  # Average path lengths per generation, for plotting
        self.best_path_lengths = []  # Best path lengths per generation, for plotting
        self.best_path_length = 999999  # Best path length found
        self.best_path_data = []  # Nodes of the best path, for visualization
        self.best_path_indices = []

    def run(self):
        # Start main iteration loop
        for i in range(self.max_iter):
            self.successful_paths = []
            print(f'Generation {i}: ', end='')
            # Step 1: Run ants for this generation
            for j in range(self.ant_num):
                self.ant_params['q_importance'] = (j + 1) / self.ant_num
                ant = Ant(
                    start=self.ant_params['start'],
                    end=self.ant_params['end'],
                    max_step=self.map_length * 3,
                    q_importance=self.ant_params['q_importance']
                )
                ant.run(map_data=self.map_data.copy(), q_data=self.q_data)
                if ant.successful:  # Record successful paths
                    self.successful_paths.append(ant.path_record)
            print(f' Successful paths: {len(self.successful_paths)}', end='')
            # Step 2: Calculate path lengths for pheromone updates
            path_lengths = []

            # Step 3: Update Q matrix
            for k, path in enumerate(self.successful_paths):
                path_lengths.append(self.calc_total_length(path))
                for j in range(len(path) - 2, -1, -1):
                    reward = 1 if j == (len(path) - 2) else 0  # Reward value
                    decay = 0.9 if np.abs(np.array(path[j]) - np.array(path[j + 1])).sum() == 1 else 0.85
                    self.q_data[path[j][0], path[j][1]] = max(
                        decay * self.q_data[path[j + 1][0], path[j + 1][1]],
                        self.q_data[path[j][0], path[j][1]]
                    )

            # Step 4: Summarize generation results
            self.avg_path_lengths.append(np.average(path_lengths))
            self.best_path_lengths.append(min(path_lengths))
            if self.best_path_length > min(path_lengths):
                idx = path_lengths.index(min(path_lengths))
                self.best_path_length = path_lengths[idx]
                self.best_path_data = copy.deepcopy(self.successful_paths[idx])
            print(f' Avg length: {np.average(path_lengths):.2f}, Best: {np.min(path_lengths):.2f}')

    def calc_total_length(self, path):
        length = 0
        for j in range(len(path) - 1):
            dist = abs(path[j][0] - path[j + 1][0]) + abs(path[j][1] - path[j + 1][1])
            if dist == 2:
                length += 1.41421  # Diagonal distance
            else:
                length += 1  # Horizontal/vertical distance
        return length


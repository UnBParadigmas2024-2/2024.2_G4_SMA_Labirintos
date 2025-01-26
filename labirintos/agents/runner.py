import mesa
from labirintos.parse_maps import Maze
from labirintos.util import to_maze_space
from labirintos.agents.enemy import EnemyAgent
from collections import deque

class RunnerAgent(mesa.Agent):
    MAX_HEALTH = 10
    PHEROMONE_STRENGTH = 1
    PHEROMONE_DECAY = 0.1
    PHEROMONE_RANGE = 20

    def __init__(self, model, maze: Maze) -> None:
        super().__init__(model)
        self.maze = maze
        self.health = self.MAX_HEALTH
        self.pheromone_strength = 0
        self.reached_exit = False

    def distance_to_exit(self):
        # Calcula a distância Manhattan até a saída
        return abs(self.pos[0] - self.maze.exit_pos[0]) + abs(self.pos[1] - self.maze.exit_pos[1])

    def bfs(self, start, goal):
        # Busca o caminho mais curto do ponto 'start' até o ponto 'goal' usando o algoritmo BFS
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            for neighbor in self.model.grid.get_neighborhood(current, moore=True, include_center=False):
                if neighbor not in visited and self.is_valid_move(neighbor):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def is_valid_move(self, pos):
        # Verifica se a posição não é uma parede
        x, y = to_maze_space(pos[0], pos[1], self.maze)
        return self.maze.data[x][y] != Maze.WALL

    def find_closest_pheromone(self):
        # Encontra o feromônio mais forte dentro do alcance e retorna a posição dele
        max_pheromone_strength = 0
        target_pos = None

        for pos, strength in self.model.pheromones.items():
            distance = abs(self.pos[0] - pos[0]) + abs(self.pos[1] - pos[1])
            if distance <= self.PHEROMONE_RANGE and strength > max_pheromone_strength:
                max_pheromone_strength = strength
                target_pos = pos
                print(f"Runner {self.unique_id} is attracted to pheromone at {target_pos} (Distance: {distance})")

        return target_pos

    def walk(self):
        # Faz o agente runner andar, liberando feromônios ou seguindo os mais fortes
        if self.pos == self.maze.exit_pos and not self.reached_exit:
            self.pheromone_strength = 10  # Libera feromônio ao chegar na saída
            print(f"Runner {self.unique_id} reached the exit and is releasing pheromones!")
            self.model.release_pheromones(self.pos, self.pheromone_strength)
            self.reached_exit = True
            return

        if self.reached_exit:
            return

        target_pos = self.find_closest_pheromone()

        if target_pos:
            path = self.bfs(self.pos, target_pos)
            if path:
                new_pos = path[1] if len(path) > 1 else self.pos
            else:
                return
        else:
            new_pos = self.pos
            while new_pos == self.pos:
                nei = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
                candidates = [n for n in nei if self.maze.data[to_maze_space(n[0], n[1], self.maze)[0]][to_maze_space(n[0], n[1], self.maze)[1]] != Maze.WALL]
                if candidates:
                    new_pos = self.model.random.choice(candidates)

        self.model.grid.move_agent(self, new_pos)

        if self.pheromone_strength > 0:
            self.model.release_pheromones(self.pos, self.pheromone_strength)

        self.pheromone_strength = max(0, self.pheromone_strength - self.PHEROMONE_DECAY)

        # Verificar se está na mesmo lugar que um inimigo e tomar dano
        agents = self.model.grid.get_cell_list_contents([new_pos])
        for a in agents:
            if isinstance(a, EnemyAgent):
                # Quantidade de dano é arbitrário. Pode mudar se quiser
                self.health -= 2
                print("Runner", self.unique_id, "took damage, H:", self.health)
                if self.health <= 0:
                    print("Runner", self.unique_id, "died. Being removed")
                    self.remove()

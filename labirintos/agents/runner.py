import mesa
from labirintos.agents.key import KeyAgent
from labirintos.parse_maps import Maze
from labirintos.util import to_maze_space
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import ExitAgent
from collections import deque
from labirintos.agents.food import FoodAgent
from mesa.space import Position

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
        self.has_key = False
        self.last_position = None
        self.active = True

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
        # Verifica se o runner possui a chave
        if not self.has_key:
            return None

        # Encontra o feromônio mais forte dentro do alcance e retorna a posição dele
        max_pheromone_strength = 0
        target_pos = None

        for pos, strength in self.model.pheromones.items():
            distance = abs(self.pos[0] - pos[0]) + abs(self.pos[1] - pos[1])
            if distance <= self.PHEROMONE_RANGE and strength > max_pheromone_strength:
                max_pheromone_strength = strength
                target_pos = pos
                print(f"Runner {self.unique_id} é atraído pelo feromônio em {target_pos} (Distância: {distance})")

        return target_pos

    def walk(self):
        if not self.active:
            return

        # Primeira prioridade: Verificar se precisamos de comida e não estamos na saída
        if self.should_seek_food() and not self.reached_exit:
            food_pos = self.find_closest_food()
            if food_pos:
                # Usa BFS para encontrar caminho até a comida
                path = self.bfs(self.pos, food_pos)
                if path and len(path) > 1:
                    new_pos = path[1]  # Próxima posição no caminho
                    print(f"Runner {self.unique_id} movendo em direção à comida em {food_pos}, próxima posição: {new_pos}")
                    self.model.grid.move_agent(self, new_pos)
                    
                    # Verifica se alcançamos a comida
                    agents = self.model.grid.get_cell_list_contents([new_pos])
                    for a in agents:
                        if isinstance(a, FoodAgent):
                            old_health = self.health
                            self.health = min(self.MAX_HEALTH, self.health + FoodAgent.HEAL_AMOUNT)
                            health_gained = self.health - old_health
                            print(f"Runner {self.unique_id} coletou comida. Saúde recuperada: {health_gained}. Nova saúde: {self.health}")
                            self.model.grid.remove_agent(a)
                    return  # Termina o turno após lidar com a comida

        # Se estivermos na saída com a chave
        if self.pos == self.maze.exit_pos and self.has_key and not self.reached_exit:
            self.pheromone_strength = 10
            print(f"Runner {self.unique_id} alcançou a saída com a chave e está liberando feromônios!")
            self.model.release_pheromones(self.pos, self.pheromone_strength)
            self.reached_exit = True
            self.model.AGENTS_OUT += 1
            return

        if self.reached_exit:
            return

        # Lógica de movimento normal
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

        # Verifica interações com outros agentes
        agents = self.model.grid.get_cell_list_contents([new_pos])
        for a in agents:
            if isinstance(a, EnemyAgent):
                self.health -= 2
                print(f"Runner {self.unique_id} tomou dano, Saúde: {self.health}")
                if self.health <= 0:
                    print(f"Runner {self.unique_id} morreu. Sendo removido")
                    self.remove()
            elif isinstance(a, KeyAgent):
                if not self.has_key:
                    self.has_key = True
                    print(f"Runner {self.unique_id} pegou a chave!")
                else:
                    print(f"Runner {self.unique_id} já possui a chave!")
            elif isinstance(a, ExitAgent):
                if self.has_key:
                    print(f"Runner {self.unique_id} saiu do labirinto!")
                else:
                    print(f"Runner {self.unique_id} precisa da chave para sair!")

    def should_seek_food(self):
        # Verifica se o agente precisa procurar comida (saúde abaixo de 50%)
        return self.health < (self.MAX_HEALTH / 2)
    
    def find_closest_food(self):
        if not self.active or not self.pos or not self.should_seek_food():
            return None
        
        print(f"Runner {self.unique_id} procurando comida. Saúde atual: {self.health}")
        
        # Procura em todo o grid
        min_distance = float('inf')
        closest_food_pos = None
        food_found = 0
        
        # Primeiro, vamos contar quantas comidas existem no grid
        for x in range(self.model.grid.width):
            for y in range(self.model.grid.height):
                cell_contents = self.model.grid.get_cell_list_contents([(x, y)])
                for agent in cell_contents:
                    if isinstance(agent, FoodAgent):
                        food_found += 1
                        distance = abs(self.pos[0] - x) + abs(self.pos[1] - y)
                        if distance < min_distance:
                            min_distance = distance
                            closest_food_pos = (x, y)
        
        print(f"Runner {self.unique_id} encontrou {food_found} comidas no total")
        
        if closest_food_pos:
            print(f"Runner {self.unique_id} encontrou comida mais próxima em {closest_food_pos}, distância: {min_distance}")
            return closest_food_pos
        else:
            print(f"Runner {self.unique_id} não encontrou nenhuma comida no labirinto")
            return None
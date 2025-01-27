import mesa
from mesa.space import Position
from labirintos.parse_maps import Maze
from labirintos.util import to_maze_space


def is_within_bounds(x: int, y: int, maze: Maze) -> bool:
    if (0 <= x < maze.width) and (0 <= y < maze.height):
        return True
    return False


class EnemyAgent(mesa.Agent):
    """
    EnemyAgent que se move pelo labirinto seguindo a trilha de feromônios deixada pelo RunnerAgent.
    """

    def __init__(self, model, maze: Maze, pos=(0, 0)) -> None:
        super().__init__(model)
        self.maze = maze
        self.pos = pos

    def find_strongest_pheromone(self):
        """
        Encontra o feromônio mais forte dentro do alcance do agente inimigo.
        """
        max_pheromone_strength = 0
        target_pos = None

        for pos, strength in self.model.pheromones.items():
            distance = abs(self.pos[0] - pos[0]) + abs(self.pos[1] - pos[1])
            if strength > max_pheromone_strength and self.is_valid_move(pos):
                max_pheromone_strength = strength
                target_pos = pos

        return target_pos

    def is_valid_move(self, pos):
        """
        Verifica se a posição é válida (não é uma parede).
        """
        x, y = to_maze_space(pos[0], pos[1], self.maze)
        return self.maze.data[x][y] != Maze.WALL and self.maze.data[x][y] != Maze.EXIT

    def bfs(self, start, goal):
        """
        Busca o caminho mais curto do ponto 'start' até o ponto 'goal' usando o algoritmo BFS.
        """
        queue = [(start, [start])]
        visited = set()

        while queue:
            current, path = queue.pop(0)
            if current == goal:
                return path

            for neighbor in self.model.grid.get_neighborhood(current, moore=True, include_center=False):
                if neighbor not in visited and self.is_valid_move(neighbor):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def walk(self):
        """
        Controla o movimento do EnemyAgent pelo labirinto.
        """
        # Encontra o feromônio mais forte na vizinhança
        target_pos = self.find_strongest_pheromone()

        if target_pos:
            # Usa BFS para encontrar o caminho até o feromônio mais forte
            path = self.bfs(self.pos, target_pos)
            if path and len(path) > 1:
                new_pos = path[1]  # Próxima posição no caminho
                print(f"Enemy {self.unique_id} movendo-se em direção ao feromônio em {target_pos}. Nova posição: {new_pos}")
                self.model.grid.move_agent(self, new_pos)
        else:
            # Movimento aleatório caso não haja feromônio
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            valid_moves = [n for n in neighbors if self.is_valid_move(n)]
            if valid_moves:
                new_pos = self.random.choice(valid_moves)
                print(f"Enemy {self.unique_id} movendo-se aleatoriamente para {new_pos}")
                self.model.grid.move_agent(self, new_pos)
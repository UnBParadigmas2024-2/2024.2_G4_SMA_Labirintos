import mesa
from mesa.space import Position

from labirintos.parse_maps import Maze


def to_maze_space(x: int, y: int, maze: Maze) -> Position:
    """Espaço do MultiGrid -> Espaço do Maze ->"""
    y = maze.height - y - 1
    x, y = y, x
    return (x, y)


def is_within_bounds(x: int, y: int, maze: Maze) -> bool:
    if (0 <= x and x < maze.width) and (0 <= y and y < maze.height):
        return True
    return False


class EnemyAgent(mesa.Agent):
    """Percorre um trajeto fixo no labirinto periodicamente,
    indo e voltando pra sempre"""

    def __init__(self, model, maze: Maze, pos=(0, 0)) -> None:
        super().__init__(model)

        self.path: list[Position] = []
        self.path_index = 0
        self.path_index_inc = +1

        self._determine_fixed_path(pos, maze)

    def _determine_fixed_path(self, initial_pos: Position, maze: Maze):
        """Essa função não cria um caminho de tamanho `max_path_length`
        obrigatoriamente. É um limite superior.

        Se algoritmo chegar num \"beco sem saída\", ele apenas termina,
        mesmo que esteja curto."""

        max_path_length = self.model.random.randint(3, 6)

        visited_positions = set(initial_pos)
        curr_pos = initial_pos
        while len(self.path) < max_path_length:
            x, y = curr_pos
            candidadates: list[Position] = []
            neighbors = [
                (x + 1, y + 0),
                (x - 1, y + 0),
                (x + 0, y + 1),
                (x + 0, y - 1),
            ]
            for n_pos in neighbors:
                x, y = n_pos
                x, y = to_maze_space(x, y, maze)
                if maze.data[x][y] != Maze.WALL:
                    if n_pos not in visited_positions:
                        candidadates.append(n_pos)
            if len(candidadates) == 0:
                print("Não tem mais vizinho que não foi visitado")
                break
            else:
                curr_pos = candidadates[0]
                visited_positions.add(curr_pos)
                self.path.append(curr_pos)

        print("Path resolvido ID", self.unique_id)
        print(self.path)

    def walk(self) -> None:
        if self.path_index == 0:
            self.path_index_inc = +1
        elif self.path_index >= len(self.path) - 1:
            self.path_index_inc = -1

        self.path_index += self.path_index_inc

        print(self.unique_id, "Index:", self.path_index)

        new_pos = self.path[self.path_index]

        self.model.grid.move_agent(self, new_pos)

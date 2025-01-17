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

        # AVISO: pra setar a posição real, deve-se usar self.model.grid.move_agent
        self.pos = pos
        self.path: list[Position] = []

        self._determine_path(maze)

    def _determine_path(self, maze: Maze):
        """Acho melhor que seja um DFS, pq imagno que o caminho fica mais
        retilíneo"""
        path_length = self.model.random.randint(3, 6)
        path_length = 5

        self._visited_positions_globally = set(self.pos)

        curr_pos = self.pos

        print("Iniciando DFS")
        self._dfs(curr_pos, maze, path_length)
        print(self.path)
        print("Finalizado DFS")
        self.path = self._reorder_to_walkable_path()
        # print("Result path", self.pos, path_length)
        print(self.path)

    def _reorder_to_walkable_path(self):
        """A intenção dessa função é fazer `self.path` ser um caminho andável,
        com as posições "ordenadas". Mas não consegui ainda."""

        def is_within_walkable_distance(p1: Position, p2: Position) -> bool:
            dx = p1[0] - p2[0]
            dy = p1[1] - p2[1]

            if abs(dx) == 0 and abs(dy) == 1:
                return True
            if abs(dx) == 1 and abs(dy) == 0:
                return True

            return False

        # Orderna por x e depois por x
        # Não é garantido. Se uma das pontas está no centro da espiral não funciona!!!
        self.path = sorted(self.path, key=lambda pos: pos[0])
        self.path = sorted(self.path, key=lambda pos: pos[1])

        curr_index = 0

        while curr_index < len(self.path):
            for j in range(curr_index + 1, len(self.path)):
                if is_within_walkable_distance(self.path[curr_index], self.path[j]):
                    self.path[curr_index], self.path[j] = (  # swap
                        self.path[j],
                        self.path[curr_index],
                    )
                    break
            curr_index += 1

        for i in range(1, len(self.path)):
            if not is_within_walkable_distance(self.path[i - 1], self.path[i]):
                print("REODENAÇÃO DE ERRADO!")
                break

        return self.path

    def _dfs(self, pos: Position, maze: Maze, max_path_length: int):
        print("One more iter at", pos)
        x, y = pos
        # Vizinhos estão em cima, embaixo, na esquerda e direita. Ignora diagonais
        neighbors = [
            (x + 1, y + 0),
            (x - 1, y + 0),
            (x + 0, y + 1),
            (x + 0, y - 1),
        ]
        self.model.random.shuffle(neighbors)

        if len(self.path) >= max_path_length:
            return

        for candidate_pos in neighbors:
            x, y = candidate_pos
            x, y = to_maze_space(x, y, maze)
            if is_within_bounds(x, y, maze):
                print(" ", candidate_pos, f"[{maze.data[x][y]}]")
                if maze.data[x][y] != Maze.WALL:
                    if candidate_pos in self._visited_positions_globally:
                        continue
                    else:
                        real_pos = candidate_pos
                        self._visited_positions_globally.add(real_pos)
                        self.path.append(real_pos)
                        pos = real_pos
                        self._dfs(real_pos, maze, max_path_length)

    def walk(self) -> None:
        '''Por enquanto, o inimigo se teletransporta mesmo. O correto é ele
        percorerr o caminho "continuamente"'''
        new_pos = self.pos
        # Ineficiente? kkk
        while new_pos == self.pos:
            new_pos = self.model.random.choice(self.path)

        self.model.grid.move_agent(self, new_pos)

import mesa

from labirintos.parse_maps import Maze
from labirintos.util import to_maze_space


class RunnerAgent(mesa.Agent):
    def __init__(self, model, maze: Maze) -> None:
        super().__init__(model)
        self.maze = maze

    def walk(self):
        new_pos = self.pos

        while new_pos == self.pos:
            nei = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )

            candidates = []
            for n in nei:
                x, y = n
                # Tem um jeito mais "mesa" de checar se tem uma parede do lado?
                x, y = to_maze_space(x, y, self.maze)
                if self.maze.data[x][y] != Maze.WALL:
                    candidates.append(n)

            new_pos = self.model.random.choice(candidates)
            break

        self.model.grid.move_agent(self, new_pos)

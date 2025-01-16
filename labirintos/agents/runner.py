import mesa

from labirintos.parse_maps import Maze


class RunnerAgent(mesa.Agent):
    def __init__(self, model, maze: Maze) -> None:
        super().__init__(model)
        self.maze = maze

    def do_thing(self):
        print('Do thing')
import mesa
from mesa.space import MultiGrid

from labirintos.parse_maps import parse_map_file, Maze
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent


class MazeModel(mesa.Model):
    def __init__(self, maze_map_path="maps/map1.txt", seed=None) -> None:
        super().__init__(seed=seed)
        
        maze = parse_map_file(maze_map_path)

        self.grid = MultiGrid(maze.width, maze.height, torus=False)

        for y, row in enumerate(maze.data):
            _y = maze.height - y - 1
            for x, _ in enumerate(row):
                if maze.data[y][x] == Maze.WALL:
                    self.grid.place_agent(WallAgent(self), (x, _y))
                elif maze.data[y][x] == Maze.EXIT:
                    self.grid.place_agent(ExitAgent(self), (x, _y))
                elif maze.data[y][x] == Maze.START:
                    # TODO: iterar sobre todos os runners e colocá-los na posição inicial: S
                    # Não precisa ser feito nesse loop. Pode ser feito em outro lugar
                    self.grid.place_agent(RunnerAgent(self, maze), (x, _y))
                elif maze.data[y][x] == Maze.START:
                    self.grid.place_agent(StartAgent(self), (x, _y))


        print("Dim", maze.width, maze.height)
        for row in maze.data:
            print("".join(row))

    def step(self) -> None:
        # self.agents_by_type[EnemyAgent].do('do_thing')
        self.agents_by_type[RunnerAgent].do('do_thing')

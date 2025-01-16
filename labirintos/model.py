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

        self.grid.place_agent(RunnerAgent(self, maze), (0, 0))

        for x, row in enumerate(maze.data):
            for y, _ in enumerate(row):
                if maze.data[x][y] == Maze.WALL:
                    self.grid.place_agent(WallAgent(self), (x, y))
                elif maze.data[x][y] == Maze.EXIT:
                    self.grid.place_agent(ExitAgent(self), (x, y))
                elif maze.data[x][y] == Maze.START:
                    self.grid.place_agent(StartAgent(self), (x, y))

        print("Dim", maze.width, maze.height)
        for row in maze.data:
            print("".join(row))

    def step(self) -> None:
        # self.agents_by_type[EnemyAgent].do('do_thing')
        self.agents_by_type[RunnerAgent].do('do_thing')

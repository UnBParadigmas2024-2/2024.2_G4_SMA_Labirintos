import mesa
from mesa.space import MultiGrid

from labirintos.parse_maps import parse_map_file
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent


class MazeModel(mesa.Model):
    def __init__(
        self, maze_map_path="maps/map1.txt", runners_count=10, seed=None
    ) -> None:
        super().__init__(seed=seed)

        # TODO: Se der errado, carregar um mapa default, válido, mas sem paredes?
        maze = parse_map_file(maze_map_path)

        self.grid = MultiGrid(maze.width, maze.height, torus=False)

        self.grid

        for pos in maze.walls:
            self.grid.place_agent(WallAgent(self), pos)

        for pos in maze.enemies:
            self.grid.place_agent(EnemyAgent(self, maze, pos), pos)

        # Os runners spawnam no start position
        for _ in range(runners_count):
            self.grid.place_agent(RunnerAgent(self, maze), maze.start_pos)

        self.grid.place_agent(StartAgent(self), maze.start_pos)

        self.grid.place_agent(ExitAgent(self), maze.exit_pos)

        # maze.print()

    def step(self) -> None:
        self.agents_by_type[EnemyAgent].do("walk")
        # self.agents_by_type[RunnerAgent].do("do_thing")

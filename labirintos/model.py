import mesa
from mesa.space import MultiGrid
from labirintos.parse_maps import parse_map_file
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent
from labirintos.agents.key import KeyAgent

class MazeModel(mesa.Model):
    def __init__(self, maze_map_path="maps/map1.txt", runners_count=10, seed=None) -> None:
        super().__init__(seed=seed)

        maze = parse_map_file(maze_map_path)
        self.grid = MultiGrid(maze.width, maze.height, torus=False)

        for pos in maze.walls:
            self.grid.place_agent(WallAgent(self), pos)

        for pos in maze.enemies:
            self.grid.place_agent(EnemyAgent(self, maze, pos), pos)

        for _ in range(runners_count):
            self.grid.place_agent(RunnerAgent(self, maze), maze.start_pos)

        self.grid.place_agent(StartAgent(self), maze.start_pos)
        self.grid.place_agent(ExitAgent(self), maze.exit_pos)

        self.grid.place_agent(KeyAgent(self), maze.key_pos)

    def step(self) -> None:
        self.agents_by_type[EnemyAgent].do("walk")
        self.agents_by_type[RunnerAgent].do("walk")
        print("#agents", len(self.agents_by_type[RunnerAgent]))

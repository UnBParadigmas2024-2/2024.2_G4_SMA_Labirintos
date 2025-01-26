import mesa
from mesa.space import MultiGrid
from labirintos.parse_maps import parse_map_file
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent

class MazeModel(mesa.Model):
    def __init__(self, maze_map_path="maps/map1.txt", runners_count=10, seed=None) -> None:
        # Inicializa o modelo, carrega o mapa e posiciona os agentes
        super().__init__(seed=seed)

        maze = parse_map_file(maze_map_path)
        self.grid = MultiGrid(maze.width, maze.height, torus=False)
        self.pheromones = {}

         # Coloca as paredes no mapa
        for pos in maze.walls:
            self.grid.place_agent(WallAgent(self), pos)

        # Coloca os inimigos no mapa
        for pos in maze.enemies:
            self.grid.place_agent(EnemyAgent(self, maze, pos), pos)

        # Coloca os runners no mapa
        for _ in range(runners_count):
            self.grid.place_agent(RunnerAgent(self, maze), maze.start_pos)

        # Coloca os agentes de início e saída no mapa
        self.grid.place_agent(StartAgent(self), maze.start_pos)
        self.grid.place_agent(ExitAgent(self), maze.exit_pos)

    def step(self) -> None:
        # Executa uma etapa do modelo, atualizando o estado de todos os agentes
        self.move_happened = False
        self.agents_by_type[EnemyAgent].do("walk")
        self.agents_by_type[RunnerAgent].do("walk")

        total_runners = len(self.agents_by_type[RunnerAgent])
        if total_runners < 8:
            self.running = False
        
        print(f"#agents {len(self.agents_by_type[RunnerAgent])}")

    def release_pheromones(self, position, strength):
        # Libera feromônios na posição especificada com a força dada
        if position not in self.pheromones:
            self.pheromones[position] = 0
        self.pheromones[position] = max(self.pheromones[position], strength)
        print(f"Released pheromone at {position} with strength {strength}")

    def get_pheromone_at(self, position):
        # Retorna a intensidade de feromônio em uma posição
        return self.pheromones.get(position, 0)

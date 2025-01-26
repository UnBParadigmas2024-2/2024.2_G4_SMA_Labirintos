import mesa

from labirintos.agents.key import KeyAgent
from labirintos.parse_maps import Maze
from labirintos.util import to_maze_space
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import ExitAgent


class RunnerAgent(mesa.Agent):
    MAX_HEALTH = 10
    has_key = False

    def __init__(self, model, maze: Maze) -> None:
        super().__init__(model)
        self.maze = maze
        self.health: int = self.MAX_HEALTH

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

        # Verificar se está na mesmo lugar que um inimigo e tomar dano
        agents = self.model.grid.get_cell_list_contents([new_pos])
        for a in agents:
            if isinstance(a, EnemyAgent):
                # Quantidade de dano é arbitrário. Pode mudar se quiser
                self.health -= 1
                print("Runner", self.unique_id, "took damage, H:", self.health)
                if self.health <= 0:
                    print("Runner", self.unique_id, "died. Being removed")
                    self.remove()
            if isinstance(a, KeyAgent):
                if not self.has_key:  
                    self.has_key = True
                    print(f"Runner {self.unique_id} pegou a chave!")  
                else:
                    print(f"Runner {self.unique_id} já possui a chave!")
            if isinstance(a, ExitAgent):
                if self.has_key:
                    print(f"Runner {self.unique_id} saiu do labirinto!")
                else:
                    print(f"Runner {self.unique_id} precisa da chave para sair!")

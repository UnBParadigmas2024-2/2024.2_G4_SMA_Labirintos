import mesa
from labirintos.agents.key import KeyAgent

class KeyCollectorAgent(mesa.Agent):
    """Agente que coleta a chave e atualiza a posição da chave"""
    def __init__(self, model):
        super().__init__(model=model)
        self.model = model  # Armazene o modelo

    def walk(self):
        # Movimenta o agente para uma posição aleatória adjacente
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

        # Escolhe uma posição válida que não seja uma parede ou já tenha chave
        valid_steps = [step for step in possible_steps if self.model.grid.is_cell_empty(step) or 
                       any(isinstance(agent, KeyAgent) for agent in self.model.grid.get_cell_list_contents([step]))]

        if not valid_steps:
            return

        new_position = self.random.choice(valid_steps)

        # Verifica se há uma chave na nova posição
        agents = self.model.grid.get_cell_list_contents([new_position])
        for agent in agents:
            if isinstance(agent, KeyAgent):  # Verifica se o agente é a chave
                # Reposiciona a chave para um novo local
                print(f"Agente {self.unique_id} encontrou a chave!")
                self.model.reposition_key(agent)  # Reposiciona a chave

        # Move o agente para a nova posição
        self.model.grid.move_agent(self, new_position)

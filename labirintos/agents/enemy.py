import mesa


class EnemyAgent(mesa.Model):
    def __init__(self, seed=None) -> None:
        super().__init__(seed=seed)
    
    def step(self) -> None:
        ...

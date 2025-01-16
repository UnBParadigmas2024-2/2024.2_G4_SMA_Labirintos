import mesa


class RunnerAgent(mesa.Model):
    def __init__(self, seed=None) -> None:
        super().__init__(seed=seed)

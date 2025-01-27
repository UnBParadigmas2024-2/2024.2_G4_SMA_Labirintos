import mesa

class FoodAgent(mesa.Agent):
    """representa saude que pode recuperar vida do runner"""
    HEAL_AMOUNT = 3  # quantidade de saude a ser restorado
    
    def __init__(self, model):
        super().__init__(model)
        self.type = "food"  
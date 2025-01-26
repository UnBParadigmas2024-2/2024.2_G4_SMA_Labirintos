import mesa
from mesa.visualization import SolaraViz, make_space_component
from labirintos.model import MazeModel
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent
from labirintos.agents.key import KeyAgent
from labirintos.agents.food import FoodAgent


def agent_portrayal(agent: mesa.Agent):
    if agent is None:
        return

    p = {"size": 120, "marker": "s"}  # Base inicial para os agentes

    if isinstance(agent, RunnerAgent):
        health_percent = agent.health / RunnerAgent.MAX_HEALTH
        if health_percent == 1.0:
            p["color"] = "#15ff22"  
        elif health_percent > 0.7:
            p["color"] = "#c0e996"  
        elif health_percent > 0.4:
            p["color"] = "#f3fb4c"  
        elif health_percent <= 0:
            p["color"] = "#ffffff"  
        p["size"] = 35  
        p["marker"] = "o"
    elif isinstance(agent, EnemyAgent):
        p["color"] = "#F44336"  
        p["size"] = 50
        p["marker"] = "X"  
    elif isinstance(agent, StartAgent):
        p["color"] = "#00BCD4" 
        p["marker"] = "o"  
    elif isinstance(agent, ExitAgent):
        p["color"] = "#3F51B5"  
        p["marker"] = "o"
    elif isinstance(agent, KeyAgent):
        p["color"] = "#FFC107" 
        p["marker"] = "P"  
        p["size"] = 50  
    elif isinstance(agent, WallAgent):
        p["color"] = "#000000"  
        p["marker"] = "s"  
    elif isinstance(agent, FoodAgent):
        p["color"] = "#4CAF50"  
        p["marker"] = "h"  
        p["size"] = 90

    return p

def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


model_params = {
    "maze_map_path": {
        "type": "InputText",  
        "value": "maps/map1.txt",
        "label": "Caminho do arquivo do mapa",
        "disabled": True,
    },
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
}

SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process, draw_grid=False
)

model = MazeModel()

page = SolaraViz(
    model, components=[SpaceGraph], model_params=model_params, name="Labirintos"
)

page

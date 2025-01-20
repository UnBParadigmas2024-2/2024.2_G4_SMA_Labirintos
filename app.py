import mesa
from labirintos.model import MazeModel
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.enemy import EnemyAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent

from mesa.visualization import SolaraViz, make_space_component


def agent_portrayal(agent: mesa.Agent):
    if agent is None:
        return

    p = {"size": 120, "marker": "s"}

    if isinstance(agent, RunnerAgent):
        health_percent = agent.health / RunnerAgent.MAX_HEALTH
        p["color"] = "#00ff00FF"
        if health_percent == 1.0:
            p["color"] = "#00ff00FF"
        elif health_percent > 0.7:
            p["color"] = "#00ff0099"
        elif health_percent > 0.4:
            p["color"] = "#00ff0033"
        elif health_percent <= 0:
            p["color"] = "white"
        p["size"] = 40
    elif isinstance(agent, EnemyAgent):
        p["color"] = "red"
        p["size"] = 40
    elif isinstance(agent, StartAgent):
        p["color"] = "cyan"  # Temporário, melhor achar outra cor
    elif isinstance(agent, ExitAgent):
        p["color"] = "blue"
    elif isinstance(agent, WallAgent):
        p["color"] = "black"

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
    },
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
}

model = MazeModel()

SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process, draw_grid=False
)

page = SolaraViz(
    model, components=[SpaceGraph], model_params=model_params, name="Labirintos"
)

page

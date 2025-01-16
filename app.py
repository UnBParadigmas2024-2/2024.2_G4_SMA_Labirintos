import mesa
from labirintos.model import MazeModel
from labirintos.agents.runner import RunnerAgent
from labirintos.agents.static_agents import WallAgent, ExitAgent, StartAgent

from mesa.visualization import SolaraViz, make_space_component


def agent_portrayal(agent: mesa.Agent):
    if agent is None:
        return

    p = {"size": 120, "marker": "s"}

    if isinstance(agent, RunnerAgent):
        p["color"] = "green"
    elif isinstance(agent, StartAgent):
        p["color"] = "cyan"
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
    # Adianta? Tem como recriar o modelo passando um mapa diferente?
    # O modelo pode acessar esses parâmetros depois? Sim é possível
    "map_path": {
        'type': 'InputText',
        'value': 'maps/map1.txt',
        'label': 'Caminho do arquivo do mapa'
    },
    # "seed": {
    #     "type": "InputText",
    #     "value": 42,
    #     "label": "Random Seed",
    # },
}

model = MazeModel()

SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process, draw_grid=False
)

page = SolaraViz(
    model, components=[SpaceGraph], model_params=model_params, name="Labirintos"
)

page

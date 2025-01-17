from mesa.space import Position
from labirintos.parse_maps import Maze


def to_maze_space(x: int, y: int, maze: Maze) -> Position:
    """Espaço do MultiGrid -> Espaço do Maze ->"""
    y = maze.height - y - 1
    x, y = y, x
    return (x, y)

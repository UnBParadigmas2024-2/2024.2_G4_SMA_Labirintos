from mesa.space import Position

class Maze:
    WALL = "#"
    EMPTY = " "
    EXIT = "E"
    START = "S"
    ENEMY = "N"
    KEY = "K"

    def __init__(self) -> None:
        """As posições vão ser convertidas para sistema de coordenadas do
        `MultiGrid`"""

        self.width = 0
        self.height = 0
        self.data = []
        self.start_pos: Position = (0, 0)
        self.exit_pos: Position = (0, 0)
        self.enemies: list[Position] = []
        self.walls: list[Position] = []
        self.key_pos: Position = None

    def print(self, show_data=True):
        res = "Maze info:\n"
        res += f"M.width  {self.width}    \n"
        res += f"M.height {self.height}   \n"
        res += f"M.start  {self.start_pos}\n"
        res += f"M.exit   {self.exit_pos} \n"
        res += f"len M.data    {len(self.data)}    \n"
        res += f"len M.data[0] {len(self.data[0])} \n"

        if show_data:
            res += f"M.data[0] {(self.data[1])} \n"
            for row in self.data:
                res += "".join(row) + "\n"

        print(res)


def parse_map_file(file_path: str) -> Maze:
    with open(file_path, "r") as f:
        lines = f.readlines()

    start_count = 0
    exit_count = 0
    maze = Maze()
    map_builder: list[str] = []

    # Apenas descarta comentários no inicío do arquivo
    for line in lines:
        if line.startswith("/"):
            continue
        else:
            map_builder.append(line)

    w, h = map_builder[0].strip().split(" ")
    maze.width = int(w)
    maze.height = int(h)

    for y, line in enumerate(map_builder[1:]):
        row = []
        for x, cell in enumerate(line.strip()):
            """
            Na grade do web app, os valores de y crescem de baixo pra cima.
            `pos` está no sistema de coordenadas do `MultiGrid`, não do `maze.data`.
            """
            pos = (x, maze.height - y - 1)

            if cell == Maze.WALL:
                maze.walls.append(pos)
            elif cell == Maze.START:
                start_count += 1
                maze.start_pos = pos
            elif cell == Maze.EXIT:
                exit_count += 1
                maze.exit_pos = pos
            elif cell == Maze.ENEMY:
                maze.enemies.append(pos)
            elif cell == Maze.KEY:
                maze.key_pos = pos

            row.append(cell)

        maze.data.append(row)

    if start_count != 1:
        print("ERRO: O mapa deve ter exatamente um início")
        exit(1)
    if exit_count != 1:
        print("ERRO: O mapa deve ter exatamente uma saída")
        exit(1)


    return maze

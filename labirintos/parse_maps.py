
class Maze:
    WALL = "#"
    EMPTY = " "
    EXIT = "E"
    START = "S"

    def __init__(self, w: int, h: int, data: list[list[str]]) -> None:
        self.width = w
        self.height = h
        self.data = data




# state S_PARSING_MAZE_DATA

def parse_map_file(file_path: str) -> Maze:
    __map = []
    width = 0
    height = 0
    data: list[list[str]] = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        __map: list[str] = []
        for line in lines:
            if line.startswith("/"):  # Comentário, apenas ignore
                continue
            else:
                __map.append(line)

        w, h = __map[0].strip().split(" ")
        width = int(w)
        height = int(h)

        for line in __map[1:]:
            row = []
            for el in line.strip():
                row.append(el)
            data.append(row)

    maze = Maze(width, height, data)
    return maze



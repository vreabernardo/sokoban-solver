class Maze:
    def __init__(self, width, height, cells):
        self.width = width
        self.height = height
        self.cells = cells

    def __str__(self):
        return f"Maze (Width: {self.width}, Height: {self.height}, Cells: {len(self.cells)})"

    def find_element(self, element_type):
        for cell in self.cells:
            if cell.cell_type == element_type:
                return cell.pos
        return None

    def find_elements(self, element_type):
        elements = []
        for cell in self.cells:
            if cell.cell_type == element_type:
                elements.append(cell.pos)
        return elements


class Position:
    def __init__(self, col, line):
        self.col = col
        self.line = line

    def __str__(self):
        return f"Position(Col: {self.col}, Line: {self.line})"

    def plus(self, dir):
        return Position(self.col + dir[0], self.line + dir[1])

    def __eq__(self, other):
        return self.col == other.col and self.line == other.line


class Cell:
    def __init__(self, pos, cell_type):
        self.pos = pos
        self.cell_type = cell_type

    def __str__(self):
        return f"Cell {self.pos} - Type: {self.cell_type}"

    def __repr__(self):
        return str(self)


def char_to_cell_type(char):
    cell_types = {
        '#': 'WALL',
        '.': 'TARGET',
        'M': 'MAN',
        '@': 'MAN',
        'B': 'BOX',
        '$': 'BOX'
    }
    return cell_types.get(char, None)


def load_level(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    width = max(len(line.strip()) for line in lines)
    height = len(lines)

    cells = []

    for x, line in enumerate(lines):
        line = list(line.strip('\n'))
        for y, char in enumerate(line):
            cell_type = char_to_cell_type(char)
            if cell_type is not None:
                cells.append(Cell(Position(x, y), cell_type))

    return Maze(width=width, height=height, cells=cells)


if __name__ == "__main__":
    # Test
    sokoban_level = load_level("maps.txt")
    print(sokoban_level.cells)


    """
    sprite_coordinates = dict(sourceSize=(241, 272), UP0=(0, 1), Right0=(0, 55), Down0=(0, 109), Left0=(0, 163),
                          UPS=(40, 1), RightS=(40, 55), DownS=(40, 109), LeftS=(40, 163), UP1=(81, 1), Right1=(81, 55),
                          Down1=(81, 109), Left1=(81, 163), UP1P=(121, 1), Right1P=(121, 55), Down1P=(121, 109),
                          Left1P=(121, 163), UPPS=(160, 1), RightPS=(160, 55), DownPS=(160, 109), LeftPS=(160, 163),
                          UP0P=(200, 1), Right0P=(200, 55), Down0P=(200, 109), Left0P=(200, 163), BOX=(80, 218),
                          BoxOnTarget=(120, 218), TARGET=(0, 218), WALL=(40, 218))
    """

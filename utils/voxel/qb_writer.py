import struct

from typing import List, Dict, Tuple

class QbMatrix:
    def __init__(self, name: str, size_x, size_y, size_z, data, pos: Tuple[int, int, int]):
        self.name = name
        self.pos = pos
        self.data = data
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z

class Qb:
    def __init__(self) -> None:
        self.version: int = 0x0101
        self.colorFormat: int = 0
        self.zAxisOrientation: int = 0
        self.compressed: int = 0
        self.visibilityMaskEncoded: int = 0
        self.matrixList: List[QbMatrix] = []

    def add_matrix(self, name: str, data, pos: Tuple[int, int, int]) -> None:
        self.matrixList.append(QbMatrix(name, data, pos))

    def save(self, filename: str) -> None:
        with open(filename, "wb") as f: # type(f) = <class '_io.BufferedWriter'>
            self.compressed = 0  # Compression saving not supported

            f.write(struct.pack("I", self.version))
            f.write(struct.pack("I", self.colorFormat))
            f.write(struct.pack("I", self.zAxisOrientation))
            f.write(struct.pack("I", self.compressed))
            f.write(struct.pack("I", self.visibilityMaskEncoded))
            f.write(struct.pack("I", len(self.matrixList)))

            for matrix in self.matrixList: # QbMatrix
                self.save_matrix(f, matrix)

    def save_matrix(self, file: object, matrix: QbMatrix) -> None:
        file.write(struct.pack("B", len(matrix.name)))
        file.write(struct.pack(str(len(matrix.name.encode('ascii')))+"s", matrix.name.encode('ascii')))
        size_x = matrix.size_x
        size_y = matrix.size_y
        size_z = matrix.size_z
        file.write(struct.pack("III", size_x, size_y, size_z))
        file.write(struct.pack("iii", matrix.pos[0], matrix.pos[1], matrix.pos[2]))
        file.write(bytes([c for color in matrix.data for c in color]))

# Usage:

def test_write_qb() -> None:
    from mathutils import Color
    from typing import List, Dict, Tuple

    EMPTY_COLOR = (0, 0, 0, 0)
    data: List[List[List[Tuple[int, int, int, int]]]] = []
    colors: Dict[Tuple[int, int, int], Color] = {(-2, -1, -2): Color((0.0, 204.0, 0.0)), (-1, -1, -1): Color((0.0, 204.0, 0.0)), (-2, 0, -1): Color((0.0, 204.0, 0.0)), (-1, -1, -2): Color((0.0, 204.0, 0.0)), (-1, -1, 0): Color((204.0, 7.0, 2.0)), (0, -1, 1): Color((204.0, 7.0, 2.0)), (-2, 0, -2): Color((120.0, 116.0, 91.0)), (-1, 1, -2): Color((79.0, 77.0, 56.0)), (-1, 1, -1): Color((0.0, 204.0, 0.0)), (-1, 0, -2): Color((90.0, 86.0, 59.0)), (-1, 0, 0): Color((204.0, 7.0, 2.0)), (0, -1, -2): Color((0.0, 204.0, 0.0)), (0, -1, -1): Color((0.0, 204.0, 0.0)), (0, -1, 0): Color((204.0, 7.0, 2.0)), (0, 0, -2): Color((0.0, 204.0, 0.0)), (0, 0, -1): Color((0.0, 204.0, 0.0)), (0, 1, -2): Color((0.0, 204.0, 0.0)), (0, 0, 0): Color((204.0, 7.0, 2.0))}

    for x in range(-3, 3 + 1):
        layer: List[List[Tuple[int, int, int, int]]] = []
        for y in range(-3, 3 + 1):
            row: List[Tuple[int, int, int, int]] = []
            for z in range(-3, 3 + 1):
                color: Color = colors.get((x, y, z))
                if color:
                    row.append((int(color.r), int(color.g), int(color.b), 255))
                else:
                    row.append(EMPTY_COLOR)
            layer.append(row)
        data.append(layer)

    file: str = "C:/out.qb"
    layer: QbMatrix = QbMatrix("cube", data, (0, 0, 0))

    qb: Qb = Qb()
    qb.matrixList.append(layer)
    qb.save(file)

# test_write_qb()
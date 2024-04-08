import struct
from typing import List, Tuple

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
            self.compressed = 0  # Use 1 to set compression to RLE

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

        if self.compressed == 1:
            self.save_matrix_compressed(file, matrix) # RLE compression is slower due to more loops/write operations and besides it doesn't work in Qubicle even if they claimed it does https://getqubicle.com/qubicle/documentation/docs/file/qb/#voxel-data
        else:
            self.save_matrix_uncompressed(file, matrix)

    def save_matrix_uncompressed(self, file: object, matrix: QbMatrix) -> None:
        file.write(bytes([c for color in matrix.data for c in color]))

    def save_matrix_compressed(self, file: object, matrix: QbMatrix) -> None:
        size_x = matrix.size_x
        size_y = matrix.size_y
        size_z = matrix.size_z
        data = matrix.data

        def convert_color(color_tuple):
            return (color_tuple[0] << 24) | (color_tuple[1] << 16) | (color_tuple[2] << 8) | color_tuple[3]

        index = 0
        while index < size_x * size_y * size_z:
            count = 1
            while (index + count) < (size_x * size_y * size_z) and data[index + count] == data[index]:
                count += 1

            color_data = convert_color(data[index])
            if count > 3:
                file.write(struct.pack("I", 2))  # CODEFLAG
                file.write(struct.pack("I", count))
                file.write(struct.pack("I", color_data))
                index += count
            else:
                for _ in range(count):
                    file.write(struct.pack("I", color_data))
                    index += 1

        file.write(struct.pack("I", 6))  # NEXTSLICEFLAG


# Usage:
def test_write_qb_file():
    size_x=4
    size_y=4
    size_z=4

    colors = {
        (2, 1, 0): (140, 40, 17, 255),
        (2, 0, 3): (114, 32, 186, 255),
        (1, 1, 3): (233, 46, 88, 255),
        (1, 2, 1): (197, 99, 132, 255),
        (1, 0, 3): (228, 9, 122, 255),
        (2, 0, 2): (149, 83, 110, 255),
        (2, 2, 3): (128, 248, 166, 255),
        (2, 2, 1): (236, 131, 28, 255),
        (3, 2, 1): (13, 202, 21, 255),
        (0, 3, 0): (193, 191, 96, 255)
    }

    EMPTY_COLOR = (0, 0, 0, 0)
    data = [colors[x, y, z]
                if colors.get((x,y,z)) else EMPTY_COLOR 
                for z in range(size_z)
                for y in range(size_y)
                for x in range(size_x)]

    file: str = "C:/out.qb"
    layer: QbMatrix = QbMatrix("cube", size_x, size_y, size_z, data, (0, 0, 0))
    qb: Qb = Qb()
    qb.matrixList.append(layer)
    qb.save(file)

#test_write_qb_file()
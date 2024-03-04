import struct

class QbMatrix(object):
    def __init__(self, name, data, pos):
        self.name = name
        self.pos = pos
        self.data = data

class Qb(object):
    def __init__(self):
        self.version = 0x0101
        self.colorFormat = 0
        self.zAxisOrientation = 0
        self.compressed = 0
        self.visibilityMaskEncoded = 0
        self.matrixList = []

    def add_matrix(self, name, data, pos):
        self.matrixList.append(QbMatrix(name, data, pos))

    def save(self, filename):
        with open(filename, "wb") as f:
            self.compressed = 0  # Compression saving not supported

            f.write(struct.pack("I", self.version))
            f.write(struct.pack("I", self.colorFormat))
            f.write(struct.pack("I", self.zAxisOrientation))
            f.write(struct.pack("I", self.compressed))
            f.write(struct.pack("I", self.visibilityMaskEncoded))
            f.write(struct.pack("I", len(self.matrixList)))

            for matrix in self.matrixList:
                self.save_matrix(f, matrix)

    def save_matrix(self, file, matrix):
        file.write(struct.pack("B", len(matrix.name)))
        file.write(struct.pack(str(len(matrix.name.encode('ascii')))+"s", matrix.name.encode('ascii')))
        size_x = len(matrix.data)
        size_y = len(matrix.data[0])
        size_z = len(matrix.data[0][0])
        file.write(struct.pack("III", size_x, size_y, size_z))
        file.write(struct.pack("iii", matrix.pos[0], matrix.pos[1], matrix.pos[2]))
        for z in range(size_z):
            for y in range(size_y):
                for x in range(size_x):
                    color = matrix.data[x][y][z]
                    file.write(struct.pack("BBBB", color[0], color[1], color[2], color[3]))


# Sample Usage:

qb = Qb()

colors = [(255, 0, 0, 255),   # Red
          (0, 0, 255, 255),   # Blue
          (0, 255, 0, 255)]   # Green
data = []

for _ in range(3):
    voxel = []
    for color in colors:
        voxel.append([color])
    data.append(voxel)

file = "C:/out.qb"
qb = Qb()
layer = QbMatrix("main", data, (0, 0, 0)) # Matrix name, data as 3-dimensional array, position of matrix
qb.matrixList.append(layer)
qb.save(file)
class VoxConvertExeMissingError(Exception):
    def __init__(self, voxconvert_version):
        self.voxconvert_version = voxconvert_version
        super().__init__(f"Executable voxconvert version {voxconvert_version} missing.")

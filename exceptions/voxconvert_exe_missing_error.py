class VoxConvertExeMissingError(Exception):
    def __init__(self, voxconvert_version: str) -> None:
        self.voxconvert_version: str = voxconvert_version
        super().__init__(f"Executable voxconvert version {voxconvert_version} missing.")

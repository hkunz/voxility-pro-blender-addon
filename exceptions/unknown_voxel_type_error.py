class UnknownVoxelTypeError(Exception):
    def __init__(self, type: str) -> None:
        self.type: str = type
        super().__init__(f"Unknown voxel type: {type}")
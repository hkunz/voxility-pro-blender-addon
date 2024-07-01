class ColorReadError(Exception):
    MISSING_TEXTURE = "MISSING_TEXTURE"
    UNHANDLED = "UNHANDLED"
    
    def __init__(self, type: str) -> None:
        self.type: str = type
        if type == self.MISSING_TEXTURE:
            message = "Missing Texture!"
        elif type == self.UNHANDLED:
            message = "This error type is unhandled"
        else:
            message = f"Unknown voxel type: {type}"
        super().__init__(message)


class CommandExecutionError(Exception):
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(f"Error: Command exited with return code {returncode}")

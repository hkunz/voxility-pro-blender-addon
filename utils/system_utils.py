import platform

class SystemUtils:

    @staticmethod
    def get_architecture():
        return platform.machine()

    @staticmethod
    def is_darwin():
        return platform.system().lower() == "darwin"

    @staticmethod
    def is_darwin_x86_64():
        return platform.system().lower() == "darwin" and SystemUtils.is_x86_64()

    @staticmethod
    def is_darwin_arm64():
        return platform.system().lower() == "darwin" and SystemUtils.is_arm64()

    @staticmethod
    def is_x86_64():
        return SystemUtils.get_architecture() == 'x86_64'

    @staticmethod
    def is_arm64():
        return SystemUtils.get_architecture() == 'arm64' or platform.uname().machine == 'aarch64'
import bpy
import os

from voxelity_pro.operators.operator_generic_popup import create_generic_popup
from voxelity_pro.operators.installation.operator_script_base import OperatorScriptBase
from voxelity_pro.utils.file_utils import FileUtils

class WEB_OT_OperatorInstallMacRosetta2(OperatorScriptBase):
    bl_idname = "voxelity_pro.install_macos_rosetta2"
    bl_label = "Install Rosetta 2"
    bl_description = "Install Rosetta 2 on MacOS to be able to run x86_64 binaries on arm64 architecture"
    bl_options = {'REGISTER'}

    def draw(self, context) -> None:
        self.message = "Proceed with Rosetta 2 Installation?|This may take several minutes.,,INFO|Please wait while installation completes.,,INFO"
        self.exec_message = "Installing Rosetta 2 ... Please wait ..."
        super().draw(context)

    def get_command(self, script_path, script_args):
        return ["zsh", script_path] + list(script_args)

    def get_script_args(self):
        return []

    def get_script_path(self):
        return os.path.join(FileUtils.get_addon_root_dir(), r'scripts/installation/darwin', 'install-macos-rosetta2.zsh')

    def on_script_exit_success(self, context):
        msg = "Successfully installed Rosetta 2"
        self.report({'INFO'}, msg)
        create_generic_popup(message=f"{msg},,INFO")

    def on_script_exit_error(self, stdout, errorCode):
        self.report({'ERROR'}, stdout)
        create_generic_popup(message=f"Error installing Rosetta 2,,CANCEL,,1|Script exit with error code {str(errorCode)},,TRIA_RIGHT")

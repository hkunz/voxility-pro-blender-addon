import subprocess
import platform
import requests

from voxelity_pro.operators.operator_generic_popup import create_generic_popup, OperatorGenericPopup
from voxelity_pro.utils.ui_utils import UiUtils

class OperatorScriptBase(OperatorGenericPopup):
    bl_options = {'INTERNAL'}

    def get_architecture():
        return platform.machine()

    def is_x86_64(self):
        return self.get_architecture() == 'x86_64'

    def is_arm64(self):
        return self.get_architecture() == 'arm64' or platform.uname().machine == 'aarch64'

    def get_script_path(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_script_args(self):
        return []  # Override in subclasses to provide arguments

    def get_command(self, script_path, script_args):
        # override this function if not powershell
        return ["powershell", "-File", script_path] + list(script_args)

    def execute_script(self, context):
        try:
            script_path = self.get_script_path()
            script_args = self.get_script_args()
            command = self.get_command(script_path, script_args)
            subprocess_result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"Script {script_path} has completed normally with exit code {subprocess_result.returncode}")
            self.on_script_exit_success(context)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Script {script_path} exited prematurely with exit code {e.returncode}")
            if e.returncode >= 10:
                self.on_script_exit_error(e.stdout, e.returncode)
            else:
                self.on_script_exit_unknown(e)
        except Exception as e:
            msg = f"Unknown error occured while running subprocess"
            self.report(msg)
            create_generic_popup(message=f"{msg},,CANCEL,,1")
        return False

    def on_script_exit_success(self, context):
        msg = f"Success"
        self.report({'INFO'}, msg)
        create_generic_popup(message=f"{msg},,INFO")
        UiUtils.update_ui(context)

    def on_script_exit_error(self, stdout, errorCode):
        self.report({'ERROR'}, stdout)
        create_generic_popup(message=f"{stdout},,CANCEL,,1|Script exit with error code {str(errorCode)},,TRIA_RIGHT")

    def on_script_exit_unknown(self, e):
        self.report({'ERROR'}, str(e))
        create_generic_popup(message=f"Unknown script exit error,,CANCEL,,1|Script exit with error code {str(e.returncode)},,TRIA_RIGHT")

    def execute(self, context):
        if self.check_internet():
            #FIXME: https://blender.stackexchange.com/questions/322779/how-can-i-get-info-report-to-show-up-before-subprocess-call
            #context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Installation in progress... Please wait."), title="Info", icon='INFO')
            #context.view_layer.update()
            #bpy.app.timers.register(self.execute_script, first_interval=0.1)
            self.execute_script(context)
        else:
            self.report({'ERROR'}, f"No internet connection. Please check your internet connection!")
        return {'FINISHED'}

    def check_internet(self, url='http://www.google.com', timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    @classmethod
    def poll(cls, context):
        return True

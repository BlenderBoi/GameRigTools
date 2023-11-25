import bpy
from . import ops_scale
from .. import Preferences

modules = [ops_scale]


def menu_func(self, context):

    addon_preferences = context.preferences.addons[Preferences.addon_name].preferences
    if addon_preferences.OPERATOR_APPLYMENU_Apply_Armature_Scale:
        layout = self.layout
        layout.separator()

        row = layout.row()

        row.operator_context = "INVOKE_DEFAULT"
        row.operator("gamerigtool.apply_scale_op", text="Apply Armature Scale")


def register():
    for module in modules:
        module.register()

    bpy.types.VIEW3D_MT_object_apply.append(menu_func)


def unregister():

    bpy.types.VIEW3D_MT_object_apply.remove(menu_func)

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()

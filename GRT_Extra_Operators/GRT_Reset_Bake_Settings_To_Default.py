import bpy




class GRT_Reset_Bake_Settings_To_Default(bpy.types.Operator):
    """Reset Bake Settings To Default"""
    bl_idname = "gamerigtool.reset_bake_settings_to_default"
    bl_label = "Reset Bake Settings To Default"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scn = context.scene
        Action_Bakery = scn.GRT_Action_Bakery_Global_Settings

        Action_Bakery.Pre_Unmute_Constraint = True
        Action_Bakery.Post_Mute_Constraint = True
        Action_Bakery.BAKE_SETTINGS_Only_Selected = False
        Action_Bakery.BAKE_SETTINGS_Do_Visual_Keying = True
        Action_Bakery.BAKE_SETTINGS_Do_Constraint_Clear = False
        Action_Bakery.BAKE_SETTINGS_Do_Parent_Clear = False
        Action_Bakery.BAKE_SETTINGS_Do_Clean = False
        Action_Bakery.BAKE_SETTINGS_Do_Pose = True
        Action_Bakery.BAKE_SETTINGS_Do_Object = False


        return {'FINISHED'}




classes = [GRT_Reset_Bake_Settings_To_Default]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

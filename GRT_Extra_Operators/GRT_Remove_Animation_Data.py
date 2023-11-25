import bpy

class GRT_Remove_Animation_Data(bpy.types.Operator):
    """Remove Animation Data"""
    bl_idname = "gamerigtool.remove_animation_data"
    bl_label = "Remove Animation Data and Drivers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for object in context.selected_objects:
            if object:
                object.animation_data_clear()
                object.data.animation_data_clear()


        return {'FINISHED'}


classes = [GRT_Remove_Animation_Data]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

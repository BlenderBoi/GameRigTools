import bpy

class GRT_Remove_BBone(bpy.types.Operator):
    """Remove BBone"""
    bl_idname = "gamerigtool.remove_bbone"
    bl_label = "Remove BBone"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        for object in context.selected_objects:
            if object:
                if object.type == "ARMATURE":
                    Edit_Bones = object.data.bones
                    for bone in Edit_Bones:
                        bone.bbone_segments = 0


        return {'FINISHED'}

classes = [GRT_Remove_BBone]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

import bpy


class GRT_Remove_Bone_Shape(bpy.types.Operator):
    """Remove Bone Shape"""
    bl_idname = "gamerigtool.remove_bone_shape"
    bl_label = "Remove Bone Shape"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for object in context.selected_objects:
            if object:
                if object.type == "ARMATURE":
                    Pose_Bones = object.pose.bones
                    for bone in Pose_Bones:
                        bone.custom_shape = None


        return {'FINISHED'}

classes = [GRT_Remove_Bone_Shape]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

import bpy

class GRT_Clear_All_Bones_Constraints(bpy.types.Operator):
    """Clear All Bones Constraints"""
    bl_idname = "gamerigtool.clear_all_bones_constraints"
    bl_label = "Clear All Bones Constraints"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for object in context.selected_objects:

            if object:
                if object.type == "ARMATURE":

                    Pose_Bones = object.pose.bones

                    for bone in Pose_Bones:

                        for c in bone.constraints:
                            for constraint in bone.constraints:
                                bone.constraints.remove(constraint)

        return {'FINISHED'}






classes = [GRT_Clear_All_Bones_Constraints]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

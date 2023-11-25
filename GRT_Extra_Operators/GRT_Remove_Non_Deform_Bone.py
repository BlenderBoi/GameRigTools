
import bpy

class GRT_Remove_Non_Deform_Bone(bpy.types.Operator):
    """Remove Non Deform Bone"""
    bl_idname = "gamerigtool.remove_non_deform_bone"
    bl_label = "Remove Non Deform Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for object in context.selected_objects:

            if object:
                if object.type == "ARMATURE":

                    object = object
                    bpy.ops.object.select_all(action='DESELECT')
                    object.select_set(True)
                    context.view_layer.objects.active = object

                    bpy.ops.object.mode_set(mode = 'EDIT')
                    Edit_Bones = object.data.edit_bones
                    for bone in Edit_Bones:

                        if not bone.use_deform:
                            Edit_Bones.remove(bone)

                bpy.ops.object.mode_set(mode = 'OBJECT')


        return {'FINISHED'}


classes = [GRT_Remove_Non_Deform_Bone]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

import bpy



class GRT_Disconnect_All_Bones(bpy.types.Operator):
    """Disconnect All Bones"""
    bl_idname = "gamerigtool.disconnect_all_bones"
    bl_label = "Disconnect All Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        mode = context.mode

        for object in context.selected_objects:
            if object.type == "ARMATURE":
                armature_check = True
                bpy.context.view_layer.objects.active = object
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                break

        if armature_check:

            if mode == "OBJECT":

                for object in context.selected_objects:

                    if object.type == "ARMATURE":

                        Bones = object.data.edit_bones

                        for Bone in Bones:
                            Bone.use_connect = False

                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            if mode in ["EDIT_ARMATURE", "POSE"]:

                if mode == "POSE":
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

                for object in context.selected_objects:

                    if object.type == "ARMATURE":

                        Bones = object.data.edit_bones

                        for Bone in Bones:
                            Bone.use_connect = False
                            
                if mode == "POSE":
                    bpy.ops.object.mode_set(mode='POSE', toggle=False)


        context.view_layer.update()

        return {'FINISHED'}






classes = [GRT_Disconnect_All_Bones]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

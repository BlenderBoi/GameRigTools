import bpy




class GRT_Unlock_Bones_Transform(bpy.types.Operator):
    """Unlock Bones Transform"""
    bl_idname = "gamerigtool.unlock_bones_transform"
    bl_label = "Unlock Bones Transform"
    bl_options = {'REGISTER', 'UNDO'}

    Location: bpy.props.BoolProperty(default=True)
    Rotation: bpy.props.BoolProperty(default=True)
    Scale: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        if context.mode == "POSE":

            for object in context.selected_objects:

                if object.type == "ARMATURE":

                    Pose_Bones = object.pose.bones

                    for bone in Pose_Bones:

                        if self.Location:
                            bone.lock_location[0] = False
                            bone.lock_location[1] = False
                            bone.lock_location[2] = False
                        if self.Rotation:
                            bone.lock_scale[0] = False
                            bone.lock_scale[1] = False
                            bone.lock_scale[2] = False
                        if self.Scale:
                            bone.lock_rotation_w = False
                            bone.lock_rotation[0] = False
                            bone.lock_rotation[1] = False
                            bone.lock_rotation[2] = False

        context.view_layer.update()

        return {'FINISHED'}






classes = [GRT_Unlock_Bones_Transform]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

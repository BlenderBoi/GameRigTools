import bpy


ENUM_Scope = [("ALL","All","All"),("SELECTED","Selected","Selected")]

class GRT_Flatten_Hierarchy(bpy.types.Operator):
    """Flatten Hierarchy"""
    bl_idname = "gamerigtool.flatten_hierarchy"
    bl_label = "Flatten Hierarchy"
    bl_options = {'REGISTER', 'UNDO'}

    Scope: bpy.props.EnumProperty(items=ENUM_Scope)

    def invoke(self, context, event):
        if context.mode == "OBJECT":

            return self.execute(context)

        if context.mode in ["EDIT_ARMATURE" , "POSE"]:

            return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        mode = context.mode

        armature_check = False

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
                            Bone.parent = None

                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            if mode in ["EDIT_ARMATURE", "POSE"]:

                if mode == "POSE":
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

                for object in context.selected_objects:

                    if object.type == "ARMATURE":

                        Bones = object.data.edit_bones

                        for Bone in Bones:
                            if self.Scope == "ALL":
                                Bone.parent = None
                            if self.Scope == "SELECTED":
                                if Bone.select:
                                    Bone.parent = None
                if mode == "POSE":
                    bpy.ops.object.mode_set(mode='POSE', toggle=False)


        context.view_layer.update()

        return {'FINISHED'}






classes = [GRT_Flatten_Hierarchy]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

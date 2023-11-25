import bpy



Layer_Default = []

Layer_Default.append(True)

for layer in range(31):
    Layer_Default.append(False)

class GRT_Move_All_Bones_To_Layer(bpy.types.Operator):
    """Move All Bones to Layer"""
    bl_idname = "gamerigtool.move_all_bones_to_layer"
    bl_label = "Move All Bones to Layer"
    bl_options = {'REGISTER', 'UNDO'}

    layer: bpy.props.BoolVectorProperty(default=Layer_Default, size=32, subtype="LAYER")


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "layer", text="Layer")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        mode = context.mode

        for object in context.selected_objects:

            if object:
                if object.type == "ARMATURE":


                    for bone in object.data.bones:
                        bone.layers = self.layer
                    for bone in object.data.edit_bones:
                        bone.layers = self.layer


                    object.data.layers = self.layer


        if mode == "EDIT_ARMATURE":
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)


        context.view_layer.update()

        return {'FINISHED'}






classes = [GRT_Move_All_Bones_To_Layer]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

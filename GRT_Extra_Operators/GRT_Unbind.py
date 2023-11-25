import bpy


class GRT_Remove_Unbind(bpy.types.Operator):
    """Remove Unbind"""
    bl_idname = "gamerigtool.unbind_mesh"
    bl_label = "Clean Unbind"
    bl_options = {'REGISTER', 'UNDO'}

    Clear_Parent: bpy.props.BoolProperty(default=True, name="Clear Parent")
    Remove_Armature_Modifier: bpy.props.BoolProperty(default=True, name="Remove Armature Modifier")
    Clear_Vertex_Group: bpy.props.BoolProperty(default=True, name="Clear Vertex Group")
    Apply_Transform: bpy.props.BoolProperty(name="Apply Transform", default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Clear_Parent")
        layout.prop(self, "Remove_Armature_Modifier")
        layout.prop(self, "Clear_Vertex_Group")
        layout.prop(self, "Apply_Transform")

    @classmethod
    def poll(cls, context):
        if context.mode == "OBJECT":
            return True

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        context.view_layer.update()
        selected = [object for object in context.selected_objects]
        active = context.active_object

        selected_mesh_objects = [object for object in context.selected_objects if object.type == "MESH"]
        bpy.ops.object.select_all(action='DESELECT')

        for object in selected_mesh_objects:
            if object:
                if object.type == "MESH":
                    object.select_set(True)
                    context.view_layer.objects.active = object

                    if self.Clear_Parent:
                        if object.parent:
                            mw = object.matrix_world.copy()
                            object.parent = None
                            object.matrix_world = mw

                    if self.Remove_Armature_Modifier:

                        for i in object.modifiers:
                            for modifier in object.modifiers:
                                if modifier.type == "ARMATURE":
                                    object.modifiers.remove(modifier)

                    if self.Clear_Vertex_Group:
                        object.vertex_groups.clear()

        if self.Apply_Transform:
            if len(selected_mesh_objects) > 0:
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        bpy.ops.object.select_all(action='DESELECT')

        for obj in selected:
            obj.select_set(True)

        context.view_layer.objects.active = active

        return {'FINISHED'}

classes = [GRT_Remove_Unbind]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

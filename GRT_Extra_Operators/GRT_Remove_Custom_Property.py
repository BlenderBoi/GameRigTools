import bpy
from .. import Utility

class GRT_Remove_Custom_Property(bpy.types.Operator):
    """Remove Custom Property"""
    bl_idname = "gamerigtool.remove_custom_property"
    bl_label = "Remove Custom Property"
    bl_options = {'REGISTER', 'UNDO'}

    data: bpy.props.BoolProperty(default=True)
    object: bpy.props.BoolProperty(default=True)
    posebone: bpy.props.BoolProperty(default=True)
    editbone: bpy.props.BoolProperty(default=True)

    #Only Armature Object

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "data", text="Data")
        layout.prop(self, "object", text="Object")

        Armature_Objects = [object for object in context.selected_objects if object.type == "ARMATURE"]

        if len(Armature_Objects) > 0:

            layout.prop(self, "posebone", text="Pose Bone")
            layout.prop(self, "editbone", text="Edit Bone")



    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        object = context.object
        context.view_layer.update()


        if object:

            if self.object:

                object.id_properties_clear()

            if object.type == "ARMATURE":

                if self.data:
                    object.data.id_properties_clear()

                if self.posebone:
                    Pose_Bones = object.pose.bones
                    for bone in Pose_Bones:
                        bone.id_properties_clear()

                if self.editbone:
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')
                    object.select_set(True)
                    context.view_layer.objects.active = object

                    bpy.ops.object.mode_set(mode = 'EDIT')
                    Edit_Bones = object.data.edit_bones
                    for bone in Edit_Bones:
                        bone.id_properties_clear()

                    bpy.ops.object.mode_set(mode = 'OBJECT')

        context.view_layer.update()
        Utility.update_UI()
        return {'FINISHED'}


classes = [GRT_Remove_Custom_Property]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

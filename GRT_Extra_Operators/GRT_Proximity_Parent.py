
import bpy

import mathutils

def object_switch_mode(object, mode):

    bpy.context.view_layer.update()

    Previous_Mode = object.mode

    if not object.visible_get():

        if not bpy.context.collection.objects.get(object.name):

            bpy.context.collection.objects.link(object)



    object.hide_viewport = False
    object.hide_set(False)

    object.hide_select = False

    if object.visible_get():

        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.mode_set(mode=mode, toggle=False)

        return Previous_Mode




class BONERA_Proximity_Parent(bpy.types.Operator):
    """Parent Bone Base on Distance"""
    bl_idname = "gamerigtool.proximity_parent"
    bl_label = "Proximity Parent"
    bl_options = {'UNDO', 'REGISTER'}

    max_distance: bpy.props.FloatProperty(default=0, min=0)

    selected_as_child: bpy.props.BoolProperty(default=True)
    selected_as_parent: bpy.props.BoolProperty(default=True)



    def draw(self, context):
        layout = self.layout
        layout.prop(self, "max_distance", text="Max Distance")

        if context.mode in ["EDIT_ARMATURE", "POSE"]:
            layout.prop(self, "selected_as_child",text="Selected As Child")
            layout.prop(self, "selected_as_parent",text="Selected As Parent")


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        active_object = context.object
        current_mode = active_object.mode
        object_switch_mode(active_object, "EDIT")

        for armature in context.selected_objects:

            if armature.type == "ARMATURE":

                if current_mode in ["EDIT", "POSE"]:
                    if self.selected_as_child:
                        child_edit_bones = [bone for bone in armature.data.edit_bones if bone.select]
                    else:
                        child_edit_bones = [bone for bone in armature.data.edit_bones]

                    if self.selected_as_parent:
                        parent_edit_bones = [bone for bone in armature.data.edit_bones if bone.select]
                    else:
                        parent_edit_bones = [bone for bone in armature.data.edit_bones]

                else:
                    parent_edit_bones = [bone for bone in armature.data.edit_bones]
                    child_edit_bones = [bone for bone in armature.data.edit_bones]


                for bone in child_edit_bones:

                    if bone.parent == None:

                        parents_candidate = {}

                        for check_bone in parent_edit_bones:

                            if not bone == check_bone:
                                child_source = bone.head
                                parent_source = check_bone.tail

                                distance = mathutils.Vector(child_source - parent_source).length


                                if self.max_distance >= distance:

                                    parents_candidate[check_bone] = distance

                        if len(parents_candidate) > 0:

                            closest_bone = min(parents_candidate, key=parents_candidate.get)

                            if closest_bone:
                                distance = parents_candidate.get(closest_bone)
                                bone.parent = closest_bone






        
        object_switch_mode(armature, current_mode)

        return {'FINISHED'}


classes = [BONERA_Proximity_Parent]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

import bpy
import os
from . import Utility

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)

def draw_armature_visibility_options(self, context, layout):

    addon_preferences = context.preferences.addons[addon_name].preferences

    object = context.object


    if object:
        if object.type == "ARMATURE":

            layout = layout.box()

            if Utility.draw_subpanel(addon_preferences, addon_preferences.show_armature_display, "show_armature_display", context.object.name, layout):


                layout.prop(object.data, "display_type", text="Display As")
                layout.prop(object.data, "show_names", text="Names")
                layout.prop(object.data, "show_bone_custom_shapes", text="Shapes")
                layout.prop(object.data, "show_group_colors", text="Group Colors")
                layout.prop(object, "show_in_front", text="In Front")

                row = layout.row(align=True)

                row.prop(object.data, "show_axes", text="Show Axes")
                row.prop(object.data, "axes_position", text="Position")



#
# def draw_action_bakery(self, context, layout):
#     addon_preferences = context.preferences.addons[addon_name].preferences
#
#     scn = context.scene
#     row = layout.row(align=True)
#     row.alignment ="LEFT"
#
#     if addon_preferences.show_action_bakery:
#         row.prop(addon_preferences, "show_action_bakery", text="Action Bakery", emboss=False, icon="TRIA_DOWN")
#         layout.template_list("CGD_UL_Action_Bakery_List", "", bpy.data, "actions", scn, "action_bakery_index")
#
#         row = layout.row(align=True)
#         row.operator("cgd.check_all_for_bake", text="Select All").mode = True
#         row.operator("cgd.check_all_for_bake", text="Deselect All").mode = False
#
#         if len(bpy.data.actions) > 0:
#             active_action = bpy.data.actions[scn.action_bakery_index]
#
#             # layout.prop(active_action, "use_custom_range", text="Use Custom Range")
#             #
#             # row = layout.row(align=True)
#             #
#             # if active_action.use_custom_range:
#             #     row.prop(active_action, "custom_range_start", text="Custom Start")
#             #     row.prop(active_action, "custom_range_end", text="Custom End")
#
#             layout.prop(active_action, "loop", text="Loop")
#
#
#             layout.label(text="Bake Objects")
#             layout.prop(scn, "bake_control_armature", text="Control Armature")
#             layout.prop(scn, "bake_deform_armature", text="Deform Armature")
#
#             if not scn.bake_control_armature:
#                 layout.label(text="Control Armature Not Picked", icon="ERROR")
#
#             if not scn.bake_deform_armature:
#                 layout.label(text="Deform Armature Not Picked", icon="ERROR")
#
#
#             layout.prop(scn, "Push_to_NLA", text="Push to NLA")
#             layout.prop(scn, "Unmute_Before_Bake", text="Unmute Constraint Before Bake")
#             layout.prop(scn, "Mute_After_Bake", text="Mute Constraint After Bake")
#
#
#             if scn.bake_deform_armature and scn.bake_control_armature:
#                 layout.operator("cgd.bake_action_bakery", text="Bake Action Bakery")
#
#     else:
#         row.prop(addon_preferences, "show_action_bakery", text="Action Bakery", emboss=False, icon="TRIA_RIGHT")

def draw_panel(self, context, layout):
    addon_preferences = context.preferences.addons[addon_name].preferences

    # layout.label(text="Armature Constraint")





    # box = layout.box()
    # if Utility.draw_subpanel(context.scene.GRT_Settings, context.scene.GRT_Settings.Show_GameRigTools, "Show_GameRigTools", "Game Rig Tools", box):

    #     box.label(text="Control Rig")
    #     row = box.row(align=True)
    #     row.prop(context.scene.GRT_Settings, "ControlRig", text="", icon="ARMATURE_DATA")
    #     row.prop(context.scene.GRT_Settings, "active_to_control_rig", text="", icon="RESTRICT_SELECT_OFF")
    #     box.label(text="Game Rig")
    #     row = box.row(align=True)
    #     row.prop(context.scene.GRT_Settings, "GameRig", text="", icon="OUTLINER_OB_ARMATURE")
    #     row.prop(context.scene.GRT_Settings, "active_to_game_rig", text="", icon="RESTRICT_SELECT_OFF")

    #     box.separator()


    
    
    #     col = box.column()

    #     if not context.scene.GRT_Settings.ControlRig:
    #         col.enabled = False

    #     if not context.scene.GRT_Settings.GameRig:
    #         op = col.operator("gamerigtool.generate_game_rig", text="Generate Game Rig", icon="FILE_REFRESH")
    #         op.Use_Regenerate_Rig = False
    #         op.Use_Legacy = False
    #     else:
    #         op = col.operator("gamerigtool.generate_game_rig", text="Regenerate Game Rig", icon="FILE_REFRESH")
    #         op.Use_Regenerate_Rig = True
    #         op.Use_Legacy = False

    #     if not context.scene.GRT_Settings.ControlRig:
    #         box.label(text="Select Control Rig", icon="INFO")



    # layout.separator()

    # layout.label(text="Legacy", icon="INFO")

    #col = layout.column(align=True)
    #op = col.operator("gamerigtool.generate_game_rig", text="Generate Game Rig", icon="RESTRICT_SELECT_OFF")
    #col.scale_y = 2
    #op.Use_Regenerate_Rig = False
    #op.Use_Legacy = True

    #row = layout.row(align=True)

    #operator = row.operator("gamerigtool.toogle_constraint", text="Mute", icon="HIDE_ON")
    #operator.mute = True
    #operator.use_selected = addon_preferences.use_selected

    #operator = row.operator("gamerigtool.toogle_constraint", text="Unmute", icon="HIDE_OFF")
    #operator.mute = False
    #operator.use_selected = addon_preferences.use_selected

    #row.prop(addon_preferences, "use_selected", text="", icon="RESTRICT_SELECT_OFF")



    layout.separator()
    draw_armature_visibility_options(self, context, layout)


    # op = layout.operator("gamerigtool.generate_game_rig", text="Legacy Generate")
    # op.Use_Regenerate_Rig = False






    # if Utility.draw_subpanel(addon_preferences, addon_preferences.show_utility, "show_utility", "Utility Tools", layout):

    layout.separator()
    layout.label(text="Utility Tool", icon="MODIFIER")
    layout.operator("gamerigtool.constraint_to_armature_name", text="Constraint to Armature Name", icon="CONSTRAINT_BONE")
    layout.operator("gamerigtool.batch_rename_actions", text="Batch Rename Actions", icon="SORTALPHA")
    layout.operator("gamerigtool.flatten_hierarchy", text="Flatten Hierarchy", icon="NOCURVE")
    layout.operator("gamerigtool.disconnect_all_bones", text="Disconnect All Bones", icon="GROUP_BONE")
    layout.operator("gamerigtool.apply_scale_op", text="Apply Armature Scale", icon="CON_SIZELIMIT")
    layout.operator("gamerigtool.convert_bendy_bones_to_bones", text="Convert Bendy Bones to Bones", icon="BONE_DATA")
    layout.operator("gamerigtool.unbind_mesh", text="Unbind Mesh", icon="ARMATURE_DATA")

    layout.operator("gamerigtool.batch_rename_vertex_groups", text="Batch Rename Vertex Groups", icon="GROUP_VERTEX")

    layout.operator("gamerigtool.bake_custom_properties", text="Bake Custom Properties", icon="PROPERTIES")

    layout.operator("gamerigtool.proximity_parent", text="Proximity Parent", icon="CON_CHILDOF")


    # if Utility.draw_subpanel(addon_preferences, addon_preferences.show_cleanup, "show_cleanup", "Clean Up Tools", layout):

    layout.separator()
    layout.separator()
    layout.label(text="Clean Up Tool", icon="BRUSH_DATA")
    layout.operator("gamerigtool.unlock_bones_transform", text="Unlock Bones Transform", icon="UNLOCKED")
    layout.operator("gamerigtool.clear_all_bones_constraints", text="Clear All Bones Constraints", icon="CONSTRAINT")

    layout.operator("gamerigtool.remove_non_deform_bone", text="Remove Non Deform Bone", icon="BONE_DATA")
    layout.operator("gamerigtool.remove_animation_data", text="Remove Animation Data", icon="ACTION")
    layout.operator("gamerigtool.remove_bbone", text="Remove BBone", icon="BONE_DATA")
    layout.operator("gamerigtool.remove_bone_shape", text="Remove Bone Shapes", icon="CUBE")
    layout.operator("gamerigtool.remove_custom_property", text="Remove Custom Properties", icon="PROPERTIES")

    layout.operator("gamerigtool.move_all_bones_to_layer", text="Move All Bones to Layer", icon="SEQ_STRIP_DUPLICATE")

    # draw_action_bakery(self, context, layout)


class CGD_PT_Deform_Rig_Side_Panel(bpy.types.Panel):

    bl_label = "GRT: Utility Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Game Rig Tools"
    bl_options = {"DEFAULT_CLOSED"}



    def draw(self, context):
        layout = self.layout
        draw_panel(self, context, layout)




def POLL_Game_Armature(self, obj):
    if obj.type == "ARMATURE":
        if obj == self.ControlRig:
            return False

        return True

    else:
        return False

def POLL_Control_Armature(self, obj):
    if obj.type == "ARMATURE":
        if obj == self.GameRig:
            return False

        return True

    else:
        return False










classes = [CGD_PT_Deform_Rig_Side_Panel]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

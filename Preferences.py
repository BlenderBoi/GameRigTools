import bpy
import os
from . import Deform_Rig_Panel
from . import Utility
from . import GRT_Action_Bakery

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


def update_panel(self, context):

    addon_preferences = context.preferences.addons[addon_name].preferences
    message = ": Updating Panel locations has failed"
    try:

        if "bl_rna" in GRT_Action_Bakery.GRT_PT_Action_Bakery.__dict__:
            bpy.utils.unregister_class(GRT_Action_Bakery.GRT_PT_Action_Bakery)

        GRT_Action_Bakery.GRT_PT_Action_Bakery.bl_category = addon_preferences.action_bakery_panel_name
        bpy.utils.register_class(GRT_Action_Bakery.GRT_PT_Action_Bakery)


        if "bl_rna" in Deform_Rig_Panel.CGD_PT_Deform_Rig_Side_Panel.__dict__:
            bpy.utils.unregister_class(Deform_Rig_Panel.CGD_PT_Deform_Rig_Side_Panel)


        Deform_Rig_Panel.CGD_PT_Deform_Rig_Side_Panel.bl_category = addon_preferences.game_rig_tool_panel_name
        bpy.utils.register_class(Deform_Rig_Panel.CGD_PT_Deform_Rig_Side_Panel)




    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass



class CGD_user_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # side_panel: bpy.props.BoolProperty(default=True)
    # armature_data: bpy.props.BoolProperty(default=False)

    show_cleanup: bpy.props.BoolProperty(default=False)
    show_utility: bpy.props.BoolProperty(default=False)
    show_armature_display: bpy.props.BoolProperty(default=False)

    show_action_bakery: bpy.props.BoolProperty(default=False)
    toogle_constraints: bpy.props.BoolProperty(default=False)

    game_rig_tool_panel_name: bpy.props.StringProperty(default="Game Rig Tool", update=update_panel)
    action_bakery_panel_name: bpy.props.StringProperty(default="Game Rig Tool", update=update_panel)

    use_selected: bpy.props.BoolProperty(default=False)

    show_credits: bpy.props.BoolProperty(default=False)

    OPERATOR_APPLYMENU_Apply_Armature_Scale: bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "action_bakery_panel_name", text="Game Rig Tool Tab")
        layout.prop(self, "game_rig_tool_panel_name", text="Utility Tab")


        layout.prop(self, "toogle_constraints", text="Top Bar Toogle Constraint")

        layout.label(text="Operators Options")
        layout.prop(self, "OPERATOR_APPLYMENU_Apply_Armature_Scale", text="Apply Menu: Apply Armature Scale")


        if Utility.draw_subpanel(self, self.show_credits, "show_credits", "Credit", layout):
            box = layout.box()
            box.label(text="Author: Xin", icon="USER")

            box.label(text="Contribution: Apply armature scale", icon="ADD")
            box.label(text="Source: https://gitlab.com/x190/apply_armature_scale", icon="LINKED")


classes = [CGD_user_preferences]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    update_panel(None, bpy.context)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

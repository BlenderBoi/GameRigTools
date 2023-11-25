import bpy
from . import utils


class GRT_ScaleArmatureOperator(bpy.types.Operator):
    """Apply armature scale"""
    bl_idname = "gamerigtool.apply_scale_op"
    bl_label = "Apply Armature Scale"

    include_actions: bpy.props.EnumProperty( name = "Include actions",
                                             items = ( ('CURRENT', "Only current", ""),
                                                       ('ALL_NLA', "All in nla", ""), ),
                                             default = 'ALL_NLA' )

    scale_only_armatures: bpy.props.BoolProperty(name="Scale only armatures", default=False,
                            description="Only scale selected armatures instead of all selected objects")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.prop(self, "include_actions")
        row = layout.row()
        row.prop(self, "scale_only_armatures")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)  # width=600

    def execute(self, context):
        if not self.scale_armatures(context):
            return {'CANCELLED'}
        return {'FINISHED'}

    def scale_armatures(self, context):
        ob_types = None
        if self.scale_only_armatures:
            ob_types = set( ['ARMATURE'] )
        selected = utils.get_selected_objects(context, ob_types=ob_types)
        if len(selected) == 0:
            self.report({'ERROR'}, "No valid objects selected.")
            return False

        include_nla = (self.include_actions == 'ALL_NLA')
        tot_scaled_armatures, tot_scaled_others = utils.scale_objects(selected, include_nla, silent=False)

        if tot_scaled_armatures == 0 and tot_scaled_others == 0:
            self.report({'INFO'}, "No objects needed to be scaled.")
            return False
        self.report({'INFO'}, "{} armatures, {} other objects scaled.".format(tot_scaled_armatures, tot_scaled_others))
        return True


# class ScaleArmaturesMenu(bpy.types.Menu):
#     bl_label = "Scale Armature"
#     bl_idname = "OBJECT_MT_scale_armatures_menu"
#
#     def draw(self, context):
#         layout = self.layout
#         layout.use_property_split = True
#         layout.use_property_decorate = False
#
#         row = layout.row()
#         row.operator(ScaleArmatureOperator.bl_idname)

classes = [GRT_ScaleArmatureOperator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

import bpy
from bpy_extras import anim_utils
import os
from . import Utility

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


constraint_type = [
    ("TRANSFORM", "Copy Transform", "Copy Transforms"),
    ("LOTROT", "Copy Location & Copy Rotation", "Lot Rot"),
    ("NONE", "None (Do not Constraint)", "None"),
]
ENUM_Extract_Mode = [
    ("SELECTED", "Selected", "Selected"),
    ("DEFORM", "Deform", "Deform"),
    ("SELECTED_DEFORM", "Selected Deform", "Selected Deform"),
    ("DEFORM_AND_SELECTED", "Deform and Selected", "Deform and Selected"),
]


def get_deform(bone, bones):
    bone_name = bone.name.replace("ORG-", "DEF-")
    return bones.get(bone_name)


def find_first_def(bone, bones):
    if bone:
        if get_deform(bone, bones):
            if bone.parent:
                if bone.parent.use_deform:
                    return bone.parent


def find_deform(bone, bones):
    if not "DEF-" in bone.name:
        new_name = bone.name.replace("ORG-", "DEF-")
        return bones.get(new_name)


def get_root(bone):
    if bone.parent:
        return get_root(bone.parent)
    else:
        return bone


ENUM_Hierarchy_Mode = [
    ("KEEP_EXISTING", "Keep Existing", "Keep Existing"),
    ("RIGIFY", "Rigify Hierarchy Fix", "Rigify Hierarchy Fix"),
    ("FLAT", "Flat Hierarchy", "Flat Hierarchy"),
]


class GRT_Generate_Game_Rig(bpy.types.Operator):
    """This will Generate a Deform Game Rig based on the step in CGDive Video"""

    bl_idname = "gamerigtool.generate_game_rig"
    bl_label = "Generate Game Rig"
    bl_options = {"UNDO", "PRESET"}

    Use_Regenerate_Rig: bpy.props.BoolProperty(default=False)
    Use_Legacy: bpy.props.BoolProperty(default=False)

    Hierarchy_Mode: bpy.props.EnumProperty(
        items=ENUM_Hierarchy_Mode, default="KEEP_EXISTING"
    )

    SUB_Generation_Settings: bpy.props.BoolProperty(default=True)
    SUB_Hierarchy_Settings: bpy.props.BoolProperty(default=False)
    SUB_Constraints_Settings: bpy.props.BoolProperty(default=False)
    SUB_Extract_Settings: bpy.props.BoolProperty(default=False)
    SUB_Binding_Settings: bpy.props.BoolProperty(default=False)

    Extract_Mode: bpy.props.EnumProperty(items=ENUM_Extract_Mode, default="DEFORM")
    Copy_Root_Scale: bpy.props.BoolProperty(default=False)
    Root_Bone_Name: bpy.props.StringProperty(default="root")
    Root_Bone_Picker: bpy.props.BoolProperty(default=True)
    Auto_Find_Root: bpy.props.BoolProperty(default=False)

    Flat_Hierarchy: bpy.props.BoolProperty(default=False)
    Disconnect_Bone: bpy.props.BoolProperty(default=True)

    Constraint_Type: bpy.props.EnumProperty(items=constraint_type, default="LOTROT")

    Animator_Remove_BBone: bpy.props.BoolProperty(default=False)
    Animator_Disable_Deform: bpy.props.BoolProperty(default=False)

    Parent_To_Deform_Rig: bpy.props.BoolProperty(default=True)
    Deform_Armature_Name: bpy.props.StringProperty()
    Deform_Remove_BBone: bpy.props.BoolProperty(default=True)

    Deform_Move_Bone_to_GRT_Collection: bpy.props.BoolProperty(default=True)
    Deform_GRT_Collection_Name: bpy.props.StringProperty(default="Deform")
    Deform_Clear_Existing_Collections: bpy.props.BoolProperty(default=True)

    Deform_Set_Inherit_Rotation_True: bpy.props.BoolProperty(default=True)
    Deform_Set_Inherit_Scale_Full: bpy.props.BoolProperty(default=True)
    Deform_Set_Local_Location_True: bpy.props.BoolProperty(default=True)

    Deform_Remove_Non_Deform_Bone: bpy.props.BoolProperty(default=True)
    Deform_Unlock_Transform: bpy.props.BoolProperty(default=True)
    Deform_Remove_Shape: bpy.props.BoolProperty(default=True)
    Deform_Remove_All_Constraints: bpy.props.BoolProperty(default=True)
    Deform_Copy_Transform: bpy.props.BoolProperty(default=True)
    Deform_Bind_to_Deform_Rig: bpy.props.BoolProperty(default=True)

    Remove_Custom_Properties: bpy.props.BoolProperty(default=True)
    Remove_Animation_Data: bpy.props.BoolProperty(default=True)

    Show_Advanced: bpy.props.BoolProperty(default=False)

    Rigify_Hierarchy_Fix: bpy.props.BoolProperty(default=False)
    #    RIGIFY_Disable_Stretch: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):
        scn = context.scene
        Global_Settings = scn.GRT_Action_Bakery_Global_Settings
        Action_Bakery = scn.GRT_Action_Bakery

        control_rig = Global_Settings.Source_Armature
        deform_rig = Global_Settings.Target_Armature

        if deform_rig:
            self.Deform_Armature_Name = deform_rig.name
        elif control_rig:
            self.Deform_Armature_Name = control_rig.name + "_deform"

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        scn = context.scene

        scn = context.scene
        Global_Settings = scn.GRT_Action_Bakery_Global_Settings
        Action_Bakery = scn.GRT_Action_Bakery

        control_rig = Global_Settings.Source_Armature
        deform_rig = Global_Settings.Target_Armature

        if Utility.draw_subpanel(
            self,
            self.SUB_Generation_Settings,
            "SUB_Generation_Settings",
            "Generation Settings",
            layout,
        ):
            box = layout.box()
            box.separator()

            if self.Use_Regenerate_Rig:
                box.prop(
                    Global_Settings,
                    "Target_Armature",
                    text="Game Rig",
                    icon="ARMATURE_DATA",
                )

            else:
                box.prop(self, "Deform_Armature_Name", text="Name")

            if not self.Use_Legacy:
                box.prop(
                    self,
                    "Use_Regenerate_Rig",
                    text="Regenerate Rig",
                    icon="FILE_REFRESH",
                )
            box.separator()

        layout.separator()

        if Utility.draw_subpanel(
            self,
            self.SUB_Hierarchy_Settings,
            "SUB_Hierarchy_Settings",
            "Hierarchy Settings",
            layout,
        ):
            box = layout.box()
            box.separator()
            # layout.separator()
            # box.label(text="Hierarchy Mode")
            box.prop(self, "Hierarchy_Mode", text="")
            # layout.prop(self, "Rigify_Hierarchy_Fix", text="Rigify Hierarchy Fix (FOR RIGIFY ONLY)")
            # layout.prop(self, "Flat_Hierarchy", text="Flat Hierarchy")
            box.prop(self, "Disconnect_Bone", text="Disconnect Bones")
            box.separator()
        layout.separator()

        if Utility.draw_subpanel(
            self,
            self.SUB_Constraints_Settings,
            "SUB_Constraints_Settings",
            "Constraints Settings",
            layout,
        ):
            box = layout.box()
            box.separator()
            # box.label(text="Constraint Type:")

            box.prop(self, "Constraint_Type", text="")
            if self.Constraint_Type == "LOTROT":
                box.prop(self, "Copy_Root_Scale", text="Copy Root Scale")
                if self.Copy_Root_Scale:
                    box.prop(self, "Auto_Find_Root", text="Auto Find Root")
                    if not self.Auto_Find_Root:
                        box.label(text="Root Bone Name")
                        row = box.row(align=True)
                        if self.Root_Bone_Picker:
                            row.prop_search(
                                self,
                                "Root_Bone_Name",
                                control_rig.data,
                                "bones",
                                text="",
                            )

                        else:
                            row.prop(self, "Root_Bone_Name", text="")
                        row.prop(self, "Root_Bone_Picker", text="", icon="EYEDROPPER")
            box.separator()
        layout.separator()
        if Utility.draw_subpanel(
            self,
            self.SUB_Extract_Settings,
            "SUB_Extract_Settings",
            "Extract Settings",
            layout,
        ):
            box = layout.box()
            box.separator()
            # box.label(text="Extract Mode:")
            box.prop(self, "Extract_Mode", text="")

            box.separator()
        layout.separator()

        if Utility.draw_subpanel(
            self,
            self.SUB_Binding_Settings,
            "SUB_Binding_Settings",
            "Binding Settings",
            layout,
        ):
            box = layout.box()
            box.separator()
            box.prop(self, "Deform_Bind_to_Deform_Rig", text="Bind to Game Rig")

            if self.Deform_Bind_to_Deform_Rig:
                box.prop(
                    self, "Parent_To_Deform_Rig", text="Parent Mesh Object to Game Rig"
                )
            box.separator()

        layout.separator()

        if Utility.draw_subpanel(
            self, self.Show_Advanced, "Show_Advanced", "Advanced", layout
        ):
            box = layout.box()
            box.separator()
            box.label(text="Control Rig")
            box.prop(self, "Animator_Remove_BBone", text="Remove BBone")

            box.separator()

            box.label(text="Game Rig")

            box2 = box.box()
            box2.prop(
                self,
                "Deform_Move_Bone_to_GRT_Collection",
                text="Move Bones to Collection",
            )
            if self.Deform_Move_Bone_to_GRT_Collection:
                box2.prop(self, "Deform_GRT_Collection_Name", text="")
                box2.prop(
                    self,
                    "Deform_Clear_Existing_Collections",
                    text="Clear Existing Collections",
                )

            box.prop(self, "Deform_Remove_BBone", text="Remove BBone")

            box.prop(
                self,
                "Deform_Set_Inherit_Rotation_True",
                text="Set Inherit Rotation True",
            )
            box.prop(
                self, "Deform_Set_Inherit_Scale_Full", text="Set Inherit Scale Full"
            )
            box.prop(
                self,
                "Deform_Set_Local_Location_True",
                text="Set Local Location Bone Setting True",
            )

            box.prop(
                self,
                "Deform_Remove_Non_Deform_Bone",
                text="Remove Non Deform / Non Selected Bones",
            )

            box.prop(self, "Deform_Unlock_Transform", text="Unlock Transform")
            box.prop(self, "Deform_Remove_Shape", text="Remove Bone Shapes")
            box.prop(self, "Deform_Remove_All_Constraints", text="Remove Constraints")

            # layout.prop(self, "Deform_Copy_Transform", text="Constrain Deform Rig to Animation Rig")

            # layout.prop(self, "Deform_Bind_to_Deform_Rig", text="Bind to Deform Rig")
            # if self.Deform_Bind_to_Deform_Rig:
            #     layout.prop(self, "Parent_To_Deform_Rig", text="Parent Mesh Object to Deform Rig")

            box.prop(
                self, "Remove_Animation_Data", text="Remove Animation Data & Drivers"
            )
            box.prop(self, "Remove_Custom_Properties", text="Remove Custom Properties")
            box.separator()

    #        layout.prop(self, "RIGIFY_Disable_Stretch", text="Disable Rigify Stretch")

    def execute(self, context):
        object = context.object

        scn = context.scene
        Global_Settings = scn.GRT_Action_Bakery_Global_Settings
        Action_Bakery = scn.GRT_Action_Bakery

        control_rig = Global_Settings.Source_Armature
        deform_rig = Global_Settings.Target_Armature

        if self.Hierarchy_Mode == "KEEP_EXISTING":
            self.Rigify_Hierarchy_Fix = False
            self.Flat_Hierarchy = False
        if self.Hierarchy_Mode == "RIGIFY":
            self.Rigify_Hierarchy_Fix = True
            self.Flat_Hierarchy = False
        if self.Hierarchy_Mode == "FLAT":
            self.Rigify_Hierarchy_Fix = False
            self.Flat_Hierarchy = True

        if not self.Use_Legacy:
            # if self.Use_Regenerate_Rig:
            #     object = context.scene.GRT_Settings.ControlRig

            object = control_rig

        if object:
            if object.type == "ARMATURE":
                vis = object.hide_get()
                vis_view = object.hide_viewport

                object.hide_set(False)
                object.hide_viewport = False

                bpy.ops.object.mode_set(mode="OBJECT")

                object.hide_set(vis)
                object.hide_viewport = vis_view

                ORI_Edit_Bones = object.data.bones

                for bone in ORI_Edit_Bones:
                    if self.Animator_Remove_BBone:
                        bone.bbone_segments = 0

                #                if self.Animator_Disable_Deform:

                game_rig = None

                if not self.Use_Legacy:
                    if self.Use_Regenerate_Rig:
                        game_rig = deform_rig
                        game_rig.hide_set(False)
                        game_rig.hide_viewport = False

                if not game_rig:
                    game_rig = object.copy()
                    game_rig.name = self.Deform_Armature_Name
                    if not self.Use_Legacy:
                        Global_Settings.Target_Armature = game_rig

                game_rig.display_type = "SOLID"
                game_rig.show_in_front = True
                game_rig.data = object.data.copy()

                if not bpy.context.collection.objects.get(game_rig.name):
                    bpy.context.collection.objects.link(game_rig)

                bpy.ops.object.select_all(action="DESELECT")
                game_rig.select_set(True)
                context.view_layer.objects.active = game_rig
                bpy.ops.object.mode_set(mode="EDIT")

                Edit_Bones = game_rig.data.edit_bones

                if self.Rigify_Hierarchy_Fix:
                    for bone in Edit_Bones:
                        if bone.use_deform:
                            if bone.parent:
                                if not bone.parent.use_deform:
                                    recursive_parent = bone.parent_recursive

                                    for f in recursive_parent:
                                        if f.use_deform:
                                            bone.parent = f
                                            break
                                        else:
                                            b = find_deform(f, Edit_Bones)
                                            if b:
                                                if not b.name == bone.name:
                                                    if b.use_deform:
                                                        bone.parent = b
                                                        break

                                # if bone.name == bone.parent.name.replace("ORG-", "DEF-"):
                                #     if bone.parent.parent:
                                #         parent_bone = Edit_Bones.get(bone.parent.parent.name.replace("ORG-", "DEF-"))
                                #         bone.parent = parent_bone

                                # else:
                                #     parent_bone = Edit_Bones.get(bone.parent.name.replace("ORG-", "DEF-"))

                                #     if parent_bone:

                                #         if parent_bone.use_deform:
                                #             bone.parent = parent_bone
                                #         else:
                                #             if bone.parent.parent:
                                #                 parent_bone = Edit_Bones.get(bone.parent.parent.name.replace("ORG-", "DEF-"))
                                #                 if parent_bone:
                                #                     if parent_bone.use_deform:
                                #                         bone.parent = parent_bone

                if self.Remove_Animation_Data:
                    game_rig.animation_data_clear()
                    game_rig.data.animation_data_clear()

                    # for i, layer in enumerate(game_rig.data.layers):
                    #     if i == 0:
                    #         game_rig.data.layers[i] = True
                    #     else:
                    #         game_rig.data.layers[i] = False

                for bone in Edit_Bones:
                    if self.Flat_Hierarchy:
                        bone.parent = None
                    if self.Disconnect_Bone:
                        bone.use_connect = False

                    if self.Remove_Custom_Properties:
                        bone.id_properties_clear()
                        # if bone.get("_RNA_UI"):
                        #     for property in bone["_RNA_UI"]:
                        #         del bone[property]

                    if self.Deform_Remove_BBone:
                        bone.bbone_segments = 0

                    if self.Deform_Set_Inherit_Rotation_True:
                        bone.use_inherit_rotation = True

                    if self.Deform_Set_Local_Location_True:
                        bone.use_local_location = True

                    if self.Deform_Set_Inherit_Scale_Full:
                        bone.inherit_scale = "FULL"

                    if self.Deform_Move_Bone_to_GRT_Collection:
                        if self.Deform_Clear_Existing_Collections:
                            while len(game_rig.data.collections) > 0:
                                game_rig.data.collections.remove(
                                    game_rig.data.collections[0]
                                )

                        new_collection = game_rig.data.collections.get(
                            self.Deform_GRT_Collection_Name
                        )

                        if not new_collection:
                            new_collection = game_rig.data.collections.new(
                                self.Deform_GRT_Collection_Name
                            )

                        new_collection.assign(bone)
                        new_collection.is_visible = True

                        # for i, layer in enumerate(bone.layers):
                        #     if i == 0:
                        #         bone.layers[i] = True
                        #     else:
                        #         bone.layers[i] = False

                    if self.Deform_Remove_Non_Deform_Bone:
                        if self.Extract_Mode == "SELECTED":
                            if not bone.select:
                                Edit_Bones.remove(bone)

                        if self.Extract_Mode == "DEFORM":
                            if not bone.use_deform:
                                Edit_Bones.remove(bone)

                        if self.Extract_Mode == "SELECTED_DEFORM":
                            if not bone.select:
                                if not bone.use_deform:
                                    Edit_Bones.remove(bone)

                        if self.Extract_Mode == "DEFORM_AND_SELECTED":
                            if not bone.use_deform and not bone.select:
                                Edit_Bones.remove(bone)

                bpy.ops.object.mode_set(mode="POSE")
                game_rig.data.bones.update()

                if self.Remove_Custom_Properties:
                    # if game_rig.get("_RNA_UI"):
                    #     for property in game_rig["_RNA_UI"]:
                    #         del game_rig[property]

                    game_rig.id_properties_clear()
                    game_rig.data.id_properties_clear()
                    # if game_rig.data.get("_RNA_UI"):
                    #     for property in game_rig.data["_RNA_UI"]:
                    #         del game_rig.data[property]

                Pose_Bones = game_rig.pose.bones

                for bone in Pose_Bones:
                    if self.Remove_Custom_Properties:
                        if bone.get("_RNA_UI"):
                            for property in bone["_RNA_UI"]:
                                del bone[property]

                    if self.Deform_Remove_Shape:
                        bone.custom_shape = None

                    if self.Deform_Unlock_Transform:
                        bone.lock_location[0] = False
                        bone.lock_location[1] = False
                        bone.lock_location[2] = False

                        bone.lock_scale[0] = False
                        bone.lock_scale[1] = False
                        bone.lock_scale[2] = False

                        bone.lock_rotation_w = False
                        bone.lock_rotation[0] = False
                        bone.lock_rotation[1] = False
                        bone.lock_rotation[2] = False

                    if self.Deform_Remove_All_Constraints:
                        for constraint in bone.constraints:
                            bone.constraints.remove(constraint)

                    # if self.Deform_Copy_Transform:

                    if self.Constraint_Type == "TRANSFORM":
                        constraint = bone.constraints.new("COPY_TRANSFORMS")
                        constraint.target = object
                        constraint.subtarget = object.data.bones.get(bone.name).name

                    if self.Constraint_Type == "LOTROT":
                        constraint = bone.constraints.new("COPY_LOCATION")
                        constraint.target = object
                        constraint.subtarget = object.data.bones.get(bone.name).name

                        constraint = bone.constraints.new("COPY_ROTATION")
                        constraint.target = object
                        constraint.subtarget = object.data.bones.get(bone.name).name

                        if self.Copy_Root_Scale:
                            root = None

                            if self.Auto_Find_Root:
                                root = get_root(object.data.bones.get(bone.name))
                            else:
                                root = object.data.bones.get(self.Root_Bone_Name)

                            if root:
                                constraint = bone.constraints.new("COPY_SCALE")
                                constraint.target = object
                                constraint.subtarget = root.name

                    if self.Constraint_Type == "NONE":
                        pass

                bpy.ops.object.mode_set(mode="OBJECT")
                if self.Deform_Bind_to_Deform_Rig:
                    for obj in bpy.data.objects:
                        for modifier in obj.modifiers:
                            if modifier.type == "ARMATURE":
                                if modifier.object == object:
                                    modifier.object = game_rig
                                    if self.Parent_To_Deform_Rig:
                                        obj.parent = game_rig
                                        obj.matrix_parent_inverse = (
                                            game_rig.matrix_world.inverted()
                                        )

            for bone in object.data.bones:
                if self.Animator_Disable_Deform:
                    bone.use_deform = False

        return {"FINISHED"}


def draw_item(self, context):
    layout = self.layout
    row = layout.row(align=True)

    addon_preferences = context.preferences.addons[addon_name].preferences

    if addon_preferences.toogle_constraints:
        if context.mode == "POSE":
            operator = row.operator("gamerigtool.toogle_constraint", text="Mute")
            operator.mute = True
            operator.use_selected = addon_preferences.use_selected

            operator = row.operator("gamerigtool.toogle_constraint", text="Unmute")
            operator.mute = False
            operator.use_selected = addon_preferences.use_selected

            row.prop(
                addon_preferences, "use_selected", text="", icon="RESTRICT_SELECT_OFF"
            )


classes = [GRT_Generate_Game_Rig]


def register():
    bpy.types.VIEW3D_HT_header.append(draw_item)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(draw_item)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

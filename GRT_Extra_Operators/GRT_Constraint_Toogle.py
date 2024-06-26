import bpy

# Editing bone


class GRT_Constraint_Toogle(bpy.types.Operator):
    """Constraint Toogle"""

    bl_idname = "gamerigtool.toogle_constraint"
    bl_label = "Toogle Constraints"
    bl_options = {"REGISTER", "UNDO"}

    mute: bpy.props.BoolProperty()
    use_selected: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        if context.mode in ["OBJECT", "POSE"]:
            return True
        else:
            return False

    def execute(self, context):
        for object in context.selected_objects:
            if object.type == "ARMATURE":
                # object = context.object
                Pose_Bone = object.pose.bones

                for bone in Pose_Bone:
                    if self.use_selected:
                        if bone.bone.select:
                            for constraint in bone.constraints:
                                constraint.mute = self.mute

                    else:
                        for constraint in bone.constraints:
                            constraint.mute = self.mute

        return {"FINISHED"}


class GRT_Constraint_Game_Rig_Toogle(bpy.types.Operator):
    """Constraint Game Rig Toogle"""

    bl_idname = "gamerigtool.toogle_game_rig_constraint"
    bl_label = "Toogle Game Rig Constraints"
    bl_options = {"REGISTER", "UNDO"}

    mute: bpy.props.BoolProperty()
    use_selected: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        if context.mode in ["OBJECT", "POSE"]:
            return True
        else:
            return False

    def execute(self, context):
        scn = context.scene
        Global_Settings = scn.GRT_Action_Bakery_Global_Settings

        control_rig = Global_Settings.Source_Armature
        deform_rig = Global_Settings.Target_Armature

        if deform_rig:
            Pose_Bone = deform_rig.pose.bones

            for bone in Pose_Bone:
                if self.use_selected:
                    if bone.bone.select:
                        for constraint in bone.constraints:
                            constraint.mute = self.mute

                else:
                    for constraint in bone.constraints:
                        constraint.mute = self.mute

        return {"FINISHED"}


classes = [GRT_Constraint_Toogle, GRT_Constraint_Game_Rig_Toogle]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

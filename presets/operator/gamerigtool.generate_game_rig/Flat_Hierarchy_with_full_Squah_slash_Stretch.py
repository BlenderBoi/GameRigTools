import bpy
op = bpy.context.active_operator

op.Extract_Mode = 'DEFORM'
op.Flat_Hierarchy = True
op.Disconnect_Bone = True
op.Constraint_Type = 'TRANSFORM'
op.Animator_Remove_BBone = False
op.Animator_Disable_Deform = False
op.Parent_To_Deform_Rig = True
op.Deform_Armature_Name = ''
op.Deform_Remove_BBone = True
op.Deform_Move_Bone_to_Layer1 = True
op.Deform_Set_Inherit_Rotation_True = True
op.Deform_Set_Inherit_Scale_Full = True
op.Deform_Set_Local_Location_True = True
op.Deform_Remove_Non_Deform_Bone = True
op.Deform_Unlock_Transform = True
op.Deform_Remove_Shape = True
op.Deform_Remove_All_Constraints = True
op.Deform_Copy_Transform = True
op.Deform_Bind_to_Deform_Rig = True
op.Remove_Custom_Properties = True
op.Remove_Animation_Data = True
op.Show_Advanced = False

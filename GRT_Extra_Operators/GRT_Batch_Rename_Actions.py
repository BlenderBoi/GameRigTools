import bpy



Mode = [("REPLACE","Replace","Replace"),("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix")]
Scope = [("SELECTED_BAKER","Selected Action in Action Bakery","Selected Action in Action Bakery"),("ACTION_BAKERY","Action Bakery","Action Bakery"),("ALL","All","All")]

class GRT_Batch_Rename_Actions(bpy.types.Operator):
    """Batch Rename Actions"""
    bl_idname = "gamerigtool.batch_rename_actions"
    bl_label = "Batch Rename Actions"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.EnumProperty(items=Mode)
    scope: bpy.props.EnumProperty(items=Scope)
    name_01: bpy.props.StringProperty()
    name_02: bpy.props.StringProperty()




    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):

        layout = self.layout
        layout.prop(self, "scope", text="")
        layout.prop(self, "mode", text="Mode", expand=True)

        if self.mode == "REPLACE":
            layout.prop(self, "name_01", text="From")
            layout.prop(self, "name_02", text="To")

        if self.mode == "PREFIX":
            layout.prop(self, "name_01", text="Prefix")

        if self.mode == "SUFFIX":
            layout.prop(self, "name_01", text="Suffix")



    def execute(self, context):

        scn = context.scene
        Action_Bakery = scn.GRT_Action_Bakery

        if self.scope == "SELECTED_BAKER":

            actions = [baker.Action for baker in Action_Bakery if baker.Action and baker.Bake_Select]


        if self.scope == "ACTION_BAKERY":

            actions = [baker.Action for baker in Action_Bakery if baker.Action]

        if self.scope == "ALL":

            actions = bpy.data.actions

        bpy.context.view_layer.update()


        for action in actions:

            if self.mode == "PREFIX":
                name = self.name_01 + action.name
                action.name = name

            if self.mode == "SUFFIX":
                name = action.name + self.name_01
                action.name = name

            if self.mode == "REPLACE":
                action.name = action.name.replace(self.name_01, self.name_02)


        return {'FINISHED'}




classes = [GRT_Batch_Rename_Actions]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

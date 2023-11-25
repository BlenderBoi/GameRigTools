
import bpy


ENUM_Mode = [("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix"),("REMOVE","Remove","Remove"), ("REPLACE","Replace","Replace")]


class GRT_Batch_Rename_Vertex_Groups(bpy.types.Operator):
    """Batch Rename Vertex Groups"""
    bl_idname = "gamerigtool.batch_rename_vertex_groups"
    bl_label = "Batch Rename Vertex Groups"
    bl_options = {'UNDO', 'REGISTER'}

    Mode: bpy.props.EnumProperty(items=ENUM_Mode)

    Name01: bpy.props.StringProperty()
    Name02: bpy.props.StringProperty()

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):

        layout = self.layout
        
        layout.prop(self, "Mode",text="Mode")
        
        if self.Mode == "PREFIX":
            layout.prop(self, "Name01", text="Prefix")
        
        if self.Mode == "SUFFIX":
            layout.prop(self, "Name01", text="Suffix")
        
        if self.Mode == "REMOVE":
            layout.prop(self, "Name01", text="Remove")
            
        if self.Mode == "REPLACE":
            layout.prop(self, "Name01", text="Find")
            layout.prop(self, "Name02", text="Replace")    
        
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        object = context.object
        
        for vertex_group in object.vertex_groups:
            if self.Mode == "PREFIX":
                vertex_group.name = self.Name01 + vertex_group.name
            if self.Mode == "SUFFIX":
                vertex_group.name = vertex_group.name + self.Name01
            if self.Mode == "REMOVE":
                vertex_group.name = vertex_group.name.replace(self.Name01, "")
            if self.Mode == "REPLACE":
                vertex_group.name = vertex_group.name.replace(self.Name01, self.Name02)
        
        return {'FINISHED'}

# def menu_func(self, context):
#     self.layout.operator(Batch_Rename_Vertex_Groups.bl_idname, text=Batch_Rename_Vertex_Groups.bl_label)
classes = [GRT_Batch_Rename_Vertex_Groups]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

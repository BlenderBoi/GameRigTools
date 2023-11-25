import bpy
import rna_prop_ui



def get_custom_properties(object):

    object_type = type(object)
    type_dict = dir(object_type)

    properties_name = []

    for k, v in object.items():

        if k in type_dict:
            tmp = getattr(object_type, k)

            if isinstance(tmp, bpy.props._PropertyDeferred):
                continue
            
        if not isinstance(v, (int, float)):     
           continue

        properties_name.append(k) 

    return properties_name

def grab_property_source(self, context):

    object = None
    source = None

    if self.Source_Object:
        object = context.view_layer.objects.get(self.Source_Object)

    if object:

        if self.Source_Type == "OBJECT":
            source = object
        if self.Source_Type == "DATA":
            source = object.data

        if self.Source_Type in ["POSEBONE", "EDITBONE"]:
            if self.Source_Type == "POSEBONE":
                if self.Source_Bone:
                    
                    PoseBone = object.pose.bones.get(self.Source_Bone)
                    if PoseBone:
                        source = PoseBone

            if self.Source_Type == "EDITBONE":
            
                if self.Source_Bone:
                    
                    EditBone = object.data.edit_bones.get(self.Source_Bone)

                    if EditBone:
                        source = EditBone
                        
    return source 

def grab_properties(self, context):

    object = None
    source = grab_property_source(self, context)
    custom_properties = []

    if source:

        custom_properties = get_custom_properties(source)

                        
    return custom_properties


def ENUM_Property_Picker(self, context):

    items = []

    custom_properties = grab_properties(self, context) 

    for cp in custom_properties:
        item = (cp, cp, cp)
        items.append(item)

    if len(items) > 0:
        return items
    else:
        return [("NONENULLNOTFOUND", "None", "None")]




def ENUM_Source_Type(self, context):
     
    object = None
    isArmature = False


    items = [("OBJECT","Object","Object"),("DATA","Object Data","Object Data")]


    if self.Source_Object:
        object = context.view_layer.objects.get(self.Source_Object)

    if object:
        if object.type == "ARMATURE":
            isArmature = True
        if object.type == "EMPTY":
            items = [("OBJECT","Object","Object")]
    
    if isArmature:
        items = [("OBJECT","Object","Object"),("DATA","Object Data","Object Data"),("POSEBONE","Bone","Bone")]
        
    return items

class GRT_Bake_Custom_Properties(bpy.types.Operator):
    """Bake Custom Properties"""
    bl_idname = "gamerigtool.bake_custom_properties"
    bl_label = "Bake Custom Properties"
    bl_options = {'REGISTER', 'UNDO'}

    frame_start: bpy.props.IntProperty(default=0)
    frame_end: bpy.props.IntProperty(default=100)
   
    Property_Name_Picker: bpy.props.EnumProperty(items=ENUM_Property_Picker)
    Property_Name_String: bpy.props.StringProperty()
    Use_String: bpy.props.BoolProperty(default=False)
    All_Properties: bpy.props.BoolProperty(default=False)
    All_Bones: bpy.props.BoolProperty(default=False)

    Source_Object: bpy.props.StringProperty()
    Source_Bone: bpy.props.StringProperty()
    Source_Type: bpy.props.EnumProperty(items=ENUM_Source_Type)


    @classmethod
    def poll(cls, context):
        return context.mode in ["OBJECT", "POSE"]


    def invoke(self, context, event):
        self.frame_start = context.scene.frame_start
        self.frame_end = context.scene.frame_end
        if context.object:
            self.Source_Object = context.object.name
            
            active_bone = context.active_bone

            if context.active_bone:
                self.Source_Bone = active_bone.name

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout


        object = None

        if self.Source_Object:
            object = context.view_layer.objects.get(self.Source_Object)



        row = layout.row(align=True)
        row.prop(self, "frame_start", text="Frame Start")
        row.prop(self, "frame_end", text="Frame End")
        

        layout.prop_search(self, "Source_Object", context.view_layer, "objects", text="Object" )
        if object:
            if object.type == "ARMATURE":


                if self.Source_Type in ["POSEBONE"]:
                    # if not self.All_Bones:
                    layout.prop_search(self, "Source_Bone", object.pose, "bones", text="Bone")
                    # layout.prop(self, "All_Bones", text="All Bones")

            layout.prop(self, "Source_Type", text="Type" )

            row = layout.row()
            
            custom_properties = grab_properties(self, context)

            if len(custom_properties) > 0:
                
                if not self.All_Properties:
                    if self.Use_String:
                        row.prop(self, "Property_Name_String", text="Property")
                    else:
                        row.prop(self, "Property_Name_Picker", text="Property")

                    row.prop(self, "Use_String", text="" , icon="OUTLINER_OB_FONT")

                layout.prop(self, "All_Properties", text="Use All Properties")

            else:
                row.label(text="No Custom Properties Found", icon="INFO")

    def get_property_name(self, context):
        if self.Use_String:
            return self.Property_Name_String
        else:
            return self.Property_Name_Picker

    def execute(self, context):
        
        source = grab_property_source(self, context)
        properties = grab_properties(self, context)
        source_type = self.Source_Type
        current_mode = context.mode        
        object = None
    

        if len(properties) > 0:
                
            if source:
                if not source.animation_data:
                    source.animation_data_create()
                extrapolation = source.animation_data.action_extrapolation
                source.animation_data.action_extrapolation = "NOTHING"

                for i in range(self.frame_start,self.frame_end):
                    context.scene.frame_set(i)
                    if self.All_Properties:
                        for prop in properties:    
                            if not source.animation_data:
                                source.animation_data_create()
                            path = rna_prop_ui.rna_idprop_quote_path(prop)
                            source.keyframe_insert(data_path = path)
                            source.keyframe_insert(data_path = path)
                    else:
                        prop = self.get_property_name(context)
                        if prop in properties:


                            path = rna_prop_ui.rna_idprop_quote_path(self.get_property_name(context))
                            source.keyframe_insert(data_path = path)
                            source.keyframe_insert(data_path = path)
                            
                source.animation_data.action_extrapolation = extrapolation

        return {'FINISHED'}



classes = [GRT_Bake_Custom_Properties]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()


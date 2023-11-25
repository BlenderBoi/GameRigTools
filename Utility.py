import bpy

def update_UI():
    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()




def draw_subpanel(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_RIGHT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

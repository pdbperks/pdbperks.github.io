#!/usr/bin/env python

# create text drop shadow in GIMP Python

from gimpfu import *

def drop_shadow(initstr, font, size, pattern, color, shadowOffsetX, shadowOffsetY, color2, outlineWidth, color3, color4, pattern2) :

    g = gimp.pdb
    if abs(shadowOffsetX) >= abs(shadowOffsetY):
        extra = abs(shadowOffsetX)
    else:
        extra = abs(shadowOffsetY) + 10
    extraBorder = extra + outlineWidth
    # Make a new image. Size 10x10 for now -- we'll resize later.
    img = gimp.Image(1, 1, RGB)

    # Save the current foreground color:
    pdb.gimp_context_push()

    # Set the text color
    gimp.set_foreground(color)
    gimp.set_background(color4)
    

    # Create a new text layer (-1 for the layer means create a new layer)
    layer = pdb.gimp_text_fontname(img, None, 0,0, initstr,  extraBorder,
                                   True, size, PIXELS, font)

    # Resize the image to the size of the layer
    img.resize(layer.width, layer.height, 0, 0)
    # Background layer.
    # Can't add this first because we don't know the size of the text layer.
    background = gimp.Layer(img, "Background", layer.width, layer.height,
                            RGB_IMAGE, 100, NORMAL_MODE)
    background.fill(BACKGROUND_FILL)
    
    g.gimp_context_set_pattern(pattern2)
    g.gimp_context_set_sample_transparent(TRUE)
    img.add_layer(background, 1)
    #img.add_layer(layer2, 1)
    #g.gimp_edit_fill(background,    FOREGROUND_FILL)
    back_pattern = pdb.gimp_layer_copy(layer,TRUE)
    img.add_layer(back_pattern, 1)
    g.gimp_edit_fill(back_pattern, PATTERN_FILL)    
    g.gimp_layer_set_opacity(back_pattern, 80)
    
    outline = pdb.gimp_layer_copy(layer,TRUE)
    #gimp.Layer(img, "outline", layer.width, layer.height,   RGB_IMAGE, 100, SCREEN_MODE)

    img.add_layer(outline, 1)
    #g.gimp_edit_fill(outline, PATTERN_FILL)
    
    # Set the dropshadow color
    gimp.set_foreground(color2)
    
    #try copying the layer
    
    layer2 = pdb.gimp_text_fontname(img, None, shadowOffsetX, shadowOffsetY, initstr, extraBorder ,
                           True, size, PIXELS, font)    


    g.gimp_layer_set_opacity(layer2, 60)
    #best way to select text items 
    g.gimp_image_select_item(img, CHANNEL_OP_REPLACE,layer) 
    g.gimp_image_select_item(img, CHANNEL_OP_ADD,layer2) 
    g.gimp_selection_grow (img,outlineWidth)
    gimp.set_foreground(color3)
    g.gimp_edit_fill(outline,FOREGROUND_FILL)
    g.gimp_layer_set_opacity(outline, 60)
    #add a top texture layer with opacity
    textPatternLayer = pdb.gimp_layer_copy(layer,TRUE)
    img.add_layer(textPatternLayer, 1)
    g.gimp_image_raise_item_to_top(img, textPatternLayer)
    g.gimp_image_select_item(img, CHANNEL_OP_REPLACE,textPatternLayer)
    g.gimp_context_set_pattern(pattern)
    g.gimp_edit_fill(textPatternLayer, PATTERN_FILL)
    g.gimp_layer_set_opacity(textPatternLayer, 60)
    
    g.gimp_selection_none(img)

    # Create a new image window
    gimp.Display(img)

    # Show the new image windows
    gimp.displays_flush()

    # Restore the old foreground color:
    pdb.gimp_context_pop()

register(
    "plug_in_drop_shadow",
    "Create a dropshadow text box",
    "Create a drop shadow for your text string",
    "DPerks",
    "DPerks",
    "2014",
    "Drop shadow text (Py)...",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "string", "Text string", "welcome"),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "size", "Font size", 120, (1, 3000, 1)),
	(PF_PATTERN, "pattern","Text Pattern","Leopard"),
	(PF_COLOR, "color", "Text color", (1.0, 0.0, 0.0)),
        (PF_SLIDER, "shadowOffsetX", "OffsetX", 5, (-30, 30, 1)),
        (PF_SLIDER, "shadowOffsetY", "OffsetY", 5, (-30, 30, 1)),
	(PF_COLOR, "color2", "Shadow color", (0.3, 0.0, 0.0)),
        (PF_SPINNER, "outlineWidth", "Outline", 5, (-30, 30, 1)),
	(PF_COLOR, "color3", "Outline color", (0.3, 0.0, 0.0)),
        (PF_COLOR, "color4", "Base color", (0.3, 0.0, 0.0)),
        (PF_PATTERN, "pattern2","Base Pattern","Leopard")
        
        
    ],
    [],
    drop_shadow, menu="<Image>/File/Create")

main()

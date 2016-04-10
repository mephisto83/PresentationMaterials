import bpy
import sys
argv = sys.argv
try:
    index = argv.index("--") + 1
except:
    index = len(argv)

argv = argv[index:]
start = 1
stop = 1
default_camera = "default_camera"
print(argv)
if(argv[0]):
	start = int(argv[0])

if(argv[1]):
	stop = int(argv[1])

if(argv[2]):
	default_camera = argv[2]
use_border = True
if len(argv) == 7:
    if(argv[3] != None):
        minx = float(argv[3])
    else:
        use_border = False
    if(argv[4] != None):
        miny = float(argv[4])
    else:
        use_border = False
    if(argv[5] != None):
        maxx = float(argv[5])
    else:
        use_border = False
    if(argv[6] != None):
        maxy = float(argv[6])
    else:
        use_border = False
else:
    use_border = False;			
bpy.context.scene.frame_start = start
bpy.context.scene.frame_end = stop
bpy.context.scene.camera = bpy.data.objects[default_camera]
if use_border:
    bpy.context.scene.render.border_min_x = minx
    bpy.context.scene.render.border_max_x = maxx
    bpy.context.scene.render.border_min_y = miny
    bpy.context.scene.render.border_max_y = maxy
    bpy.context.scene.render.use_border = True
bpy.ops.ptcache.bake_all(bake=True)

if hasattr(bpy.context.scene, "pl_studio_props"):
	if bpy.context.scene.pl_studio_props.use_background_mask:
		bpy.context.scene.pl_studio_props.use_background_mask = False
		bpy.context.scene.pl_studio_props.use_background_mask = True
        
if hasattr(bpy.context.scene.world, "pl_skies_settings"):
    bpy.context.scene.world.pl_skies_settings.show_advanced = True
    bpy.context.scene.world.pl_skies_settings.use_advanced_sky = True
    bpy.context.scene.world.pl_skies_settings.use_advanced_sky = False

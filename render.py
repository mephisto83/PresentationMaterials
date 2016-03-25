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
	
bpy.context.scene.frame_start = start
bpy.context.scene.frame_end = stop
bpy.context.scene.camera = bpy.data.objects[default_camera]
bpy.ops.ptcache.bake_all(bake=True)

if hasattr(bpy.context.scene, "pl_studio_props"):
	if bpy.context.scene.pl_studio_props.use_background_mask:
		bpy.context.scene.pl_studio_props.use_background_mask = False
		bpy.context.scene.pl_studio_props.use_background_mask = True
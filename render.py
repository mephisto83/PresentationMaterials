import bpy
import sys
import os.path
import json
argv = sys.argv
try:
    index = argv.index("--") + 1
except:
    index = len(argv)

argv = argv[index:]
start = 1
stop = 1
config_file = None
default_camera = "default_camera"
print(argv)
if(argv[0]):
	start = int(argv[0])

if(argv[1]):
	stop = int(argv[1])

if(argv[2]):
	default_camera = argv[2]
if(argv[3]):
    config_file = argv[3]
use_border = True
if len(argv) == 8:
    if(argv[4] != None):
        minx = float(argv[4])
    else:
        use_border = False
    if(argv[5] != None):
        miny = float(argv[5])
    else:
        use_border = False
    if(argv[6] != None):
        maxx = float(argv[6])
    else:
        use_border = False
    if(argv[7] != None):
        maxy = float(argv[7])
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
def getProskyConfig(config):
    if "scenes"  in config:
        for scene in config["scenes"]:
            if "proskies" in scene:
                proskies = scene["proskies"]
                if "skies" in proskies:
                    return proskies["skies"]
    return None
if hasattr(bpy.context.scene, "pl_studio_props"):
	if bpy.context.scene.pl_studio_props.use_background_mask:
		bpy.context.scene.pl_studio_props.use_background_mask = False
		bpy.context.scene.pl_studio_props.use_background_mask = True
if config_file != None:
    f = open(config_file, 'r')
    print(config_file)
    filecontents = f.read()
    obj = json.loads(filecontents)
    # bpy.context.scene.render.image_settings.file_format = obj["settings"]["file_format"]
    # bpy.context.scene.render.image_settings.film_transparent = obj["settings"]["film_transparent"]
    
if hasattr(bpy.context.scene.world, "pl_skies_settings") and config_file != None:
    print("setting pl_skies_settings ------------------------------------------------------------" )
    proskyconfig = getProskyConfig(obj)
    if proskyconfig != None:
        if "use_pl_skies" in proskyconfig:
            if proskyconfig["use_pl_skies"]:
                bpy.context.scene.world.pl_skies_settings.use_pl_skies = False
                bpy.context.scene.world.pl_skies_settings.use_pl_skies = True
                bpy.context.scene.world.pl_skies_settings.use_advanced_sky = True
                bpy.context.scene.world.env_previews = proskyconfig["evn_previews"]
                bpy.context.scene.world.pl_skies_settings.z_rotation = proskyconfig["z_rotation"]
                bpy.context.scene.world.pl_skies_settings.sun = proskyconfig["sun"]
                bpy.context.scene.world.pl_skies_settings.sky = proskyconfig["sky"]
    print("set pl_skies_settings ------------------------------------------------------------" )

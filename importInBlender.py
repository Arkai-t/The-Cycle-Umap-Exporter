import bpy
import sys
import json
import math

deleteOnStart = True

#Clean everything from scene
if deleteOnStart:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.outliner.orphans_purge()
    bpy.ops.outliner.orphans_purge()
    bpy.ops.outliner.orphans_purge()

assetsFolder = "D:/Images/Umodel_Screenshots/Alpha/Game/"
jsonfile = "D:/Documents/CodeFoureTout/The Cycle Umap exporter/test.json"

if jsonfile:
    with open(jsonfile, 'r') as f:
        jsonData = json.load(f)

#Init existing material tab
matTab = []

#Parcourir le json et importer les objets dans la scène
for obj in jsonData:
    
    #Construire le nom du fichier
    path = ""
    if(obj["Type"] == "SkeletalMeshComponent"):
        path = assetsFolder + obj["Properties"]["SkeletalMesh"]["ObjectPath"]  
    elif(obj["Type"] == "StaticMeshComponent"):   
        path = assetsFolder + obj["Properties"]["StaticMesh"]["ObjectPath"]
        
    path = path.split('.')[0]
    path += ".gltf"
        
    #Importer dans blender
    blendObj = bpy.ops.import_scene.gltf(filepath=str(path))
    
    #Déplacer
    if("RelativeLocation" in obj["Properties"]):
        bpy.ops.transform.translate(value=[obj["Properties"]["RelativeLocation"]["X"]/100, obj["Properties"]["RelativeLocation"]["Y"]/100, obj["Properties"]["RelativeLocation"]["Z"]/100])
    
    #Tourner
    if("RelativeRotation" in obj["Properties"]):
        bpy.context.object.rotation_mode = 'XYZ'
        bpy.ops.transform.rotate(value=math.radians(obj["Properties"]["RelativeRotation"]["Pitch"]), orient_axis='X')
        bpy.ops.transform.rotate(value=math.radians(obj["Properties"]["RelativeRotation"]["Roll"]), orient_axis='Y')
        bpy.ops.transform.rotate(value=math.radians(obj["Properties"]["RelativeRotation"]["Yaw"]), orient_axis='Z')
    
    #Mettre à l'échelle
    if("RelativeScale3D" in obj["Properties"]):
        bpy.ops.transform.resize(value=[obj["Properties"]["RelativeScale3D"]["X"], obj["Properties"]["RelativeScale3D"]["Y"], obj["Properties"]["RelativeScale3D"]["Z"]])
    
    """
        Gérer les matériaux
    """
    
    #Voir si le mat est une duplication
    #Peut etre gourmand en performance
    for currentMat in bpy.context.object.material_slots:
        nameMat = currentMat.name.split('.')
        if(len(nameMat) > 1):
            print("Duplicate mat")
            #Si le mat est dupliqué, alors le remplacer
            print(nameMat[0] in bpy.data.materials)
            if(nameMat[0] in bpy.data.materials):
                currentMat.material = bpy.data.materials[nameMat[0]]
        else:
            #Construire le mat
            a = 1
            
    #Enlever les mat qui ne sont plus utilisé
    bpy.ops.outliner.orphans_purge
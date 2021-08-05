"""
Made by Arkait
Version: 0.1
Date: 03/08/2021

Filter umap file for another script for blender
"""

import json
import math
import bpy

#Global var with default values
deleteOnStart = True
isTexturingModels = True
#@TODO MUST BE CHANGE
configPath = "D:\Documents\CodeFoureTout\The-Cycle-Umap-Exporter\config.json"

def deleteEverything():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.outliner.orphans_purge()
    bpy.ops.outliner.orphans_purge()
    bpy.ops.outliner.orphans_purge()

def main(pathFile, exportedGameAssetsPath):
    """
    Filtre l'Umap pour ne garder que ce qui est intéressant
    """
    print('Filtering umap : ' + pathFile + '\n')

    #Ouvrir le fichier
    if pathFile:
        umap = None
        with open(pathFile, 'r') as f:
            umap = json.load(f)
        
        jsonFiltered = []

        #Parcourir chaque objet pour les filtrer
        for obj in umap:
            if(obj["Type"] == "SkeletalMeshComponent"):
                #Tester si l'objet possède un attribut SkeletalMesh
                if("SkeletalMesh" in obj["Properties"]):
                    #Convertir le chemin de l'objet en un chemin local du dossier exporté
                    obj["Properties"]["SkeletalMesh"]["ObjectPath"] = str(obj["Properties"]["SkeletalMesh"]["ObjectPath"]).replace("Prospect/Content/", "")
                    #obj["Properties"]["OverrideMaterials"]["ObjectPath"] = str(obj["Properties"]["OverrideMaterials"]["ObjectPath"]).removeprefix("Prospect/Content/")

                    jsonFiltered.append(obj)
            
            elif(obj["Type"] == "StaticMeshComponent"):
                #Tester si l'objet possède un attribut StaticMesh
                if("StaticMesh" in obj["Properties"]):
                    #Convertir le chemin de l'objet en un chemin local du dossier exporté
                    obj["Properties"]["StaticMesh"]["ObjectPath"] = str(obj["Properties"]["StaticMesh"]["ObjectPath"]).replace("Prospect/Content/", "")

                    jsonFiltered.append(obj)

    """
    Building the blender file
    """
    #Init existing material tab
    matTab = []

    if deleteOnStart:
        deleteEverything()

    #Parcourir le json et importer les objets dans la scène
    for obj in jsonFiltered:  
        #Construire le nom du fichier
        path = ""
        if(obj["Type"] == "SkeletalMeshComponent"):
            path = exportedGameAssetsPath + obj["Properties"]["SkeletalMesh"]["ObjectPath"]  
        elif(obj["Type"] == "StaticMeshComponent"):   
            path = exportedGameAssetsPath + obj["Properties"]["StaticMesh"]["ObjectPath"]
            
        path = path.split('.')[0]
        path += ".gltf"
            
        #Importer l'objet dans blender
        bpy.ops.import_scene.gltf(filepath=str(path))
        
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

        #Enlever les matériaux dupliqué
        for currentMat in bpy.context.object.material_slots:
            nameMat = currentMat.name.split('.')
            if(len(nameMat) > 1):
                print("Duplicate mat")
                #Si le mat est dupliqué, alors le remplacer
                print(nameMat[0] in bpy.data.materials)
                if(nameMat[0] in bpy.data.materials):
                    currentMat.material = bpy.data.materials[nameMat[0]]
            else:
                if isTexturingModels:
                    #Construire le mat
                    a = 1
                
        #Enlever les mat qui ne sont plus utilisé du fichier Blender, nécessite un redémarage
        bpy.ops.outliner.orphans_purge


#Lire et tester le fichier de configuration
with open(configPath, 'r') as f:
    fJson = json.load(f)
    if ("umapPath" in fJson and "exportedGameAssetsPath" in fJson):
        if(fJson["umapPath"] != "" and fJson["exportedGameAssetsPath"] != ""):
            if ("deleteExistingScene" in fJson):
                deleteOnStart = fJson["deleteExistingScene"]
            if ("texturingModels" in fJson):
                isTexturingModels = fJson["texturingModels"]
            #Si tout est OK, on lance le programme principal
            main(fJson["umapPath"], fJson["exportedGameAssetsPath"])
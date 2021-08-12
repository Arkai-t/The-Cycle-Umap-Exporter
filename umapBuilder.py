"""
Made by Arkait
Version: 0.1
Date: 03/08/2021

Filter umap file for another script for blender
"""

import json
import math
import bpy
import os

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

                    if ("OverrideMaterials" in obj["Properties"]):
                        for tmpMat in obj["Properties"]["OverrideMaterials"]:
                            if tmpMat != None:
                                tmpMat["ObjectPath"] = tmpMat["ObjectPath"].replace("Prospect/Content/", "")

                    jsonFiltered.append(obj)
            
            elif(obj["Type"] == "StaticMeshComponent"):
                #Tester si l'objet possède un attribut StaticMesh
                if("StaticMesh" in obj["Properties"]):
                    #Convertir le chemin de l'objet en un chemin local du dossier exporté
                    obj["Properties"]["StaticMesh"]["ObjectPath"] = str(obj["Properties"]["StaticMesh"]["ObjectPath"]).replace("Prospect/Content/", "")

                    if ("OverrideMaterials" in obj["Properties"]):
                        for tmpMat in obj["Properties"]["OverrideMaterials"]:
                            if tmpMat != None:
                                tmpMat["ObjectPath"] = tmpMat["ObjectPath"].replace("Prospect/Content/", "")

                    jsonFiltered.append(obj)

    """
    Building the blender file
    """
    if deleteOnStart:
        deleteEverything()

    #Parcourir le json et importer les objets dans la scène
    for obj in jsonFiltered:  
        #Construire le nom du fichier
        pathObj = ""
        if(obj["Type"] == "SkeletalMeshComponent"):
            pathObj = exportedGameAssetsPath + obj["Properties"]["SkeletalMesh"]["ObjectPath"]  
        elif(obj["Type"] == "StaticMeshComponent"):   
            pathObj = exportedGameAssetsPath + obj["Properties"]["StaticMesh"]["ObjectPath"]
            
        pathObj = pathObj.split('.')[0]
        pathObj += ".gltf"
            
        #Importer l'objet dans blender
        bpy.ops.import_scene.gltf(filepath=str(pathObj))
        
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

        #Enlever les matériaux dupliqué et les créer
        for currentMat in bpy.context.object.material_slots:
            i = -1
            nameMat = currentMat.name.split('.')
            if(len(nameMat) > 1):
                #Si le mat est dupliqué, alors le remplacer
                if(nameMat[0] in bpy.data.materials):
                    currentMat.material = bpy.data.materials[nameMat[0]]
            else:
                if isTexturingModels:                                 
                    #Récupérer la localisation du mat
                    pathFicMat = ""
                    
                    #Refaire ça, car overrideMaterials n'est que sur l'un des mat mais pas tous
                    if ("OverrideMaterials" in obj["Properties"]):
                        for tmp in obj["Properties"]["OverrideMaterials"]:
                            if tmp != None:                          
                                #Récupérer la localisation du mat
                                pathFicMat = exportedGameAssetsPath
                                pathFicMat += tmp["ObjectPath"].split('.')[0]
                    else:
                        #Récupérer la localisation du dossier
                        pathFicMat = '/'.join(pathObj.split('/')[:-1])
                        pathFicMat += '/'
                        pathFicMat += currentMat.name
                        
                    #Récupérer et modifier le mat
                    tmpMat = bpy.data.materials.get(nameMat[0])
                    tmpMat.use_nodes = True
                    nodes = tmpMat.node_tree.nodes
                        
                    #Test peut etre inutile par la suite
                    if(pathFicMat != ""):
                        pathFicMat += ".mat"
                        #Si besoin
                        pathFicMatDetail = pathFicMat.replace(".mat", ".props.txt")
                        
                        print(pathFicMat)
                        
                        #Trouver les textures
                        if (os.path.isfile(pathFicMat)):
                            f = open(pathFicMat, 'r')
                            
                            lignes = f.readlines()
                            #Cette ligne est pour récupérer la texture M correcte
                            textureGenericName = '_'.join(lignes[0].split('=')[1].split('_')[:-1])
                            for ligne in lignes:
                                #Enlever les \n car ils interfèrent avec les noms des fichier
                                ligne = ligne.replace("\n", "")
                                tmp = ligne.split('=')
                                if (tmp[0] == "Diffuse"):
                                    #Ajouter le mat dans les nodes
                                    diffuseMatPath = '/'.join(pathFicMat.split('/')[:-1])
                                    diffuseMatPath += '/'
                                    diffuseMatPath += tmp[1]
                                    diffuseMatPath += ".png"
                                    
                                    if (os.path.isfile(diffuseMatPath)):
                                        diffuseTextureNode = nodes.new("ShaderNodeTexImage")                                        
                                        diffuseTextureNode.image = bpy.data.images.load(diffuseMatPath, check_existing=False)
                                        bpy.data.images[diffuseMatPath.split('/')[-1]].colorspace_settings.name = 'sRGB'
                                        
                                        #Connect node
                                        tmpMat.node_tree.links.new(diffuseTextureNode.outputs["Color"], nodes["Principled BSDF"].inputs["Base Color"])

                                    
                                elif (tmp[0] == "Normal"):
                                    #Ajouter le mat dans les nodes
                                    normalMatPath = '/'.join(pathFicMat.split('/')[:-1])
                                    normalMatPath += '/'
                                    normalMatPath += tmp[1]
                                    normalMatPath += ".png"
                                    
                                    if (os.path.isfile(normalMatPath)):
                                        normalTextureNode = nodes.new("ShaderNodeTexImage")                                        
                                        normalTextureNode.image = bpy.data.images.load(normalMatPath, check_existing=False)
                                        bpy.data.images[normalMatPath.split('/')[-1]].colorspace_settings.name = 'Non-Color'
                                        normalMapNode = nodes.new("ShaderNodeNormalMap")
                                        
                                        #Connect node
                                        tmpMat.node_tree.links.new(normalTextureNode.outputs["Color"], normalMapNode.inputs["Color"])
                                        tmpMat.node_tree.links.new(normalMapNode.outputs["Normal"], nodes["Principled BSDF"].inputs["Normal"])

                                        
                                elif (tmp[0] == "Emissive"):
                                    #Ajouter le mat dans les nodes
                                    emissiveMat = tmp[1]
                                #Récupérer M texture -> Faire attention car plusieurs textures M
                                elif (tmp[1].endswith("_M") and tmp[1].startswith(textureGenericName)):
                                    #Ajouter le mat dans les nodes
                                    maskMatPath = '/'.join(pathFicMat.split('/')[:-1])
                                    maskMatPath += '/'
                                    maskMatPath += tmp[1]
                                    maskMatPath += ".png"
                                    
                                    if (os.path.isfile(maskMatPath)):
                                        maskTextureNode = nodes.new("ShaderNodeTexImage")                                        
                                        maskTextureNode.image = bpy.data.images.load(maskMatPath, check_existing=False)
                                        bpy.data.images[maskMatPath.split('/')[-1]].colorspace_settings.name = 'Non-Color'
                                        sepRGBNode = nodes.new("ShaderNodeSeparateRGB")
#                                        mixRGBNode = nodes.new("ShaderNodeMixRGB")
#                                        mixRGBNode.blend_type = 'MULTIPLY'
#                                        mixRGBNode.inputs[0].default_value = 1
                                        
                                        #Connect node
                                        tmpMat.node_tree.links.new(maskTextureNode.outputs["Color"], sepRGBNode.inputs["Image"])
                                        tmpMat.node_tree.links.new(sepRGBNode.outputs["R"], nodes["Principled BSDF"].inputs["Roughness"])
                                        #Voir pour AO        
#                                        tmpMat.node_tree.links.new(sepRGBNode.outputs["G"], mixRGBNode.inputs["Color2"])
#                                        if ((textureGenericName + "_D") in nodes):
#                                            tmpMat.node_tree.links.new(nodes[textureGenericName + "_D"], mixRGBNode.inputs["Color1"])
#                                            tmpMat.node_tree.links.new(mixRGBNode.outputs["Color"], nodes["Principled BSDF"].inputs["Base Color"])
                                        tmpMat.node_tree.links.new(sepRGBNode.outputs["B"], nodes["Principled BSDF"].inputs["Metallic"])
                            f.close()
                        else:
                            print("File not found: "  + pathFicMat)
                    

                
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
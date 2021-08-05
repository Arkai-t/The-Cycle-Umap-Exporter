"""
Made by Arkait
Version: 0.1
Date: 03/08/2021

Filter umap file for another script for blender
"""

import json #Pour manipuler les JSON
import sys #Pour lire les paramètres

#Things for people that can't read the doc
if(sys.argv[1] == "-h" or sys.argv[1] == "-help"):
    print("""
    Run:
        - python converter.py [umap pathfile in json]
        - -h or -help to print this message
    """)
    sys.exit()

if(len(sys.argv) != 2):
    print("""
    Incorect usage !
    
    Correct usage:
        python converter.py [umap pathfile in json]
    """)
    sys.exit()


pathfile = str(sys.argv[1])
print('Exporting umap : ' + pathfile + '\n')

#Ouvrir le fichier
if pathfile:
    with open(pathfile, 'r') as f:
        umap = json.load(f)

    umapFiltered = []

    #Parcourir chaque objet pour les filtrer
    for obj in umap:
        if(obj["Type"] == "SkeletalMeshComponent"):
            #Tester si l'objet possède un attribut SkeletalMesh
            if("SkeletalMesh" in obj["Properties"]):
                #Convertir le chemin de l'objet en un chemin local du dossier exporté
                obj["Properties"]["SkeletalMesh"]["ObjectPath"] = str(obj["Properties"]["SkeletalMesh"]["ObjectPath"]).removeprefix("Prospect/Content/")
                #obj["Properties"]["OverrideMaterials"]["ObjectPath"] = str(obj["Properties"]["OverrideMaterials"]["ObjectPath"]).removeprefix("Prospect/Content/")

                umapFiltered.append(obj)
                print("Include object : " + obj["Properties"]["SkeletalMesh"]["ObjectName"])
        
        elif(obj["Type"] == "StaticMeshComponent"):
            #Tester si l'objet possède un attribut StaticMesh
            if("StaticMesh" in obj["Properties"]):
                #Convertir le chemin de l'objet en un chemin local du dossier exporté
                obj["Properties"]["StaticMesh"]["ObjectPath"] = str(obj["Properties"]["StaticMesh"]["ObjectPath"]).removeprefix("Prospect/Content/")

                umapFiltered.append(obj)
                print("Include object : " + obj["Properties"]["StaticMesh"]["ObjectName"])

        #Write new JSON
        with open("test.json", 'w') as newFile:
            json.dump(umapFiltered, newFile)
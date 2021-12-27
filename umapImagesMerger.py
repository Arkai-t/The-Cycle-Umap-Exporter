import os
import numpy as np
import cv2

#SETTINGS
mapNumImport = 6
fmodelExportFolder = "C:/Users/Moi/Downloads/TC Exported/fmodel/"
outputFolder = "C:/Users/Moi/Downloads/TC Exported/MapOutput/"

#FUNCTIONS
#Apply basic processing on a single image depending on the map
def singleImageProcessing(img, numMap):
    
    return img

#Concatene map images depending on the map
def buildImage(imgs, numMap, size_x, size_y):
    finalImg = imgs[0]
    if(numMap == 1 or numMap == 4):
        for i in range(1, size_x):
            finalImg = np.concatenate((finalImg, imgs[i]), axis=0)

        for i in range(1, size_y):
            tmpImg = imgs[i*size_x]
            for j in range(1, size_x):
                tmpImg = np.concatenate((tmpImg, imgs[i*size_x + j]), axis=0)

            finalImg = np.concatenate((finalImg, tmpImg), axis=1)

    elif(numMap == 2 or numMap == 6):
        for i in range(1, size_x):
            finalImg = np.concatenate((finalImg, imgs[i]), axis=1)

        for i in range(1, size_y):
            tmpImg = imgs[i*size_x]
            for j in range(1, size_x):
                tmpImg = np.concatenate((tmpImg, imgs[i*size_x + j]), axis=1)

            finalImg = np.concatenate((finalImg, tmpImg), axis=0)
    return finalImg

def globalImageProcessing(img, numMap):
    if(numMap == 1):
        #Rotate image 90° for map 1
        cv2.rotate(finalImg, cv2.ROTATE_90_CLOCKWISE)
    return img


#MAIN
mapChoice = {
        1: {
            'imgName': 'MAP01_',
            'imgFolder': (fmodelExportFolder + "Textures/Prospect/Content/Maps/MP/Map01/GEO/"),
            'outputName': 'Map01',
            'size_x': 10,
            'size_y': 10
        },
        2: {
            'imgName': 'MAP02_',
            'imgFolder': (fmodelExportFolder + "Textures/Prospect/Content/Maps/MP/Map02/GEO/"),
            'outputName': 'Map02',
            'size_x': 10,
            'size_y': 10
        },
        4: {
            'imgName': 'MAP04_',
            'imgFolder': (fmodelExportFolder + "Textures/Prospect/Content/Maps/MP/Map04/"),
            'outputName': 'Map04',
            'size_x': 4,
            'size_y': 5
        },
        6: {
            'imgName': 'MP_Map06_',
            'imgFolder': (fmodelExportFolder + "Textures/Prospect/Content/Maps/MP/Map06/GEO/"),
            'outputName': 'Map06',
            'size_x': 8,
            'size_y': 8
        }
    }

imgs = []
#Get all images
for i in range(0, mapChoice[mapNumImport]['size_y']):
    for j in range(0, mapChoice[mapNumImport]['size_x']):
        fileName = mapChoice[mapNumImport]['imgName'] + chr(i + 65) + str(j) + ".png"
        print("Importing: " + fileName)
        if (os.path.isfile(mapChoice[mapNumImport]['imgFolder'] + fileName)):
            img = cv2.imread(mapChoice[mapNumImport]['imgFolder'] + fileName, cv2.IMREAD_UNCHANGED)
            img = singleImageProcessing(img, mapNumImport)

            imgs.append(img)
        else:
            print("Error importing: " + fileName)

#Build image
finalImg = buildImage(imgs, mapNumImport, mapChoice[mapNumImport]['size_x'], mapChoice[mapNumImport]['size_y'])

print(finalImg.shape)

finalImg = globalImageProcessing(finalImg, mapNumImport)

#Get heightmap (RED channel)
heightmap = finalImg[:,:,2]

#Save finals images
cv2.imwrite(outputFolder + mapChoice[mapNumImport]['outputName'] + ".png", finalImg)
cv2.imwrite(outputFolder + mapChoice[mapNumImport]['outputName'] + "_heightmap.png", heightmap)
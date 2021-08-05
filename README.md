# The Cycle Umap Exporter #  
  
[License](LICENSE)

---   
  
## What that program does and does not do ##  

- :heavy_check_mark: Recreating a whole Umap from The Cycle
- :x: Exporting models  
- :x: Texturing models  
- :x: Placing Skeletal Mesh at their right place  
- :x: __Exporting other Umap for other games than The Cycle__ 
  
---  
  
## How to use it ##

1. Get the Umap file you want with [FModel](https://github.com/iAmAsval/FModel) in JSON format  
2. Export the whole game in a folder \(Or just the model that are in the map\)  
3. [Change the config file](config.json)  
4. Run the script in Blender  
5. Tada !  
  
---
  
## Config file ##  
  
```json
{
    "umapPath": "",
    "exportedGameAssetsPath": "",
    "deleteExistingScene": true,
    "texturingModels": true
}
```
  
| Parameter | Type | Description |
| --- | --- | --- |
| __umapPath__                  | String | Path of the Umap file in JSON |
| __exportedGameAssetsPath__    | String | Path where you exported the whole game |
| __deleteExistingScene__       | Boolean | If true, will delete everything that was in the blender file |
| __texturingModels__           | Boolean | If true, will try to texture the models |
  
---
  
## Things that I work on ##  

- [x] Removing duplicate materials in Blender
- [] Re-creating the materials
- [] Optimisation
- [] Exporting models and materials that are only needed
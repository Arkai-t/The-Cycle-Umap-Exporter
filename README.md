# The Cycle Umap Exporter #  
  
[License](LICENSE)

---   
  
## What that program does and does not do ##  

- :heavy_check_mark: Recreating a whole Umap from The Cycle
- :x: Exporting models
- :x: Exporting grounds    
- :x: Texturing models  
- :x: Placing Skeletal Mesh at their right place  
- :x: __Exporting other Umap for other games than The Cycle__ 
  
---  
  
## How to use it ##

1. Get the Umap file you want with [FModel](https://github.com/iAmAsval/FModel) in JSON format  
2. Export the whole game in a folder \(Or just the model that are in the map\) with [UModel](https://www.gildor.org/en/projects/umodel)  
3. [Change the config file](https://github.com/Arkait53/The-Cycle-Umap-Exporter/blob/main/README.md#config-file)  
4. Run the script in Blender and don't forget to update the [config file path in the script](https://github.com/Arkait53/The-Cycle-Umap-Exporter/blob/669744d5b8ab2bf11eb52111a07c832a4a688cbb/umapBuilder.py#L17)  
5. Tada !  

All files must be in `.gltf` for models and `.png` for textures

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

__All path must be absolute !__  
  
| Parameter | Type | Description |
| --- | --- | --- |
| __umapPath__                  | String | Path of the Umap file in JSON |
| __exportedGameAssetsPath__    | String | Path where you exported the whole game |
| __deleteExistingScene__       | Boolean | If true, will delete everything that was in the blender file |
| __texturingModels__           | Boolean | If true, will try to texture the models |
  
---
  
## Things that I work on ##  

- [x] Removing duplicate materials in Blender
- [ ] Re-creating the materials
- [ ] Optimisation
- [ ] Exporting models and materials that are only needed
- [ ] Allowing more models format

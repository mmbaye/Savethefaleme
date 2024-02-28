```javascript

// define point geometry before running this code and chose 3 or more polygone of  pure pixels water and
// mixed pixels with sediment for reference data
Map.centerObject(point,14)
Map.setOptions('hybrid')
var startDate = '2016-07-01';
var endDate = '2024-07-30';
var CLOUD_COVERAGE_ASSESSMENT =20 
var waterThreshold =0


// Calculate Turbidity using NDSSI

var vegetationIndex=function(image){
            var ndvi  = image.normalizedDifference(['B8','B4']).rename('NDVI')
            var ndwia = image.normalizedDifference(['B8','B11']).rename('NDWIA')
            var ndssi= image.normalizedDifference(['B3','B8']).rename('NDSSI')
            var ndbi  = image.normalizedDifference(["B11","B8"]).rename("NDBI")
            var ic    = image.normalizedDifference(['B4','B3']).rename('IC')
            var nbai  = image.expression('((swir2-nir)/blue) / ((swir2+nir)/blue)',
                          { swir2: image.select('B12'),
                          nir : image.select('B8'),
                          blue : image.select('B2') }).rename('NBAI');
            var ri    = image.expression('(red*red) / (green*green)',
                          {red: image.select('B4'),
                          green: image.select('B3')}).rename('RI') ;
            var ibb   = image.expression('sqrt(((red*red) + (green*green) +(nir*nir))/3)',
                          {red: image.select('B4'),
                          green: image.select('B3'),
                          nir:image.select('B8') } ).rename('IBB') ;
            var iba   = image.expression('sqrt(((red*red) + (green*green))/2)', 
                         {red: image.select('B4'),
                         green: image.select('B3')}).rename('IBA');
            var chl_a = image.expression(
                    '3.4*(green-blue+nir)/(red)+2.37',
                  {
                      nir:image.select(['B8']),
                      red:image.select(['B4']),
                      blue:image.select(['B2']),
                      green:image.select(['B3'])
                    }).rename('CHL_a');
                    

            return image.addBands([chl_a,ndvi,ndwia,ndssi,ic]).copyProperties(image, ['system:time_start']);
                         
          }   



var waterfunction = function(image){

  var water01 = image.select('NDVI').lt(waterThreshold);
  image = image.updateMask(water01).addBands(water01);
  
  var area = ee.Image.pixelArea();
  var waterArea = water01.multiply(area).rename('waterArea');
  image = image.addBands(waterArea);

  var stats = waterArea.reduceRegion({
    reducer: ee.Reducer.sum(), 
    geometry: regions, 
    scale: 10,
    bestEffort:true
  });
  
  return image.set('stats', stats);

};

/********************************* Sentinel-2 image processing *******************************************
 *    sentinel 2
 * **********************************************************************************************************/  
 
var collection=ee.ImageCollection('COPERNICUS/S2')
        .filterDate(startDate,endDate)
        .filterBounds(regions)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', CLOUD_COVERAGE_ASSESSMENT))
        .select('B.*')
        .map(function(image){return image.clip(regions).divide(10000).copyProperties(image,['system:time_start'])})
        .map(vegetationIndex)
        .map(waterfunction)


// Data collection Explorer
print(collection.first().bandNames())
print(collection.size())

var vizp={ bands: ["NDWIA","NDVI","IC"],gamma: 0.517,max: 0.2512562870979309,min: -0.18520517647266388,opacity: 0.64}

Map.addLayer(collection.first(),vizp,'image')


var aoi=ee.FeatureCollection([water1, water2,water_sed ])




var chart21=ui.Chart.image.seriesByRegion({
		imageCollection:collection,
		regions:aoi,
		reducer:ee.Reducer.mean(),
		band:"NDSSI",
		scale:10,
		seriesProperty:'class'
})

print(chart21)

//  Select time window of change of NDSSI in relation of SSC
var img=collection.filterDate('2022-01-01','2022-01-31').mean()

var ftable = img.sampleRegions({
  collection: aoi, 
  properties: ['class'],  
  scale: 10,
  tileScale:2
});


print(ftable.limit(10))


var chart=function(f,xband,yband){
  
  var graphx=ui.Chart.feature.groups({
    features:f, 
    xProperty: xband,
    yProperty: yband,
    seriesProperty:'class'
    
  }).setChartType('ScatterChart')
  
  return graphx
  
  
}

// // // // ::::::::::  Exploring the dataset you can export them ::::::::::::::::::::::::::::::::::::
print(chart(ftable, 'NDSSI','CHL_a'))
print(chart(ftable, 'NDSSI','NDVI'))
print(chart(ftable, 'NDSSI','IC'))
print(chart(ftable, 'NDSSI','NDWIA'))
```

![](https://github.com/mmbaye/Savethefaleme/blob/main/images/images3.jpeg)

### Steps 

1. **Define Area:** A polygon representing the river section you're studying.
2. **Sentinel-2:** Loads the suitable image collection and applies date, location, and cloud filtering.
3. **NDSSI Calculation:** A simple function using the Normalized Difference Suspended Sediment Index.
4. **Apply across time:** Maps the function to all images for time-series analysis.
5. **Chart:** Creates a chart of average sediment level (turbidity) over time.
6. **Map:** Visualizes a recent image with a color-coded turbidity layer.

![](https://github.com/mmbaye/Savethefaleme/blob/main/images/image1.jpeg)


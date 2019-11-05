import bpy
import os
import json

# Load files
#need to use absolute path
vectorFilename = 'route_proj.geojson'
vectorDirectory = '/Users/Nick/Documents/2019/thesis/blender'
vectorFullPath = os.path.join(vectorDirectory,vectorFilename)

#bounds of raster
geoBounds = {"upperLeft" : [-498551.735,  467621.695], 
             "bottomRight": [409733.139, -344711.568]} 

bounds3D = {"upperLeft" : [-1, 1.091], 
             "bottomRight": [1, -1.091]}


def points3D(points):
    converted = []
    for point in points:
        percentageX = (point[0] - geoBounds["upperLeft"][0]) / (geoBounds["bottomRight"][0] - geoBounds["upperLeft"][0])
        convertedX = bounds3D["upperLeft"][0] + percentageX * (bounds3D["bottomRight"][0] - bounds3D["upperLeft"][0])
        percentageY = (geoBounds["upperLeft"][1] - point[1]) / (geoBounds["upperLeft"][1] - geoBounds["bottomRight"][1])
        convertedY = bounds3D["upperLeft"][1] - percentageY * (bounds3D["upperLeft"][1] - bounds3D["bottomRight"][1])
        print(percentageY)
        print(convertedY)
        converted.append([convertedX,convertedY, 0])
    return converted

# open vector data
with open(vectorFullPath) as f:
    vectorData = json.load(f)

unconverted = vectorData['features'][0]['geometry']['coordinates']
vertices = points3D(unconverted)

# create curve datablock
curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('NURBS')
polyline.points.add(len(vertices))
for i, coord in enumerate(vertices):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)
    
# create object
curveOb = bpy.data.objects.new('myCurve', curveData)

#attach to scene
bpy.context.scene.collection.objects.link(curveOb)

import bpy

nPixelCountX = 8
nPixelCountY = 8

nMatrixSizeX = 64.8
nMatrixSizeY = 64.8
nMatrixSizeZ = 3.05

nMatrixBorderX = 1
nMatrixBorderY = 1
nMatrixBorderZ = 2.5

nMatrixFrameX = nMatrixSizeX + nMatrixBorderX
nMatrixFrameY = nMatrixSizeY + nMatrixBorderY
nMatrixFrameZ = nMatrixSizeZ + nMatrixBorderZ

nPixelSpaceX = 1
nPixelSpaceY = 1
nPixelSpaceZ = 2.95

nPixelSizeX = 4.9 + nPixelSpaceX
nPixelSizeY = 4.9 + nPixelSpaceY
nPixelSizeZ = 1.6 + nPixelSpaceZ

nSpaceX = nMatrixSizeX / nPixelCountX - nPixelSizeX
nSpaceY = nMatrixSizeY / nPixelCountY - nPixelSizeY

# clean up
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# create frame
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "FRAME"
oFrame = bpy.context.scene.objects.get("FRAME")
oFrame.location = (0, 0, nMatrixFrameZ / 2)
oFrame.dimensions = (nMatrixFrameX, nMatrixFrameY, nMatrixFrameZ)


# create board
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "BOARD"

oBoard = bpy.context.scene.objects.get("BOARD")
nMatrixSizeT = nMatrixSizeZ
nMatrixSizeZ = nMatrixSizeT + nMatrixBorderZ + 1
oBoard.location = (0, 0, nMatrixSizeZ / 2)
oBoard.dimensions = (nMatrixSizeX, nMatrixSizeY, nMatrixSizeZ)

oModifier = oFrame.modifiers.new("mod_" + oBoard.name, 'BOOLEAN')
oModifier.object = oBoard
oModifier.operation = 'DIFFERENCE'
bpy.ops.object.modifier_apply({"object": oFrame},apply_as='DATA',modifier=oModifier.name)

nMatrixSizeZ = nMatrixSizeT
oBoard.location = (0, 0, nMatrixSizeZ / 2)
oBoard.dimensions = (nMatrixSizeX, nMatrixSizeY, nMatrixSizeZ)


# create pixels
for y in range(0, nPixelCountY):
    for x in range(0, nPixelCountX):
        sPixelName = "PIXEL"
        bpy.ops.mesh.primitive_cube_add(size=1)
        bpy.context.object.name = sPixelName
        
        oPixel = bpy.context.scene.objects.get(sPixelName)
        oPixel.location = (-(nPixelCountX * .5 - 1) * (nPixelSizeX + nSpaceX) + (nPixelSizeX + nSpaceX) * -.5 + x * nPixelSizeX + nSpaceX * x, -(nPixelCountY * .5 - 1) * (nPixelSizeY + nSpaceY) + (nPixelSizeY + nSpaceY) * -.5 + y * nPixelSizeY + nSpaceY * y, nMatrixSizeZ * .5 + nPixelSizeZ *.5)
        oPixel.dimensions = (nPixelSizeX, nPixelSizeY, nPixelSizeZ + nPixelSpaceZ)

        oModifier = oBoard.modifiers.new("mod_" + oPixel.name, 'BOOLEAN')
        oModifier.object = oPixel
        oModifier.operation = 'DIFFERENCE'
        bpy.ops.object.modifier_apply({"object": oBoard},apply_as='DATA',modifier=oModifier.name)
        
        bpy.data.objects[sPixelName].select_set(True)
        bpy.ops.object.delete()

# add bevels
nBevelZ=nMatrixSizeZ + nMatrixBorderZ

# bevel left
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "BEVELLEFT"
oBevelLeft = bpy.context.scene.objects.get("BEVELLEFT")
oBevelLeft.location = ((nMatrixSizeX + nBevelZ + 1) * -0.5, 0, nBevelZ * .5)
oBevelLeft.dimensions = (nBevelZ, nMatrixSizeY + nMatrixBorderY + 2 * nBevelZ, nBevelZ)

# bevel bottom
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "BEVELBOTTOM"
oBevelBottom = bpy.context.scene.objects.get("BEVELBOTTOM")
oBevelBottom.location = (0, (nMatrixSizeX + nBevelZ + 1) * -0.5, nBevelZ * .5)
oBevelBottom.dimensions = (nMatrixSizeY + nMatrixBorderY + 2 * nBevelZ, nBevelZ, nBevelZ)
    
# bevel right
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "BEVELRIGHT"
oBevelRight = bpy.context.scene.objects.get("BEVELRIGHT")
oBevelRight.location = (-(nMatrixSizeX + nBevelZ + 1) * -0.5, 0, nBevelZ * .5)
oBevelRight.dimensions = (nBevelZ, nMatrixSizeY + nMatrixBorderY + 2 * nBevelZ, nBevelZ)

# bevel top
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "BEVELTOP"
oBevelTop = bpy.context.scene.objects.get("BEVELTOP")
oBevelTop.location = (0, -(nMatrixSizeX + nBevelZ + 1) * -0.5, nBevelZ * .5)
oBevelTop.dimensions = (nMatrixSizeY + nMatrixBorderY + 2 * nBevelZ, nBevelZ, nBevelZ)

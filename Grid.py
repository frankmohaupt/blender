import bpy

nHoleCountX = 8
nHoleCountY = 8

nExtraSpace = 0

nGridDimensionX = 64.8
nGridDimensionY = 64.8
nGridDimensionZ = 3.05

nHoleDimensionX = 4.9 + nExtraSpace
nHoleDimensionY = 4.9 + nExtraSpace

nGridSpaceX = nGridDimensionX / nHoleCountX - nHoleDimensionX
nGridSpaceY = nGridDimensionY / nHoleCountY - nHoleDimensionY

# cleanup
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# add the grid
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.active_object.name = "GRID"

oGrid = bpy.data.objects.get("GRID")
oGrid.dimensions = (nGridDimensionX, nGridDimensionY, nGridDimensionZ)
oGrid.location = (0, 0, nGridDimensionZ * .5)

for y in range(0, nHoleCountY):
    for x in range(0, nHoleCountX):
        n = y * nHoleCountX + x
        sHoleName = "HOLE:" + str(n).zfill(3)
        bpy.ops.mesh.primitive_cube_add(size=1)
        bpy.context.active_object.name = sHoleName

        oHole = bpy.data.objects.get(sHoleName)
        oHole.dimensions = (nHoleDimensionX, nHoleDimensionY, nGridDimensionZ + 1)
        nLocationX = round(nGridDimensionX * .5 - nHoleDimensionX * .5 - nGridSpaceX * .5 - x * (nGridSpaceX + nHoleDimensionX), 2)
        nLocationY = round(nGridDimensionY * .5 - nHoleDimensionY * .5 - nGridSpaceY * .5 - y * (nGridSpaceY + nHoleDimensionY), 2)
        print("N=" + str(n))
        print("X=" + str(nLocationX))
        print("Y=" + str(nLocationY))
        oHole.location = (nLocationX, nLocationY , nGridDimensionZ * .5)
        sModifierName = "MOD:" + sHoleName

        # add mofifier
        oGrid.modifiers.new(sModifierName, type="BOOLEAN")
        oGrid.modifiers[sModifierName].operation = "DIFFERENCE"
        oGrid.modifiers[sModifierName].object = oHole
        bpy.ops.object.modifier_apply({"object": oGrid}, apply_as='DATA', modifier=sModifierName)

        bpy.data.objects[sHoleName].select_set(True)
        bpy.ops.object.delete()

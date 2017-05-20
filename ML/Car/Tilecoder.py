import math

#globals
numTiles = 10 * 9 * 9
numTilings = 10

# -1.2 <= position <= 0.5
# -0.07 <= velocity <= 0.07
tilingSize = 8 # (subset)
# tileSize = (max - min)/tilingSize
positionTileMovementValue = -0.2125/numTilings
velocityTileMovementValue = -0.0175/numTilings

# x = position, y = velocity
def tilecode(x,y,tileIndices):
    
    # update position
    x = x + 1.2
    # update velocity
    y = y + 0.07

    for i in range (numTilings):
        
        positionMovementConstant = i * positionTileMovementValue
        velocityMovementConstant = i * velocityTileMovementValue
        
        xcoord = int(tilingSize * (x- positionMovementConstant)/1.7)
        ycoord = int(tilingSize * (y- velocityMovementConstant)/0.14)

        tileIndices[i] = i * 81 + (ycoord * 9 + xcoord)
    
    
def printTileCoderIndices(x,y):
    tileIndices = [-1]*numTilings
    tilecode(x,y,tileIndices)
    print ('Tile indices for input ({}, {}) are : {}'.format(x, y, tileIndices))


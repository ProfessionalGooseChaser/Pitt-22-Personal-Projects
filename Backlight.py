from PIL import ImageGrab
import time
from multiprocessing import Process

start = time.time()

class light():
    def __init__(self, minX, minY, rangeX, rangeY):
        self.rgb = ()
        self.minX = minX
        self.rangeX = rangeX +1
        self.minY = minY
        self.rangeY = rangeY +1

    def __str__(self) -> str:
        return str(self.rgb)

    def average(self):
        sqr = ImageGrab.grab(bbox = (self.minX, self.minY, self.minX + self.rangeX, self.minY + self.rangeY))
        px = sqr.load()
        totalRGB = (0, 0, 0)
        for x in range(self.rangeX):
            for y in range(self.rangeY):
                totalRGB = tuple(map(sum, zip(px[x,y], totalRGB))) #Stop calling this 225 times. Call it once
                print(x, y)
        self.rgb = tuple(ti/(self.rangeX * self.rangeY) for ti in totalRGB)

SCREEN = (1440, 900)
PERIMETER = 1440 * 2 + 900 * 2
lights = []

for i in range(16): #90pixels for range 
    temp = light(i*90, 0, 90, 25) #top row
    lights.append(temp)
    temp2 = light(i*90, 1415, 90, 25) #bottom row
    lights.append(temp2)

for j in range(10):
    temp = light(0, j*90, 25, 90) #Left side
    lights.append(temp)
    temp2 = light(875, j*90, 25, 90)
    lights.append(temp2) #right side

#Using processes to optimize
#creating a process for each light object
processes = []

end = time.time()
print(str(end-start))

#1mil - 48.25s
#100k - 5.17s
#10k - 0.78s
#1k - 0.4s
#100 - 0.4s

#some notes, I'm not too worried about time rn. I do want to eventually use parallelt processing to update all of the lights at onces

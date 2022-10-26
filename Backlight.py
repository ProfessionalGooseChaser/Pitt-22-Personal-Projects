from PIL import ImageGrab
import time

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



temp = light(0, 0, 100, 100) # Is creating the object causing the 0.39 time?
temp2 = light(0, 0, 100, 100)
temp.average()
temp2.average()
print(temp.rgb)
print(temp2.rgb)

end = time.time()
print(str(end-start))

#1mil - 48.25s
#100k - 5.17s
#10k - 0.78s
#1k - 0.4s
#100 - 0.4s

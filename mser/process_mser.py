import cv2
from matplotlib import pyplot as plt
import numpy as np
FILE = "regions.data"
imfile = 'EstateAgents.jpg'

strip_f = lambda x: x.strip().split(';')
split_f = lambda x: x.split(',')

with open(FILE) as f:
    data = f.readlines()
    data = list(map(strip_f,data))
    points = []
    
    for point in data:
        point[0]=point[0].split(',')
        point[1]=point[1].split(',')
        points.append(point)
    
    im = cv2.imread(imfile)
    im2 = im.copy()
    im2 = cv2.copyMakeBorder(im2,0,2,0,2,cv2.BORDER_REPLICATE)
    im = cv2.copyMakeBorder(im,0,2,0,2,cv2.BORDER_REPLICATE)
    print(points) 
    for point in points:
        x1 = int(point[0][0])
        y1 = int(point[0][1])
        x2 = int(point[1][0])
        y2 = int(point[1][1])
        for i in range(x1,x2):
            for j in range(y1,y2):
                im2[i][j] = np.array([0, 0, 0])
    
    im3 = im-im2 
    plt.imshow(im3)
    plt.show()

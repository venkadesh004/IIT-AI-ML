import torch    
import cv2
import pandas
import numpy as np
import csv

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
cap = cv2.VideoCapture("Hackathon video.mov")

cv2.namedWindow("Final", cv2.WINDOW_NORMAL)

i = 1

top = (1231, 60)
right = (2570, 429)
bottom = (1547, 1591)
left = (33, 718)

center = (1350, 573)

topRight = (1813, 220)
topLeft = (740, 336)
bottomLeft = (662, 1077)
bottomRight = (2166, 896)

quadrant1 = [top, topLeft, center, topRight]
quadrant2 = [topLeft, left, bottomLeft, center]
quadrant3 = [center, bottomLeft, bottom, bottomRight]
quadrant4 = [topRight, center, bottomLeft, right]

ms = []
m = 0

def triangleArea(a, b, c):
    area = (a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
    if area < 0:
        area *= -1
    # print("Area: ", area/2)
    return area/2

def rectArea(quadrant):
    tr1 = triangleArea(quadrant[0], quadrant[1], quadrant[2])
    tr2 = triangleArea(quadrant[0], quadrant[3], quadrant[2])

    # print("Rect Area: ", (tr1+tr2)/2)

    return tr1+tr2

def splitTri(a, quadrant):
    tr1 = triangleArea(a, quadrant[0], quadrant[1])
    tr2 = triangleArea(a, quadrant[1], quadrant[2])
    tr3 = triangleArea(a, quadrant[2], quadrant[3])
    tr4 = triangleArea(a, quadrant[3], quadrant[0])

    areaSum = tr1+tr2+tr3+tr4

    rectangleArea = rectArea(quadrant)

    # print("Total: " ,areaSum, rectangleArea)

    if areaSum > rectangleArea:
        return False
    else:
        return True

def checkQuadrants(a):
    if splitTri(a, quadrant1):
        return 1
    elif splitTri(a, quadrant2):
        return 2
    elif splitTri(a, quadrant3):
        return 3
    elif splitTri(a, quadrant4):
        return 4
    else:
        return 0

def findPoint(xmin, ymin, xmax, ymax):
    midX = (xmax-xmin)+xmin
    midY = (ymax-ymin)+ymin
    return (midX, midY)

def checkSlope(a):
    global ms
    global m

    ms.append(a)

    print(ms, m)

    if len(ms) > 1:
        print(ms[len(ms)-1])
        print(ms[len(ms)-2])
        print(ms[len(ms)-1])
        print(ms[len(ms)-2])
        if m > 1:
            if (ms[len(ms)-1][1]-ms[len(ms)-2][1])/(ms[len(ms)-1][0]-ms[len(ms)-2][0]) < 1:
                m = (ms[len(ms)-1][1]-ms[len(ms)-2][1])/(ms[len(ms)-1][0]-ms[len(ms)-2][0])
                return True
            else:
                m = (ms[len(ms)-1][1]-ms[len(ms)-2][1])/(ms[len(ms)-1][0]-ms[len(ms)-2][0])
        else:
            if (ms[len(ms)-1][1]-ms[len(ms)-2][1])/(ms[len(ms)-1][0]-ms[len(ms)-2][0]) > 1:
                m = (ms[len(ms)-1][1]-ms[len(ms)-2][1])/(ms[len(ms)-1][0]-ms[len(ms)-2][0])
                return True
            else:
                m = (ms[len(ms)-1][1]-ms[len(ms)-2][1])/(ms[len(ms)-1][0]-ms[len(ms)-2][0])  

    return False  
    
while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame[..., ::-1])

    if (results.pandas().xyxy[0].name[0] == "sports ball"):
        print(i)
        # print(results.pandas().xyxy[0])

        xmin = int(results.pandas().xyxy[0].xmin[0])
        ymin = int(results.pandas().xyxy[0].ymin[0])
        xmax = int(results.pandas().xyxy[0].xmax[0])
        ymax = int(results.pandas().xyxy[0].ymax[0])

        # print(results.pandas().xyxy[0].xmin[0], results.pandas().xyxy[0].ymin[0])
        # print(results.pandas().xyxy[0].xmax[0], results.pandas().xyxy[0].ymax[0])

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 4)

        a = findPoint(xmin, ymin, xmax, ymax)

        result = checkQuadrants(a)

        print(result)

        touch = checkSlope(result)

        print(touch)

        # cv2.imwrite('./images/{}.jpg'.format(str(i)), frame)

    else:

        ms = []
        m = 0

    cv2.imshow("Final", frame)

    key = cv2.waitKey(10)

    if key == 27:
        break

    i += 1
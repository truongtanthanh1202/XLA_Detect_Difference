import cv2
import numpy as np
import argparse

def edgePreprocess(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Temp = cv2.Canny(imgray, 150, 200)
    #normalize by smoothing and erosion + dilation
    Temp = cv2.dilate(Temp, None)
    Temp = cv2.erode(Temp, None)
    kernel_c = np.ones((5, 5), np.uint8)
    kernel_o = np.ones((1, 1), np.uint8)
    Temp = cv2.morphologyEx(Temp, cv2.MORPH_CLOSE, kernel_c)
    Temp = cv2.morphologyEx(Temp, cv2.MORPH_OPEN, kernel_o)
    return Temp

#calculate the average color in an area of an object
def colorArea(x1,y1,x2,y2, img):
    # Extract the pixels within the rectangular area
    roi = img[y1:y2, x1:x2]

    # Calculate the mean value of the pixel values for each color channel (R, G, B)
    mean_color = np.mean(roi, axis=(0, 1)).astype(int)

    # Print and return the mean color value as a tuple (R, G, B)
    # print(f"Mean color value: {mean_color}")
    mean_color = tuple(mean_color)
    return mean_color


#create a new image according to the set parameters
def CreateImage(path, level, limit):
    img = cv2.imread(path)
    test = img.copy()

    thresh = edgePreprocess(img)
    contour_info = [(c, cv2.contourArea(c)) for c in cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]]
    print('Number of contours =  ' + str(len(contour_info)))

    area = set([contour[1] for contour in contour_info])
    area = sorted(area)
    # print('List area: ' + str(area))

    #Define parameters for game level
    lenght = len(area)
    if level == 'easy':
        minn, maxx = area[int(lenght / 2) + int(lenght / 3) + 1], area[lenght - 1]
    elif level == 'medium':
        minn, maxx = area[int(lenght / 2) + 1], area[int(lenght / 2) + int(lenght / 3)]
    elif level == 'hard':
        minn, maxx = area[0], area[int(lenght / 2)]

    Limit = limit
    print("Min - Max: " + str(minn) + " " + str(maxx))
    print("Limit: " + str(Limit))
    ####

    def myFunc(e):
        return e[1]

    contour_info.sort(reverse=True, key=myFunc)
    for contour in contour_info:
        area = contour[1]
        al = np.random.randint(1, 100)
        if area >= minn and area <= maxx and al % 3 == 0:
            x, y, w, h = cv2.boundingRect(contour[0])
            R, G, B = colorArea(x, y, x+w, y+h, test)
            # print(str(R) + " " + str(G) + " " + str(B))

            if level == 'easy':
                new_color = (np.random.uniform(0, 255), np.random.uniform(0, 255), np.random.uniform(0, 255))
            elif level == 'medium':
                new_color = (int(R), int(G), int(B))
            elif level == 'hard':
                new_color = (int(R), int(G), int(B))

            cv2.fillPoly(img, [contour[0]], new_color)
            Limit = Limit - 1
            if (Limit == 0):
                break

    # Export ouput image
    cv2.imwrite('./Difference/Source.jpg', test)
    cv2.imwrite('./Difference/Replaced.jpg', img)







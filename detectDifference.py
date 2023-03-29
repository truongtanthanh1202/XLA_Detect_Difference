from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import numpy as np
import cv2


def DetectDifference():
    # load the two input images
    imgA = cv2.imread('./Difference/Source.jpg')
    imgB = cv2.imread('./Difference/Replaced.jpg')

    # resize image
    imgA = imutils.resize(imgA, height=600)
    imgB = imutils.resize(imgB, height=600)
    img_height = imgA.shape[0]

    # convert the images to grayscale
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cv2.imwrite('./Difference/Thresh.jpg', thresh)
    cv2.imwrite('./Difference/Diff.jpg', diff)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imgA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imgB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # show the output images
    imgThresh = cv2.imread('./Difference/Thresh.jpg')
    imgDiff = cv2.imread('./Difference/Diff.jpg')
    x = np.zeros((img_height, 10, 3), np.uint8)
    source = np.hstack((imgA, x, imgB))
    difference = np.hstack((imgThresh, x, imgDiff))
    cv2.imshow("Difference", difference)
    cv2.imshow("Source + Replaced", source)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

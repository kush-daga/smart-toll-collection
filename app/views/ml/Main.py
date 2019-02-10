# Main.py

import cv2
import numpy as np
import os
from PIL import Image

from app.views.ml import DetectChars
from app.views.ml import DetectPlates
from app.views.ml import PossiblePlate
import glob

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################


def main():

    # attempt KNN training
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return  # and exit program
    # end if
    # im = Image.open("LicPlateImages/25.jpg")
    # rgb_im = im.convert("RGB")
    # rgb_im.save("LicPlateImages/6.png", "PNG")
    print(os.listdir())
    imgOriginalScene = cv2.imread("LicPlateImages/2.png")  # open image 
    # cv2.imshow("imgOriginalScene", imgOriginalScene)
    # os.system("pause")
    if imgOriginalScene is None:  # if image was not read successfully
        # print error message to std out
        print("\nerror: image not read from file \n\n")
        # pause so user can see error message
        os.system("pause")
        return  # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(
        imgOriginalScene
    )  # detect plates
    # print(listOfPossiblePlates[0])
    listOfPossiblePlates = DetectChars.detectCharsInPlates(
        listOfPossiblePlates
    )  # detect chars in plates

    # show scene image
    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        # inform user no plates were found
        print("\nno license plates were detected\n")
    else:  # else
        # if we get in here list of possible plates has at leat one plate

        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(
            key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True
        )

        # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        # show crop of plate and threshold of plate
        cv2.imshow("imgPlate", licPlate.imgPlate)
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:  # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return  # and exit program
        # end if

        # draw red rectangle around plate
        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)

        # write license plate text to std out
        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")

        # write license plate text on the image
        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)

        # re-show scene image
        cv2.imshow("imgOriginalScene", imgOriginalScene)

        # write image out to file
        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

    # end if else

    cv2.waitKey(0)  # hold windows open until user presses a key

    return licPlate.strChars


# end main

###################################################################################################


def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    # get 4 vertices of rotated rect
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)

    cv2.line(
        imgOriginalScene,
        tuple(p2fRectPoints[0]),
        tuple(p2fRectPoints[1]),
        SCALAR_RED,
        2,
    )  # draw 4 red lines
    cv2.line(
        imgOriginalScene,
        tuple(p2fRectPoints[1]),
        tuple(p2fRectPoints[2]),
        SCALAR_RED,
        2,
    )
    cv2.line(
        imgOriginalScene,
        tuple(p2fRectPoints[2]),
        tuple(p2fRectPoints[3]),
        SCALAR_RED,
        2,
    )
    cv2.line(
        imgOriginalScene,
        tuple(p2fRectPoints[3]),
        tuple(p2fRectPoints[0]),
        SCALAR_RED,
        2,
    )


# end function

###################################################################################################


def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    # this will be the center of the area the text will be written to
    ptCenterOfTextAreaX = 0
    ptCenterOfTextAreaY = 0

    # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginX = 0
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    # choose a plain jane font
    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    # base font scale on height of plate area
    fltFontScale = float(plateHeight) / 30.0
    # base font thickness on font scale
    intFontThickness = int(round(fltFontScale * 1.5))

    textSize, baseline = cv2.getTextSize(
        licPlate.strChars, intFontFace, fltFontScale, intFontThickness
    )  # call getTextSize

    # unpack roatated rect into center point, width and height, and angle
    (
        (intPlateCenterX, intPlateCenterY),
        (intPlateWidth, intPlateHeight),
        fltCorrectionAngleInDeg,
    ) = licPlate.rrLocationOfPlateInScene

    # make sure center is an integer
    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)

    # the horizontal location of the text area is the same as the plate
    ptCenterOfTextAreaX = int(intPlateCenterX)

    # if the license plate is in the upper 3/4 of the image
    if intPlateCenterY < (sceneHeight * 0.75):
        # write the chars in below the plate
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(
            round(plateHeight * 1.6)
        )
    # else if the license plate is in the lower 1/4 of the image
    else:
        # write the chars in above the plate
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(
            round(plateHeight * 1.6)
        )
    # end if

    # unpack text size width and height
    textSizeWidth, textSizeHeight = textSize

    # calculate the lower left origin of the text area
    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))
    # based on the text area center, width, and height
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))

    # write the text on the image
    cv2.putText(
        imgOriginalScene,
        licPlate.strChars,
        (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY),
        intFontFace,
        fltFontScale,
        SCALAR_YELLOW,
        intFontThickness,
    )


# end function


###################################################################################################
if __name__ == "__main__":
    main()

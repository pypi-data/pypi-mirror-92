import os

def get_dir_filepaths(directorypath):
    """
    This function appends the absolute file paths from within a directory.

        Args:
            directorypath(string): Path to the directory
        Returns:
            dirpaths(list): List of file paths from within the directory 
    """

    paths = os.listdir(directorypath)
    dirpaths = []

    for path in paths:
        dirpaths.append("{}\\{}".format(directorypath, path))
    return dirpaths


def blankKinematicsDict():
    """ Returns a dictionary template for the kinematic variables, with 100 samples. """

    blankKINS = {
            'Pelvic Tilt Left': [0]*100, 
            'Pelvic Tilt Right': [0]*100, 
            'Hip Flexion Left': [0]*100, 
            'Hip Flexion Right': [0]*100, 
            'Knee Flexion Left': [0]*100, 
            'Knee Flexion Right': [0]*100, 
            'Ankle Dorsiflexion Left': [0]*100, 
            'Ankle Dorsiflexion Right': [0]*100, 
            'Pelvic Obliquity Left': [0]*100, 
            'Pelvic Obliquity Right': [0]*100, 
            'Hip Abduction Left': [0]*100, 
            'Hip Abduction Right': [0]*100, 
            'Pelvic Rotation Left': [0]*100, 
            'Pelvic Rotation Right': [0]*100, 
            'Hip Rotation Left': [0]*100, 
            'Hip Rotation Right': [0]*100, 
            'Foot Progression Left': [0]*100, 
            'Foot Progression Right': [0]*100
        }
    return blankKINS

def blankGPSdict():
    blankGPS = {
            'Pelvic Tilt Left': 0, 
            'Pelvic Tilt Right': 0, 
            'Hip Flexion Left': 0, 
            'Hip Flexion Right': 0, 
            'Knee Flexion Left': 0, 
            'Knee Flexion Right': 0, 
            'Ankle Dorsiflexion Left': 0, 
            'Ankle Dorsiflexion Right': 0, 
            'Pelvic Obliquity Left': 0, 
            'Pelvic Obliquity Right': 0, 
            'Hip Abduction Left': 0, 
            'Hip Abduction Right': 0, 
            'Pelvic Rotation Left': 0, 
            'Pelvic Rotation Right': 0, 
            'Hip Rotation Left': 0, 
            'Hip Rotation Right': 0, 
            'Foot Progression Left': 0, 
            'Foot Progression Right': 0,
            'GPS': 0,
            'GPS Left': 0,
            'GPS Right': 0
        }
    return blankGPS

def rootMeanSquare(reference, subject):
    """ Calculates the root mean square of two list. """

    sumSquares = 0
    for i in range(len(reference)):
        sumSquares += (reference[i]-subject[i])**2
    
    rmsVal = (sumSquares/len(reference))**0.5
    return rmsVal


def calculateGPSvalues(reference_dataset, subject_dataset):
    """ Calculates the GPS and MAP of a subjects kinematics relative to a reference kinematics. """

    gpsValues = {}
    for key in reference_dataset:
        gpsValues[key] = rootMeanSquare(reference_dataset[key], subject_dataset[key])
    
    gps = 0
    gpsL = 0
    gpsR = 0

    for key in gpsValues:
        gps +=  gpsValues[key]

        if "Left" in key:
            gpsL +=  gpsValues[key]
        elif "Right" in key:
            gpsR +=  gpsValues[key]
        else:
            pass
    
    gpsValues["GPS"] = gps/len(reference_dataset)
    gpsValues["GPS Left"] = gpsL/(len(reference_dataset)/2)
    gpsValues["GPS Right"] = gpsR/(len(reference_dataset)/2)
    return gpsValues


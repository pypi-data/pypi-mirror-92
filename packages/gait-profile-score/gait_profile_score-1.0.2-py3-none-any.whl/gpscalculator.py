import json
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import resample 


class exampleInputData:
    def __init__(self):
        return
    
    def kinematicVariables(self):
        """
        Returns a list of the kinematic variables required to calculate the GPS for a gait trial.

        :return kinematicVariables: List of the kinematic variables required to calculate the GPS for a gait trial
        :type kinematicVariables: list
        """
        kinematicVariables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
            'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
            'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
            'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
            'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
            'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
            'Foot Progression Right']

        return kinematicVariables

    def kinematics(self):
        """
        Returns a dictionary to illustrate the structure of the kinematics required (not real kinematic data, just sin waves)
        
        :return kinematics: A dictionary with the set of variables required in the correct format.
        :type kinematics: dict
        """

        values = list(resample(np.sin(range(0,360)), 51))

        kinematicVariables = self.kinematicVariables()

        kinematics = {}
        for key in kinematicVariables:
            kinematics[key] = values
        return kinematics

    def kinematicsJSON(self, directory=None):
        """
        Creates an example kinematics file in the format required for the GPS calculator.

        :param directory: A path to the directory where the example file is to be saved, if left blank it will save in the current working directory
        :type directory: str
        """
        kinematics = self.kinematics()

        if directory != None:
            path = os.path.join(directory,"example_kinematics.json")
        else:
            path = "example_kinematics.json"
        with open(path, 'w') as f:
            json.dump(kinematics, f)
        return

def loadKinematicsJSON(path):
    """
    Retuns the kinematics that were stored in a JSON file.
    :param path: The path (absolute or relative) to the JSON file containin the trial kinematic data
    :type path: str

    :return kinematics: The kinematic data required to calculate the GPS and MAP
    :type kinematics: dict
    """
    try:
        with open(path,'rb') as f:
            kinematics = json.load(f)
    except:
        #raise Exception("Unable to load kinematics from: {}".format(path))
        print("Unable to load kinematics from: {}".format(path))
        kinematics = 0
    return kinematics

class calculateGPS:
    """Calculate the GPS using the reference and subject kinematics dictionaries."""
    def __init__(self, referenceKinematics: dict, subjectKinematics: dict):
        """Constructor method

        :param referenceKinematics: Average kinematic variables for a reference group.
        :type referenceKinematics: dict

        :param subjectKinematics: Kinematic variables for a single subject.
        :type subjectKinematics: dict
        """

        self.refKins = referenceKinematics
        self.subKins = subjectKinematics

        self.gps = {}
        self.calculateGPS()
        return

    def RMS(self, reference: list, subject: list):
        """
        Returns the root mean square of the two input lists

        :param reference: A list of values for a single kinematic variable from the reference dataset.
        :type reference: list

        :param subject: A list of values for a single kinematic variable from the subject dataset.
        :type subject: list

        :return rms: Root mean square of the subject kinematic variable relative to the reference group
        :type rms: float
        """ 
        ref = np.array(reference)
        sub = np.array(subject)
        ss = np.sum((ref-sub)**2)
        rms = np.sqrt(ss/len(ref))
        return rms

    def calculateGPS(self):
        """
        Calculates the GPS variable scores storing in a dictionary
        :return gps: A dictionary containing the GPS variables for the 
        :type gps: dict
        """
        l_var,  r_var, var = [], [], []
        for key, value in self.refKins.items():
            rms = self.RMS(value, self.subKins[key])
            self.gps[key] = rms 
            var.append(rms)
            if "Left" in key:
                l_var.append(rms)
            elif "Right" in key:
                r_var.append(rms)
            else:
                pass

        self.gps["GPS Left"] = np.mean(l_var)
        self.gps["GPS Right"] = np.mean(r_var)
        self.gps["GPS"] = np.mean(var)
        return
    
class referenceGroup:
    """Calculates the average kinematics and the average GPS score for the kinemtic data for a reference group"""

    def __init__(self):
        """Constructor method
        """

        self.initInputDatasets()
        return
    
    def initInputDatasets(self):
        """
        Creates an empty dictionary ready for the reference group kinematimatics to be added.
        """
        self.variables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
        'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
        'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
        'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
        'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
        'Foot Progression Right']

        self.inputKinematics = []
        return

    def checkInputKins(self, inputKins):
        """
        Checks the input kinematics dictionary to ensure the data input is suitable for the GPS calculation.
        :param inputKins: The input kinematics for a given trial.
        :type inputKins: dict

        :return result: A boolean value to confirm if the input data is suitable
        :type result: bool
        """
        checksum = 0 
        keys = list(inputKins.keys())

        for key in keys:
            if key in self.variables:
                checksum = checksum+1
            else:
                print("New key found: {}".format(key))
                return False
        
        if checksum==len(self.variables):
            return True
        else:
            return False

    def loadKinematics(self, jsonPath):
        """
        Loads and checks the data store within the json file located by the path provided.

        :param jsonPath: A string path to the json file that stores the kinematic data
        :type jsonPath: str

        :return kinematics: Kinematic data from the json file
        :type kinematics: dict
        """
        
        kinematics = loadKinematicsJSON(jsonPath)
        if self.checkInputKins(kinematics):
            return kinematics
        else:
            print("Check input data from: {}".format(jsonPath))
            return 0

    def loadInputDataFromList(self, inputPaths):
        """
        Adds the kinematic data from json files using the list input.

        :param inputPaths: List of paths for json files that contain kineamtic data
        :type inputPaths: list
        """
        for path in inputPaths:
            self.inputKinematics.append(self.loadKinematics(path))
        return
    
    def averageVariable(self, groupKinematics):
        """
        Averages the reference group kinematic data for a gait variable.

        :param groupKinematics: A list of kinematic arrays from the reference group for a single kinematic variable
        :type groupKinematics: list

        :return avg: The average value for a kineamtic variabble throughout the gait cycle
        :type avg: list
        """
        data = np.array(groupKinematics)
        avg = np.mean(np.array(data), axis=0)
        return avg

    def calculateAverageKinematics(self):
        """
        Calculates the averages for the gait variables, storing the average kinematic lists to a single dictionary.
        """
        self.avgKinematics = {}
        for var in self.variables:
            varData = []
            for i, kinematics in enumerate(self.inputKinematics):
                varData.append(kinematics[var])    
            varAvg = self.averageVariable(varData)
            self.avgKinematics[var] = varAvg
        return

    def calculateGroupGPS(self):
        """
        Calculates the GPS scores for each set of reference kinematics relative to the reference group.
        """
        cols = self.variables
        cols.append("GPS Left")
        cols.append("GPS Right")
        cols.append("GPS")
        self.groupGPS = pd.DataFrame(columns=cols, data=None)
        for i, subjectKinematics in enumerate(self.inputKinematics):
            subGPS = calculateGPS(self.avgKinematics, subjectKinematics).gps
            self.groupGPS = self.groupGPS.append(subGPS, ignore_index=True)
        return 

    def averageReferenceGPS(self):
        """
        Calculates the average GPS score for the reference group, storing the average values in the avgRefGPS dictionary.
        """
        avgRef={}

        for col in self.groupGPS:
            avgRef[col] = self.groupGPS[col].mean()
        
        self.avgRefGPS ={}
        self.avgRefGPS['GPS'] = avgRef['GPS']

        keys = ['Pelvic Tilt', 'Hip Flexion', 'Knee Flexion', 'Ankle Dorsiflexion', 'Pelvic Obliquity',
        'Hip Abduction', 'Hip Abduction', 'Pelvic Rotation', 'Hip Rotation', 'Foot Progression']
        for key in keys:
            left = "{} Left".format(key)
            right = "{} Right".format(key)

            self.avgRefGPS[key] = (avgRef[left] +avgRef[right] )/2
        return

    def processGroupData(self, inputPaths):
        """
        Calculates the average set of kinematics and the average GPS scores for the reference group.

        :param inputPaths: List of paths for json files that contain kineamtic data
        :type inputPaths: list  
        """

        self.loadInputDataFromList(inputPaths)
        self.calculateAverageKinematics()
        self.calculateGroupGPS()
        self.averageReferenceGPS()
        return

class plotGPS:
    """Plots the GPS and MAP for kinematics input relative to a reference group"""

    def __init__(self, referenceGPS, subjectGPS, subjectname=None, saveplot=None):
        """Contstructor method

        :param referenceGPS: The average GPS scores for a reference group.
        :type referenceGPS: dict

        :param subjectGPS: The GPS scores for a set of kinematics relative to the reference group.
        :type subjectGPS: dict

        :param subjectname: Name or reference for the subject
        :type subjectname: str

        :param saveplot: Desired file path for the plot to be saved to.
        :type saveplot: str
        """
        self.ref = referenceGPS
        self.subject = subjectGPS

        if subjectname!=None:
            self.plotTitle = "{} Gait Profile Score".format(subjectname)
        else:
            self.plotTitle = "Gait Profile Score"

        self.plot()

        if saveplot!=None:
            self.fig.savefig(saveplot)
        return

    def separateVariables(self):
        """Grouping of the kinematic variables, to enable plotting of the left/right/overall."""

        self.left_vars = [self.subject['Pelvic Tilt Left'], self.subject['Hip Flexion Left'], self.subject['Knee Flexion Left'], self.subject['Ankle Dorsiflexion Left'], self.subject['Pelvic Obliquity Left'], self.subject['Hip Abduction Left'], self.subject['Pelvic Rotation Left'], self.subject['Hip Rotation Left'], self.subject['Foot Progression Left'], 0, self.subject['GPS Left']]
        self.right_vars = [self.subject['Pelvic Tilt Right'], self.subject['Hip Flexion Right'], self.subject['Knee Flexion Right'], self.subject['Ankle Dorsiflexion Right'], self.subject['Pelvic Obliquity Right'], self.subject['Hip Abduction Right'], self.subject['Pelvic Rotation Right'], self.subject['Hip Rotation Right'], self.subject['Foot Progression Right'], 0, self.subject['GPS Right']]
        self.ref_vars =  [self.ref['Pelvic Tilt'], self.ref['Hip Flexion'], self.ref['Knee Flexion'], self.ref['Ankle Dorsiflexion'], self.ref['Pelvic Obliquity'], self.ref['Hip Abduction'], self.ref['Pelvic Rotation'], self.ref['Hip Rotation'], self.ref['Foot Progression'], 0, self.ref['GPS']]
        return
    
    def calculateBars(self):
        """Calculation of points required to plot the bars for the GPS diagram. """

        # First number sets the width of the left/right bars
        self.width = 0.35
        self.ref_widths, self.widths, self.pos_l, self.pos_r = [], [] , [], []
        self.xTicks = np.arange(len(self.left_vars))

        for i in range(len(self.xTicks)-1):
            self.widths.append(self.width)
            self.ref_widths.append(2*self.width)
            self.pos_l.append(self.xTicks[i]-self.width/2)
            self.pos_r.append(self.xTicks[i]+self.width/2)
    
        # Set width and position for GPS vars
        self.widths.append((self.width*2)/3)
        self.pos_l.append(self.xTicks[-1]-(self.width*2)/3)
        self.pos_r.append(self.xTicks[-1])

        self.ref_widths.append(self.width*2)
        
        # value, width, position for overall gps 
        self.overall_gps = [self.subject['GPS'], (self.width*2)/3, self.xTicks[-1]+(self.width*2)/3]
        return   

    def plot(self):
        """Plotting of the GPS diagram."""

        ticks = ['Pel tilt', 'Hip flex', 'Knee flex', 'Ank dors', 'Pel obl', 'Hip abd', 'Pel rot', 'Hip rot', 'Foot prog', None,  'GPS']

        self.separateVariables()

        self.calculateBars()

        self.fig, ax = plt.subplots()

        rects1 = ax.bar(self.pos_l, height=self.left_vars, width=self.widths, label='Left')
        rects2 = ax.bar(self.pos_r, height=self.right_vars, width=self.widths, label='Right')
        rectsOVR = ax.bar(self.overall_gps[2], height=self.overall_gps[0], width=self.overall_gps[1], label="Overall")
        rectsREF = ax.bar(self.xTicks, height=self.ref_vars, width=self.ref_widths, label='No pathology', zorder=1)

        ax.set_ylabel('RMS difference (deg)')
        ax.set_title(self.plotTitle)
        ax.set_xticks(self.xTicks)
        ax.set_xticklabels(ticks, rotation=45, ha='right')
        ax.legend()
        self.fig.show()
        return
    
class batchGPS:
    """A class to calculate the GPS scores for a group of subjects relative to a reference group."""

    def __init__(self):
        """Constructor Method"""

        self.variables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
        'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
        'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
        'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
        'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
        'Foot Progression Right', 'GPS Right', 'GPS Left', 'GPS']

        self.batchData = pd.DataFrame(data=None, columns=self.variables)
        return

    def addRefGroup(self):
        """Adding the reference group data to the dataframe containin the GPS data for the subject group that is to be processed"""

        refdata = {'Pelvic Tilt Left':self.referenceGPS['Pelvic Tilt'], 
        'Pelvic Tilt Right':self.referenceGPS['Pelvic Tilt'], 
        'Hip Flexion Left':self.referenceGPS['Hip Flexion'], 
        'Hip Flexion Right':self.referenceGPS['Hip Flexion'], 
        'Knee Flexion Left':self.referenceGPS['Knee Flexion'], 
        'Knee Flexion Right':self.referenceGPS['Knee Flexion'], 
        'Ankle Dorsiflexion Left':self.referenceGPS['Ankle Dorsiflexion'], 
        'Ankle Dorsiflexion Right':self.referenceGPS['Ankle Dorsiflexion'], 
        'Pelvic Obliquity Left':self.referenceGPS['Pelvic Obliquity'], 
        'Pelvic Obliquity Right':self.referenceGPS['Pelvic Obliquity'], 
        'Hip Abduction Left':self.referenceGPS['Hip Abduction'], 
        'Hip Abduction Right':self.referenceGPS['Hip Abduction'], 
        'Pelvic Rotation Left':self.referenceGPS['Pelvic Rotation'], 
        'Pelvic Rotation Right':self.referenceGPS['Pelvic Rotation'], 
        'Hip Rotation Left':self.referenceGPS['Hip Rotation'], 
        'Hip Rotation Right':self.referenceGPS['Hip Rotation'], 
        'Foot Progression Left':self.referenceGPS['Foot Progression'], 
        'Foot Progression Right':self.referenceGPS['Foot Progression'], 
        'GPS Right':self.referenceGPS['GPS'], 
        'GPS Left':self.referenceGPS['GPS'], 
        'GPS':self.referenceGPS['GPS']
        }
        self.batchData.loc["REF_GROUP"] = refdata
        return

    def loadReferenceGroup(self, inputPaths):
        """Loads the reference group average kinematics and average GPS scores, adding the average GPS scores to the dataframe storing subject group GPS scores.

        :param inputPaths: List of paths for json files that contain kineamtic data
        :type inputPaths: list
        """

        refGroup = referenceGroup()
        refGroup.processGroupData(inputPaths)
        self.referenceAvgKins = refGroup.avgKinematics
        self.referenceGPS = refGroup.avgRefGPS
        self.addRefGroup()
        return 
    
    def processSubjectGroup(self, inputPaths, inputReferences=None):
        """Calculates and stores the GPS scores for the subject group in a dataframe.

        :param inputPaths: List of paths for json files that contain kineamtic data
        :type inputPaths: list

        :param inputReferences: A list of reference strs to use for the subjects being processed, if not provided then the default "SUB_1,SUB_2,.." will be used.
        :type inputReferences: list
        """
        self.missing = []

        if inputReferences==None:
            inputReferences=[]
            for i in range(len(inputPaths)):
                inputReferences.append("SUB_{}".format(i+1))

        for index, path in enumerate(inputPaths):
            
            subjectKins = loadKinematicsJSON(path)
            if type(subjectKins)==dict: 
                gps = calculateGPS(self.referenceAvgKins, subjectKins).gps
                self.batchData.loc[inputReferences[index]] = gps
            else:
                self.missing.append(path)
                pass
        return
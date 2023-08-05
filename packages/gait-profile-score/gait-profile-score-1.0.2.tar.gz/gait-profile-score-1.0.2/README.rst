Welcome to Gait Profile Score Calculator’s documentation!
=========================================================

**gpscalc** is a package that can be used to calculate the gait profile
score as stated in Baker et al. 2009. The package requires the gait
trials kinematic data to be stored in a json file using specific
variable names. (Baker, R. et al., 2009. The Gait Profile Score and
Movement Analysis Profile. Gait and Posture, 30(1), pp. 265-269.)
Kinematic gait data has to be in a specific format for the calculation,
the specifics of the format required can be seen using the functions
below to create example JSON files.

How to use the GPS Calculator
=============================
Package Installation
--------------------

::

    pip install gait-profile-score

Create example data in correct format
---------------------------------------

::

    from gpscalculator import exampleInputData

    exampleData = exampleInputData()

    # Kinematic variable labels required
    labels = exampleData.kinematicVariables()
    print(labels)

    # Example of a kinematic dataset
    dataset = exampleData.kinematics()
    print(dataset)
    
    # Save an example of the kinematics JSON file required
    exampleData.kinematicsJSON("chosen/directory")

Processing the reference group data
-----------------------------------

::

    from gpscalculator import referenceGroup

    # List of paths to the reference group kinematics JSON files
    referencePaths = [...]

    referenceData = refernceGroup()
    referenceData.processGroupData(referencePaths)

    # The average of the reference kinematic variables over the gait cycle
    referenceKinematics = referenceData.avgKinematics

    # The average GPS scores of the reference group relative to the average kinematics
    referenceGPS = referenceData.avgRefGPS

Calculation of GPS for a single subject
---------------------------------------

::

    from gpscalculator import calculateGPS

    # The kinematic data for the selected subject
    subjectKinematics = {kinematic data}

    # GPS scores for the subject relative to the reference group average kinematics
    subjectGPS = calculateGPS(referenceKinematics, subjectKinematics).gps

Plotting the GPS diagram
------------------------

::

    from gpscalculator import plotGPS

    plot = plotGPS(referenceGPS, subjectGPS, saveplot="test_gps_plot.png")

Processessing the GPS scores for a subject group
------------------------------------------------

::

    from gpscalculator import batchGPS

    # List of paths to the subject group kinematics JSON files
    subjectPaths = [...]

    subjectGroup = batchGPS()
    subjectGroup.loadReferenceGroup(referencePaths)
    subjectGroup.processSubjectGroup(subjectPaths)

    # Print the dataframe containing the subject group GPS data
    print(subjectGroup.batchData)


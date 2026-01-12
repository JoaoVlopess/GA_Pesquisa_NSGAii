from abaqus import *
from abaqusConstants import *
import __main__
import os
import matplotlib.pyplot as plt
import numpy as np
import random
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import shutil
import math

# CHANGE WORK DIRECTORY
path = r"C:\TestPython"
os.chdir(path)

# VERY IMPORTANT
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

#INPUTS - DIMENSIONS
R_base = 7000
R_pedestal = 2000.0
Hi_base = 500.0
Hf_base = 2000.0
H_pedestal = 2000.0
Size_mesh = 1500

#INPUTS - MATERIAL
GamaC = 30  # kN/m³
GamaS = 18  # kN/m³
qd = 2406.44
#VALUES FOR ABAQUS  - all fixed values
density = 25000.0
young_modulus = 5600 * math.sqrt(GamaC) * 1000000
poisson = 0.2

#IMPUT - LOADS
Fres = 750  # kN.m    #HORIZONTAL LOAD
Fz = 2940  # kN       #VERTICAL LOAD
Mres = 64215  # kN.m  #BENDING MOMENT
Mz = 3060  # kN.m     #TWISTING MOMENT
t = 0.6  # m - HEIGHT FROM THE GROUND TO THE POINT WHERE LOADS ARE DEFINED
#VALUES FOR ABAQUS
Load_Fx = 0           #HORIZONTAL LOAD
Load_Fy = 750000      #HORIZONTAL LOAD
Load_Fz = -2940000    #VERTICAL LOAD
Load_Mx = -64215000   #BENDING MOMENT
Load_My = 0           #BENDING MOMENT
Load_Mz = 3060000     #TWISTING MOMENT


def CalculateDisplacement():
    Mdb()

    #CREATES MATERIAL
    '''session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)'''
    mdb.models['Model-1'].Material(name='Concrete')
    mdb.models['Model-1'].materials['Concrete'].Density(table=((density,),))
    mdb.models['Model-1'].materials['Concrete'].Elastic(table=((young_modulus,poisson),))


    #CREATES THE CIRCULAR PLATE
    '''    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)'''
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(R_base, 0.0))
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']


    #CREATES THE VARIABLE SECTION
    variation = (Hf_base - Hi_base) / 10

    p = mdb.models['Model-1'].parts['Part-1']
    f1, e, d1 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f1[0], sketchUpEdge=e[0],
        sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
        sheetSize=112.82, gridSpacing=2.82, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['Part-1']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(R_pedestal, 0.0))
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e1[0], faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    layupOrientation = None
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region1 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region2 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region3 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region4 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region5 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region6 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region7 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region8 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region9 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region10 = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region11 = regionToolset.Region(faces=faces)
    compositeLayup = mdb.models['Model-1'].parts['Part-1'].CompositeLayup(
        name='CompositeLayup-1', description='', elementType=SHELL,
        offsetType=MIDDLE_SURFACE, symmetric=False,
        thicknessAssignment=FROM_SECTION)
    compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON,
        thicknessType=UNIFORM, poissonDefinition=DEFAULT, temperature=GRADIENT,
        useDensity=OFF)
    compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None,
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0,
        axis=AXIS_3)
    compositeLayup.suppress()
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-1', region=region1,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=Hi_base,
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-2', region=region2,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (1 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-3', region=region3,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (2 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-4', region=region4,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (3 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-5', region=region5,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (4 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-6', region=region6,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (5 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-7', region=region7,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (6 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-8', region=region8,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (7 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-9', region=region9,
        material='Concrete', thicknessType=SPECIFY_THICKNESS, thickness=(Hi_base + (8 * variation)),
        orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-10',
        region=region10, material='Concrete', thicknessType=SPECIFY_THICKNESS,
        thickness=(Hi_base + (9 * variation)), orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-11',
        region=region11, material='Concrete', thicknessType=SPECIFY_THICKNESS,
        thickness=Hf_base, orientationType=SPECIFY_ORIENT, orientationValue=0.0,
        additionalRotationType=ROTATION_NONE, additionalRotationField='',
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.resume()


    #CREATES SECTION FOR PEDESTAL
    mdb.models['Model-1'].HomogeneousShellSection(name='Section-1',
        preIntegrate=OFF, material='Concrete', thicknessType=UNIFORM,
        thickness=H_pedestal, thicknessField='', nodalThicknessField='',
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
        integrationRule=SIMPSON, numIntPts=5)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
    region = p.Set(faces=faces, name='Set-12')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
        offsetType=MIDDLE_SURFACE, offsetField='',
        thicknessAssignment=FROM_SECTION)


    #CREATES ASSEMBLY
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Part-1']
    a1.Instance(name='Part-1-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)


    #CREATES STEP
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON,
        adaptiveMeshConstraints=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)


    #CREATES THE MESH
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF,
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=Size_mesh, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Part-1']
    p.generateMesh()


    #CREATES THE SUPPORT
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, loads=ON,
        bcs=ON, predefinedFields=ON, connectors=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances['Part-1-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    region = a.Set(edges=edges1, name='Set-1')
    mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1',
        region=region, localCsys=None)


    #CREATES THE LOAD NODE
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF,
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    a = mdb.models['Model-1'].rootAssembly
    n1 = a.instances['Part-1-1'].nodes
    #nodes1 = n1.getSequenceFromMask(mask=('[#0:2 #100000 ]', ), )
    #a.Set(nodes=nodes1, name='Set-2')
    min_distance = float('inf')
    closest_node = None
    # Loop through all nodes to find the one closest to (0,0,0)
    for node in n1:
        # Calculate the distance from the origin (0,0,0)
        distance = sqrt(node.coordinates[0] ** 2 + node.coordinates[1] ** 2 + node.coordinates[2] ** 2)

        # Check if this node is closer to the origin than the previously found nodes
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    # Create a set with the node closest to the origin
    if closest_node:
        a.Set(nodes=(n1.sequenceFromLabels([closest_node.label]),), name='Set-2')


    # CREATES THE LOAD
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, loads=ON,
                                                               bcs=ON, predefinedFields=ON, connectors=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    a = mdb.models['Model-1'].rootAssembly
    region = a.sets['Set-2']
    mdb.models['Model-1'].ConcentratedForce(name='Load-1', createStepName='Step-1',
                                            region=region, cf1=Load_Fx, cf2=Load_Fy, cf3=Load_Fz, distributionType=UNIFORM, field='',
                                            localCsys=None)
    a = mdb.models['Model-1'].rootAssembly
    region = a.sets['Set-2']
    mdb.models['Model-1'].Moment(name='Load-2', createStepName='Step-1',
                                 region=region, cm1=Load_Mx, cm2=Load_My, cm3=Load_Mz, distributionType=UNIFORM, field='',
                                 localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF,
                                                               predefinedFields=OFF, connectors=OFF)


    #CREATES THE JOB
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
        scratch='', resultsFormat=ODB)


    #SUBMIT THE JOB
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)


    #TO WAIT FOR JOB COMPLETION
    mdb.jobs['Job-1'].waitForCompletion()
    print("Job-1 finished running")

    CurrentFolder = os.getcwd()

    #THIS OPENS THE ODB - Output Database
    session.mdbData.summary()
    odb = session.openOdb(str(CurrentFolder) + '/' + 'Job-1.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    session.viewports['Viewport: 1'].makeCurrent()
    '''(odb.steps['Step-1'].frames[1].fieldOutputs['U'].values[1].data[2])'''

    #THIS GET THE DISPLACEMENTS
    '''frame = 0 is the initial step - frame = 1 is the first fully calculated step'''
    Disps = odb.steps['Step-1'].frames[1].fieldOutputs['U'].getSubset(position=NODAL).bulkDataBlocks[0].data
    MaxDisps = np.max(np.abs(Disps), axis=0)
    MaxU3 = MaxDisps[2]

    odb.close()
    print(MaxU3)

    if os.path.exists("%s/%s" % (str(CurrentFolder), "Job-1.simdir")):
        shutil.rmtree("%s/%s" % (str(CurrentFolder), "Job-1.simdir"))

    for fname in os.listdir(CurrentFolder):
        if fname.startswith("Job-1") and not fname.endswith(".inp"):
            os.remove(os.path.join(CurrentFolder, fname))

    return MaxU3

resultado = CalculateDisplacement()

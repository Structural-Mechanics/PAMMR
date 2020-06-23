# -*- coding: utf-8 -*-
# =============================================================================
# =============================================================================
#
# PAMMR: Postprocessing of ANSYS Modal data (F4E_D_2JWG8E)
#
# =============================================================================
# =============================================================================

# Jordi Ayneto
# jordi.ayneto@f4e.europa.eu
# v1.2

'''
Description
This script is used to produce a plot presenting the accumulated ratio 
effective mass to total mass using the modal output of an ANSYS calculation

Input data
The input data is the output produced by an ANSYS modal calculation. The
following lines can be included before and after the SOLVE command:
    
    /output, Modal_Output, txt
    solve
    /output

File names are defined by modifying the "Definitions" below.
'''

# Import modules
import numpy as np
import matplotlib.pyplot as plt
import os.path

#%% Definitions
Path = 'D://DATA//'
DataFile = 'Modal_Output.txt'

#%%

# Check if file exists, then run
        
if os.path.exists(Path+DataFile):
    
    # Prepare data for plotting: compute accumulated ratio modal mass to total mass
    
    bulkdata = []
    with open (Path+DataFile, 'r') as file:
        bulkdata=file.readlines()
    
    # Inspect data: number of modes
    ln = 0
    for line in bulkdata:
        if line.find('NUMBER OF MODES') != -1:
            nModes = int(line[:-1][-4:])
            break
        else:
            ln = ln+1
    
    del bulkdata[:ln]
    
    # Inspect data: total mass
    ln = 0
    for line in bulkdata:
        if line.find('TOTAL MASS') != -1:
            tMass = float(line[:-1][-12:])
            break
        else:
            ln = ln+1
    
    del bulkdata[:ln]  
    
    # Inspect data: x-direction table data
    ln = 0
    for line in bulkdata:
        if line.find('X  DIRECTION') != -1:
            break
        else:
            ln = ln+1
    
    del bulkdata[:ln+3]
    
    xdata = np.zeros((nModes,9))
    
    try:                                # try only performed for x (consistency)
        for i in range(nModes):
            xdata[i,0] = float(bulkdata[i][:-1][0:6])
            xdata[i,1] = float(bulkdata[i][:-1][7:18])
            xdata[i,2] = float(bulkdata[i][:-1][19:36])
            xdata[i,3] = float(bulkdata[i][:-1][37:50])
            xdata[i,4] = float(bulkdata[i][:-1][51:66])
            xdata[i,5] = float(bulkdata[i][:-1][67:82])
            xdata[i,6] = float(bulkdata[i][:-1][83:98])
            xdata[i,7] = float(bulkdata[i][:-1][99:114])
            if i == 0:
                xdata[i,8] = xdata[i,7]
            else:
                xdata[i,8] = xdata[i,7] + xdata[i-1,8]
    except:
      print('Cannot process output file, please check that number of modes extracted equals number of modes requested')
    
    
    # Inspect data: y-direction table data
    ln = 0
    for line in bulkdata:
        if line.find('Y  DIRECTION') != -1:
            break
        else:
            ln = ln+1
    
    del bulkdata[:ln+3]
    
    ydata = np.zeros((nModes,9))
          
    for i in range(nModes):
            ydata[i,0] = float(bulkdata[i][:-1][0:6])
            ydata[i,1] = float(bulkdata[i][:-1][7:18])
            ydata[i,2] = float(bulkdata[i][:-1][19:36])
            ydata[i,3] = float(bulkdata[i][:-1][37:50])
            ydata[i,4] = float(bulkdata[i][:-1][51:66])
            ydata[i,5] = float(bulkdata[i][:-1][67:82])
            ydata[i,6] = float(bulkdata[i][:-1][83:98])
            ydata[i,7] = float(bulkdata[i][:-1][99:114])
            if i == 0:
                ydata[i,8] = ydata[i,7]
            else:
                ydata[i,8] = ydata[i,7] + ydata[i-1,8]
    
    # Inspect data: z-direction table data
    ln = 0
    for line in bulkdata:
        if line.find('Z  DIRECTION') != -1:
            break
        else:
            ln = ln+1
    
    del bulkdata[:ln+3]
    
    zdata = np.zeros((nModes,9))

    for i in range(nModes):
        zdata[i,0] = float(bulkdata[i][:-1][0:6])
        zdata[i,1] = float(bulkdata[i][:-1][7:18])
        zdata[i,2] = float(bulkdata[i][:-1][19:36])
        zdata[i,3] = float(bulkdata[i][:-1][37:50])
        zdata[i,4] = float(bulkdata[i][:-1][51:66])
        zdata[i,5] = float(bulkdata[i][:-1][67:82])
        zdata[i,6] = float(bulkdata[i][:-1][83:98])
        zdata[i,7] = float(bulkdata[i][:-1][99:114])
        if i == 0:
            zdata[i,8] = zdata[i,7]
        else:
            zdata[i,8] = zdata[i,7] + zdata[i-1,8]
    
    # Prepare data for plotting
    ''' Example	
    0	0	3.49	0.00000	zero
    1	0	3.49	0.01032	am1
    2	1	3.86	0.01032	am1
    3	1	3.86	0.52747	am2
    4	2	5.45	0.52747	am2
    5	2	5.45	0.52752	am3
    6	3	5.81	0.52752	am3
    7	3	5.81	0.52789	am4
    8	4	6.01	0.52789	am4
    9	4	6.01	0.52812	am5
    10	5	6.15	0.52812	am5
    11	5	6.15	0.52862	am6
    '''
    
    # xdata
    xplot = np.zeros((2*nModes,2))
    xplot[0,0] = xdata[0,1]
    xplot[0,1] = 0.0
    xplot[1,0] = xdata[0,1]
    xplot[1,1] = 100*xdata[0,8]
    for i in range(1, nModes):
        xplot[2*i,  0] =     xdata[i,  1]
        xplot[2*i,  1] = 100*xdata[i-1,8]
        xplot[2*i+1,0] =     xdata[i,  1]
        xplot[2*i+1,1] = 100*xdata[i,  8]
    
    # ydata
    yplot = np.zeros((2*nModes,2))
    yplot[0,0] = ydata[0,1]
    yplot[0,1] = 0.0
    yplot[1,0] = ydata[0,1]
    yplot[1,1] = 100*ydata[0,8]
    for i in range(1, nModes):
        yplot[2*i,  0] =     ydata[i,  1]
        yplot[2*i,  1] = 100*ydata[i-1,8]
        yplot[2*i+1,0] =     ydata[i,  1]
        yplot[2*i+1,1] = 100*ydata[i,  8]
    
    # zdata
    zplot = np.zeros((2*nModes,2))
    zplot[0,0] = zdata[0,1]
    zplot[0,1] = 0.0
    zplot[1,0] = zdata[0,1]
    zplot[1,1] = 100*zdata[0,8]
    for i in range(1, nModes):
        zplot[2*i,  0] =     zdata[i,  1]
        zplot[2*i,  1] = 100*zdata[i-1,8]
        zplot[2*i+1,0] =     zdata[i,  1]
        zplot[2*i+1,1] = 100*zdata[i,  8]
    
    # Plot data
    
    plt.figure(figsize=(10,6))
    plt.plot(xplot[:,0], xplot[:,1], label ='Acc. x-Mass')
    plt.plot(yplot[:,0], yplot[:,1], label ='Acc. y-Mass')
    plt.plot(zplot[:,0], zplot[:,1], label ='Acc. z-Mass')
    
    plt.ylim(0,100)
    
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.5)
    plt.legend(loc='best')
    
    plt.suptitle('Accumulated ratio modal mass to total mass',fontsize=16, y=0.97)
    plt.xlabel('Frequency $[Hz]$')
    plt.ylabel('Acc. ratio mass to total mass [%]')
    
    MaxX = xplot[len(xplot)-1,1]
    MaxY = yplot[len(yplot)-1,1]
    MaxZ = zplot[len(zplot)-1,1]
    
    plt.title('Max. ratio in (x,y,z) = ({:2.1f},{:2.1f},{:2.1f})[%], Number of modes = {}'.format(MaxX, MaxY, MaxZ, nModes),
              fontsize=10, y=1.00)

    del MaxX, MaxY, MaxZ
    
    # Save to file
    PlotName = 'RatioAccMass_' + DataFile[:-4] + '.png'
    plt.savefig(PlotName, dpi = 300, bbox_inches='tight')
    plt.close()
    
    # Write data to files
    Modal_Plot = np.zeros((2*nModes,4))
    Modal_Plot[:,0] = xplot[:,0]
    Modal_Plot[:,1] = xplot[:,1]
    Modal_Plot[:,2] = yplot[:,1]
    Modal_Plot[:,3] = zplot[:,1]
    labels = ' Freq[Hz] Acc.rMassX[%] Acc.rMassY[%] Acc.rMassZ[%]'
    DataName = 'RatioAccMass_' + DataFile
    np.savetxt(DataName,Modal_Plot, fmt = '%3.3f', header = labels)
    
    del nModes, tMass
    del xdata, ydata, zdata, xplot, yplot, zplot, Modal_Plot

else:
    print('Requested file does not exist!')
#%%
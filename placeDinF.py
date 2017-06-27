import csv
import numpy as np

#load depths file
iDepths = csv.reader(open('DSSI_NEW.csv', 'r'))	#I converted the excel file to .csv 
depths = []
for l in iDepths:
	depths.append(l)

depths = np.array(depths)


#load formation file
iForms = csv.reader(open('FTOPS_NEW.csv', 'r'))	#I converted the excel file to .csv 
forms = []
for l in iForms:
	forms.append(l)

forms = np.array(forms)


outputData = []
outputData.append(['User-Format Well ID', 'Top Depth (m)', 'Bottom Depth (m)', 'Coresponding Top Depth (m)', 'Coresponding FTOP', 'Coresponding Bottom Depth (m)', 'Coresponding FBTM'])	#add title row

count = 0.0
dLen = len(depths)

for r in depths:									#for each row in depths
#for r in depths[:100]:								#only do first 100 for testing purposes
	if ((count/dLen) * 100) % 10 < 0.01:				
		print (count/dLen) * 100, '%'				#progress printing
	idxs =  np.where(forms == r[0])[0]				#find where the well name is in forms
	oData = []
	topF = False
	botF = False	
	for i, idx in enumerate(idxs):									#for each index (formation) where the well names line up
		if not topF and float(r[1]) < float(forms[idx][2]):			#find the first location where top depth is less than formation
			topF = True
			if i == 0:												#above condition here
				oData = [r[0], r[1], r[2], 0, 'ABOVE ' + forms[idx][1]]
			else:
				oData = [r[0], r[1], r[2], forms[idx-1,2], forms[idx-1][1]]

		if not botF and float(r[2]) < float(forms[idx][2]):			#find first location where bottom is greated formation
			botF = True
			oData = oData + [forms[idx - 1,2], forms[idx - 1][1]]
	
	if topF and not botF:											#if we found the top, but not the bottom then bottom was below lowest
		oData = oData + [forms[-1,2], 'BELOW ' + forms[-1][1]]		
	if not topF and not botF:										#if we found neither, both top and bottom are below the lowest
		oData = [r[0], r[1], r[2], forms[-1,2], 'BELOW ' + forms[-1][1], forms[-1,2], 'BELOW ' + forms[-1][1]]
		print "\tSomething wrong with " + str(r[0])

	outputData.append(oData)
	count = count + 1.0

#save output data
oFile = open('output_NEW.csv','w')
for l in outputData:
	try:
		oFile.write(str(l[0]) + ', ' + str(l[1]) + ', ' + str(l[2]) + ', ' + str(l[3]) + ', ' + str(l[4]) + ', ' + str(l[5]) + ', ' + str(l[6]) + '\n')
	except IndexError:
		print "Probleb with missing data at " + str(l[0])
oFile.close()

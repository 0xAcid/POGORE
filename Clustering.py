#################################################################
#	Credits goes to Ax. from PogoDev	
#	Thanks to PogoDev for all the help	
#################################################################
STEP = 0.0005

from haversine import haversine

def Distance(a,b):
	# return math.fabs(a-b)
	return haversine(a,b)

def OrderCircles(Circles):
	Circles.sort(key=lambda X: len(X[1]), reverse=True)
	return Circles

	
def ClusteringOptimized(xData, CircleStep):
	Spawns = []
	for i in range(0, len(xData)):
		# print(xData[0])
		Spawns.append([xData[i], i])

	#GetMin
	
	# Just something to get topleft corner and bottom right corner of the scanning area
	MinLon = 0
	MinLat = 255
	MaxLon = -10
	MaxLat = 0
	for i in xData:
		if i[0] < MinLat:
			MinLat = i[0]
		if i[0] > MaxLat:
			MaxLat = i[0]
		if i[1] < MinLon:
			MinLon = i[1]
		if i[1] > MaxLon:
			MaxLon = i[1]
	TOPLEFT = [MaxLat +0.002, MinLon-0.002]
	BOTRIGHT = [MinLat-0.002, MaxLon+0.002]

	CirclesX = int((TOPLEFT[0] - BOTRIGHT[0])/CircleStep)
	CirclesY =  int((BOTRIGHT[1] - TOPLEFT[1])/CircleStep)
	
	# We create CirclexX * CirclesY circles spaced of STEP
	
	# Map with big step will look like this
	#OOOOOOO
	#OOOOOOO
	#OOOOOOO
	#OOOOOOO
	
	# MAp with small step will look like this
	#ooooooooo
	#ooooooooo
	#ooooooooo
	#ooooooooo
	
	Circles = []
	for i in range(0, CirclesX):
		for j in range(0, CirclesY):
			# Circle center
			Center = [TOPLEFT[0] - CircleStep*i, TOPLEFT[1] + CircleStep*j]
			RelatedSpawns = []
			for k in range(0, len(Spawns)):
				# check for all spawns if they're within a 70meters distance
				if (Distance(Center, Spawns[k][0]) < 0.07): # 70 meters
					# if so, add it to the circle relatedspawns
					RelatedSpawns.append(Spawns[k][1])
			# if the circle does not have related spawn, just move on (speed up the process)
			if not len(RelatedSpawns):
				continue
			Circles.append([Center, RelatedSpawns])
	
	
	Checked = []
	SavedCircles = []
	z = 0
	# Until we matched all Spawns in circles
	while (len(Checked) < len(Spawns)):
		z += 1
		Circles = OrderCircles(Circles)
		BestCircle = Circles[0]
		# Get the circle with the most spawns in it
		SavedCircles.append(BestCircle[0])
		# Keep the best circle
		for i in BestCircle[1]:
			Checked.append(i)
		# Delete all spawns that we already matched with the best circle we just found
		for i in range(0, len(Circles)):
			LocalSpawns = Circles[i][1]
			Circles[i][1] = set(LocalSpawns) - set(Checked)
		# ... until all spawns are matched
	print("var GridCircles =", end='')
	# SavedCircles are the circles we're interested in.
	print(SavedCircles)



if __name__ == '__main__':
	Data = []
	# Data should look like [ [lat1,lon1] , [lat2,lon2] , [lat3, lon3] .....      ] 
	
	
	ClusteringOptimized(Data, STEP)

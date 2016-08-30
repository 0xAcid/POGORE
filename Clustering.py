#################################################################
#	Credits goes to Ax. from PogoDev	
#	Thanks to PogoDev for all the help	
#################################################################
STEP = 0.0005
ACCOUNTS = 40
MAX_ITERATIONS = 100
from haversine import haversine


# Old kmeans stuff
def Clustering_6(xData, Workers):

	Data = []
	for i in range(0,len(xData)):
		Data.append([xData[i], -1])
	Clusters = []
	for i in range(0, Min(len(xData),Workers)):
		Clusters.append([])
	Randoms = []
	
	# Randomly assign one element per cluster
	x = 0
	for i in Clusters:

		LocalRandom = random.randint(0, len(Data)-1)
		
		while LocalRandom in Randoms:
			LocalRandom = random.randint(0, len(Data)-1)
		Randoms.append(LocalRandom)
		i.append(Data[LocalRandom][0])
		Data[LocalRandom][1] = x
		x = x+1

	ITE = 0
	while True:

		for i in range(0, len(Data)):
			AssociatedCluster = -1
			CurrentMin = 99999999999999999999999999999
			for j in range(0, Min(len(xData),Workers)):
				if Centroid(Clusters[j]):
					Dist = Distance(Centroid(Clusters[j]) , Data[i][0])
				else:
					Dist = 0

				if ( Dist < CurrentMin):
					CurrentMin = Dist
					AssociatedCluster = j

			
			if Data[i][1] != -1:
				Clusters[ Data[i][1]].remove( Data[i][0] )

			Clusters[ AssociatedCluster ].append(Data[i][0])
			Data[i][1] = AssociatedCluster
		ITE +=1
		if ITE > MAX_ITERATIONS:
			print("reached max ITE")
			break
			
			
	for i in Clusters:
		print(len(i))
	return Clusters

# Old kmeans stuff
def Clustering(Data, Workers):
	Clusters = []
	for i in range(0, Workers):
		Clusters.append([])
	Randoms = []
	
	# Randomly assign one element per cluster
	x = 0

	for i in Clusters:

		LocalRandom = random.randint(0, len(Data)-1)
		while LocalRandom in Randoms:
			
			LocalRandom = random.randint(0, len(Data)-1)
		Randoms.append(LocalRandom)
		i.append(Data[LocalRandom][0])
		Data[LocalRandom][1] = x
		x = x+1

	ITE = 0
	while True:

		for i in range(0, len(Data)):
			AssociatedCluster = -1
			CurrentMin = 99999999999999999999999999999
			for j in range(0, Workers):
				if Centroid(Clusters[j]):
					Dist = Distance(Centroid(Clusters[j]) , Data[i][0])
				else:
					Dist = 0

				if ( Dist < CurrentMin):
					CurrentMin = Dist
					AssociatedCluster = j
			# remove from old cluster
			
			if Data[i][1] != -1:
				Clusters[ Data[i][1]].remove( Data[i][0] )

				#add to new cluster
			Clusters[ AssociatedCluster ].append(Data[i][0])
			Data[i][1] = AssociatedCluster
		ITE +=1
		print(ITE)
		if ITE > MAX_ITERATIONS:
			print("reached max ITE")
			break

	return Clusters


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

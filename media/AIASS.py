def dfs(start, goal, mat):

	a = 0
	b = 0
	temp = 0
	res=""
	
	res += str(start) 
	while a != goal:
		if mat[a][b] == 0 and b != 6:
			b += 1
		elif b == 6 and mat[a][b] == 0: ##END NODE
			b = a+1
			a = temp
		else :
			res = res + "->" + str(b) 
			temp = a
			a = b
			b = 0
	print(res)
			
dfs(0, 4, [[0,1,1,0,0,0,0],
       [0,0,0,1,1,0,0],
       [0,0,0,0,0,1,1],
       [0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0]])


def bfs(start, goal, adj_mat):
	m=0
	n=0
	morty=[]
	result=""
	j=True
	x=0
	
	for m in range(0,len(adj_mat)):
		for n in range(0,len(adj_mat)):
			if adj_mat[m][n]==1:
				morty.append([m,n])
			else:
				pass
	while j==True:
		for y in range(0,2):
			if str(morty[x][y]) not in result and morty[x][y]!=goal:
				result=result+str(morty[x][y])+"->"
			elif morty[x][y]==goal :
				result=result+str(morty[x][y])+" "
				j=False
			else:
				pass
		x+=1
	
	print(result)


bfs(0, 5, [[0,1,0,0,1,0,0],
       		[0,0,1,1,0,0,0],
       		[0,0,0,0,0,0,0],
       		[0,0,0,0,0,0,0],
       		[0,0,0,0,0,1,1],
       		[0,0,0,0,0,0,0],
       		[0,0,0,0,0,0,0]])
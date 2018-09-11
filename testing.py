import math
import copy
import numpy as np

polygon = []
with_mapping = []
all_vertices = []
# path = [[0 for cols in range(len(all_vertices))] for rows in range(len(all_vertices))]
# distance_between_vertices = [[10e8 for cols in range(len(all_vertices))] for rows in range(len(all_vertices))]
path = [[0 for cols in range(2000)] for rows in range(2000)]
distance_between_vertices = [[10e8 for cols in range(2000)] for rows in range(2000)]

def initialize():
	#预读文件
	#预读若干凸多边形，格式为[[vertices chains],...,[]]
	f = open('copy_a.ply')
	convexnum = f.readline().split()
	for i in range((int)(convexnum[0])):
		info = f.readline().split()
		vertice_chain = []
		for j in range((int)(info[0])):
			temp_text = f.readline().split()
			vertice_chain.append(((float)(temp_text[0]),(float)(temp_text[1])))
		f.readline().split()
		polygon.append(vertice_chain)
	for convex in polygon:
		temp_map = []
		for point in convex:
			if point in all_vertices:
				temp_map.append((point,all_vertices.index(point)))
			else:
				all_vertices.append(point)
				temp_map.append((point,len(all_vertices)-1))
		with_mapping.append(temp_map)

	
	# return polygon

def floyd_algorithm():
	# path = [[0 for cols in range(len(all_vertices))] for rows in range(len(all_vertices))]
	for i in range(len(all_vertices)):
		for j in range(len(all_vertices)):
			path[i][j] = j
	
	# distance_between_vertices = [[10e8 for cols in range(len(all_vertices))] for rows in range(len(all_vertices))]
	for i in range(len(all_vertices)):
		distance_between_vertices[i][i] = 0
	for convex in with_mapping:
		temp_point_num1 = 0
		temp_point_num2 = 1
		while temp_point_num1 <= len(convex) - 2:
			temp_point_num2 = temp_point_num1 + 1
			while temp_point_num2 <= len(convex) - 1:
				distance_between_vertices[convex[temp_point_num1][1]][convex[temp_point_num2][1]] = \
				math.sqrt((convex[temp_point_num1][0][0] - convex[temp_point_num2][0][0]) ** 2 \
				+ (convex[temp_point_num1][0][1] - convex[temp_point_num2][0][1]) ** 2)
				distance_between_vertices[convex[temp_point_num2][1]][convex[temp_point_num1][1]] = \
				distance_between_vertices[convex[temp_point_num1][1]][convex[temp_point_num2][1]]
				temp_point_num2 += 1
			temp_point_num1 += 1
	# print(distance_between_vertices)
	for k in range(len(all_vertices)):
		for i in range(len(all_vertices)):
			for j in range(len(all_vertices)):
				if distance_between_vertices[i][k] != 10e8 and distance_between_vertices[k][j] != 10e8 and \
				distance_between_vertices[i][k] + distance_between_vertices[k][j] < distance_between_vertices[i][j]:
					distance_between_vertices[i][j] = distance_between_vertices[i][k] + distance_between_vertices[k][j]
					path[i][j] = path[i][k]



def find_rectangle_boundry(convex):
	minx = miny = 10e6
	maxx = maxy = -10e6
	for vertice in convex:
		if vertice[0] < minx:
			minx = vertice[0]
		if vertice[0] > maxx:
			maxx = vertice[0]
		if vertice[1] < miny:
			miny = vertice[1]
		if vertice[1] > maxy:
			maxy = vertice[1]
	return (minx,maxx,miny,maxy)

def find_in_which_convex(point):
	#O(mlogN)找到，可用range加速
	#O(mN)
	convex_series_num = -1
	on_border = 0
	temp = -1
	for convex in polygon:
		temp += 1
		(minx,maxx,miny,maxy) = find_rectangle_boundry(convex)
		if point[0] >= minx and point[0] <= maxx and point[1] >= miny and point[1] <= maxy:
			flag = False
			(v1,v2,v3) = (0,1,2)
			while flag == False and v3 < len(convex):
				flag = is_point_in_triangle(point,convex[v1],convex[v2],convex[v3])
				border_num = is_on_border(point,convex[v1],convex[v2],convex[v3])
				# if border_num != -1:
				if border_num != -1:
					if border_num == 0:
						on_border = 1
					elif (v1,v2,v3) == (0,1,2) and (border_num == 1 or border_num == 2):
						on_border = 1
					elif (v1,v2,v3) == (0,len(convex)-2,len(convex)-1) and (border_num == 2 or border_num == 3):
						on_border = 1
					elif border_num == 2:
						on_border = 1
				v2 += 1
				v3 += 1
			if flag == True:
				convex_series_num = temp
				break
	return (convex_series_num,on_border)

def is_on_border(point,vertice1,vertice2,vertice3):
	pa = (vertice1[0] - point[0], vertice1[1] - point[1])
	pb = (vertice2[0] - point[0], vertice2[1] - point[1])
	pc = (vertice3[0] - point[0], vertice3[1] - point[1])
	ab = (vertice2[0] - vertice1[0], vertice2[1] - vertice1[1])
	bc = (vertice3[0] - vertice2[0], vertice3[1] - vertice2[1])
	ca = (vertice1[0] - vertice3[0], vertice1[1] - vertice3[1])
	if pa == (0,0) or pb == (0,0) or pc == (0,0):
		return 0
	if pa[0] * ab[1] - pa[1] * ab[0] == 0 and pa[0] < 0 * ab[0] and pa[0] > -1 * ab[0]:
		return 1
	if pb[0] * bc[1] - pb[1] * bc[0] == 0 and pb[0] < 0 * bc[0] and pb[0] > -1 * bc[0]:
		return 2
	if pc[0] * ca[1] - pc[1] * ca[0] == 0 and pc[0] < 0 * ca[0] and pc[0] > -1 * ca[0]:
		return 3
	return -1

def is_point_in_triangle(point,vertice1,vertice2,vertice3):
	in_or_not_in = False
	pa = (vertice1[0] - point[0], vertice1[1] - point[1])
	pb = (vertice2[0] - point[0], vertice2[1] - point[1])
	pc = (vertice3[0] - point[0], vertice3[1] - point[1])
	t1 = get_2dmultiplication_cross(pa,pb)
	t2 = get_2dmultiplication_cross(pb,pc)
	t3 = get_2dmultiplication_cross(pc,pa)
	if t1 >= 0 and t2 >= 0 and t3 >= 0:
		in_or_not_in = True
	if t1 <= 0 and t2 <= 0 and t3 <= 0:
		in_or_not_in = True
	
	# t1 = PA^PB,
	# t2 = PB^PC,
	# t3 = PC^PA,
	# 判断符号

	return in_or_not_in

def get_2dmultiplication_cross(array1,array2):
	return(array1[0] * array2[1] - array2[0] * array1[1])
	# a.x*b.y-b.x*a.y,

def generate_advanced_point(point):
	(convex_series_num,on_border) = find_in_which_convex(point)
	advanced_point = (point[0],point[1],convex_series_num,on_border)
	return advanced_point

def find_shortest_distance_to_boundry(advanced_point):
	'''
	advancedpoint某一点数据结构：
		(横坐标，纵坐标，在哪个convex内，是否在边界上)	
	'''
	#O(N)(遍历一遍找到)
	shortest_distance = 10e6
	temp_point = (0,0)
	if advanced_point[3] == 1:
		temp_point = (advanced_point[0],advanced_point[1])
		return 0
	for point in polygon[advanced_point[2]]:
		if shortest_distance > (point[0] - advanced_point[0]) ** 2 + (point[1] - advanced_point[1]) ** 2:
			shortest_distance = (point[0] - advanced_point[0]) ** 2 + (point[1] - advanced_point[1]) ** 2
			temp_point = (point[0],point[1])
	return (math.sqrt(shortest_distance),temp_point)
	#此处还可以改一改

def get_vertices_distance(point1,point2):
	#此处要改成dijstra搜索图
	#需在初始化是建立一个网格结构，然后可搜索任意在边界上两个顶点的最短距离
	#使每个convex为完全图，然后运行Floyd算法计算出任意两个vertice的距离
	###
	#建立一个映射从原polygon到所有vertice的集合，用一个二维数组储存在vertice中的坐标

	# path = []
	# distance_between_vertices = []
	return (math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))

def get_final_distance(point1,point2):
	p1 = generate_advanced_point(point1)
	p2 = generate_advanced_point(point2)
	distance = 10e8
	if p1[2] == p2[2]:
		distance = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
	elif p1[3] == 1 and p2[3] == 1:
		p1_num = p2_num = 0
		temp = 0
		for point in with_mapping:
			if point[0] == (p1[0],p1[1]):
				p1_num = temp
			if point[0] == (p2[0],p2[1]):
				p2_num = temp
			temp += 1
		distance = distance_between_vertices[p1_num][p2_num]
	elif p1[3] == 1:
		for vertice in polygon[p2[2]]:
			p1_num = p2_num = 0
			temp = 0
			for point in with_mapping:
				if point[0] == (p1[0],p1[1]):
					p1_num = temp
				if point[0] == vertice:
					p2_num = temp
				temp += 1
			temp_distance = distance_between_vertices[p1_num][p2_num]
			vertice_to_p2 = math.sqrt((vertice[0] - p2[0]) ** 2 + (vertice[1] - p2[1]) ** 2)
			distance = distance if (temp_distance + vertice_to_p2 > distance) else (temp_distance + vertice_to_p2)
	elif p2[3] == 1:
		for vertice in polygon[p1[2]]:
			p1_num = p2_num = 0
			temp = 0
			for point in with_mapping:
				if point[0] == (p2[0],p2[1]):
					p1_num = temp
				if point[0] == vertice:
					p2_num = temp
				temp += 1
			temp_distance = distance_between_vertices[p1_num][p2_num]
			vertice_to_p1 = math.sqrt((vertice[0] - p1[0]) ** 2 + (vertice[1] - p1[1]) ** 2)
			distance = distance if (temp_distance + vertice_to_p1 > distance) else (temp_distance + vertice_to_p1)
	else:
		for vertice1 in polygon[p1[2]]:
			for vertice2 in polygon[p2[2]]:
				p1_num = p2_num = 0
				temp = 0
				for point in with_mapping:
					if point[0] == vertice1:
						p1_num = temp
					if point[0] == vertice2:
						p2_num = temp
					temp += 1
				temp_distance = distance_between_vertices[p1_num][p2_num]
				vertice_to_p1 = math.sqrt((vertice1[0] - p1[0]) ** 2 + (vertice1[1] - p1[1]) ** 2)
				vertice_to_p2 = math.sqrt((vertice2[0] - p2[0]) ** 2 + (vertice2[1] - p2[1]) ** 2)
				distance = distance if (temp_distance + vertice_to_p1 + vertice_to_p2 > distance) \
				else (temp_distance + vertice_to_p1 + vertice_to_p2)
	return distance

def main():
	initialize()
	floyd_algorithm()
	# num = find_in_which_convex((153,81))
	# num = find_in_which_convex((-1,-1))
	# print(num)
	# print(polygon)
	# print(find_rectangle_boundry(polygon[0]))
	# num = find_in_which_convex((10,10))
	# print(with_mapping)

	point1 = (50,50)
	point2 = (153,80.5)
	point = generate_advanced_point((153.5,80.5))
	# print(point)
	dis = find_shortest_distance_to_boundry(point)
	print(get_final_distance(point1,point2))
	while True:
		x = input("point1_x:")
		y = input("point1_y:")
		p1 = (float(x),float(y))
		x = input("point2_x:")
		y = input("point2_y:")
		p2 = (float(x),float(y))
		print(get_final_distance(p1,p2))
	# print(dis[0]+get_distance(dis[1],point1))
	# distance = find_shortest_distance_to_boundry(point)

if __name__ == "__main__":
	main()
 
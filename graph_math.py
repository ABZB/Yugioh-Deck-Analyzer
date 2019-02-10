import string
import shutil
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

	
#series of functions encoding the various iterated sums as per scratchwork
def astar(arr, i, j, star = False):
	#returns 0 if arr[i,j] has 1, 1 if arr[i,j] has 0
	if star:
		return 1 - arr[i][j]
	else:
		return arr[i][j]

#each function counts the number of edges of the specified vertex within the given subgraph of order 5
def count_node_i_edges(arr, index1, index2, index3, index4, index5):
	return(astar(arr, index1, index2) + astar(arr, index1, index3) + astar(arr, index1, index4) + astar(arr, index1, index5))

def count_node_j_edges(arr, index1, index2, index3, index4, index5):
	return(astar(arr, index2, index1) + astar(arr, index2, index3) + astar(arr, index2, index4) + astar(arr, index2, index5))

def count_node_k_edges(arr, index1, index2, index3, index4, index5):
	return(astar(arr, index3, index1) + astar(arr, index3, index2) + astar(arr, index3, index4) + astar(arr, index3, index5))

def count_node_l_edges(arr, index1, index2, index3, index4, index5):
	return(astar(arr, index4, index1) + astar(arr, index4, index2) + astar(arr, index4, index3) + astar(arr, index4, index5))

def count_node_m_edges(arr, index1, index2, index3, index4, index5):
	return(astar(arr, index5, index1) + astar(arr, index5, index2) + astar(arr, index5, index3) + astar(arr, index5, index4))


def count_total_edges(arr, index1, index2, index3, index4, index5):
	return((count_node_i_edges(arr, index1, index2, index3, index4, index5) + count_node_j_edges(arr, index1, index2, index3, index4, index5) + count_node_k_edges(arr, index1, index2, index3, index4, index5) + count_node_l_edges(arr, index1, index2, index3, index4, index5) + count_node_m_edges(arr, index1, index2, index3, index4, index5))/2)
	
#each function returns 1 if that vertex has at least one edge in the subgraph of the 5 given vertices, 0 otherwise
def check_node_i_edges(arr, index1, index2, index3, index4, index5):
	return(min(astar(arr, index1, index2) + astar(arr, index1, index3) + astar(arr, index1, index4) + astar(arr, index1, index5), 1))

def check_node_j_edges(arr, index1, index2, index3, index4, index5):
	return(min(astar(arr, index2, index1) + astar(arr, index2, index3) + astar(arr, index2, index4) + astar(arr, index2, index5), 1))

def check_node_k_edges(arr, index1, index2, index3, index4, index5):
	return(min(astar(arr, index3, index1) + astar(arr, index3, index2) + astar(arr, index3, index4) + astar(arr, index3, index5), 1))

def check_node_l_edges(arr, index1, index2, index3, index4, index5):
	return(min(astar(arr, index4, index1) + astar(arr, index4, index2) + astar(arr, index4, index3) + astar(arr, index4, index5), 1))

def check_node_m_edges(arr, index1, index2, index3, index4, index5):
	return(min(astar(arr, index5, index1) + astar(arr, index5, index2) + astar(arr, index5, index3) + astar(arr, index5, index4), 1))


def count_vertices_with_edges(arr, index1, index2, index3, index4, index5):
	return(check_node_i_edges(arr, index1, index2, index3, index4, index5) + check_node_j_edges(arr, index1, index2, index3, index4, index5) + check_node_k_edges(arr, index1, index2, index3, index4, index5) + check_node_l_edges(arr, index1, index2, index3, index4, index5) + check_node_m_edges(arr, index1, index2, index3, index4, index5))


def count_connected_subgraphs(arr):
	
	number_disconnected = 0
	two_vertices_connected = 0
	#count, two edges, three edges
	three_vertices_connected = [0, 0, 0]
	pair_two_vertices_connected = 0
	#count, 3, 4, 5, 6
	four_vertices_connected = [0, 0, 0, 0 ,0]
	#count, 3, 4
	two_and_three_vertices_connected = [0, 0, 0]
	#count, 4, 5, 6, 7, 8, 9, 10
	five_vertices_connected = [0, 0, 0, 0 ,0, 0, 0 ,0]
	
	for index1 in range(1, len(arr)):
		for index2 in range(index1 + 1, len(arr)):
			for index3 in range(index2 + 1, len(arr)):
				for index4 in range(index3 + 1, len(arr)):
					for index5 in range(index4 + 1, len(arr)):
					
						edged_vertices = count_vertices_with_edges(arr, index1, index2, index3, index4, index5)
						total_edges = count_total_edges(arr, index1, index2, index3, index4, index5)
						
						if(edged_vertices == 0):
							number_disconnected += 1
						#exactly two vertices have an edge, only possible if they are the only pair sharing an edge (exactly one edge with a vertex is a loop, which is does not occur under out framework)
						elif(edged_vertices == 2):
							two_vertices_connected += 1
						#exactly three vertices have an edge, only possible if there is exactly a triplet
						elif(edged_vertices == 3):
							three_vertices_connected[0] += 1
							if(total_edges == 2):
								three_vertices_connected[1] += 1
							else:
								three_vertices_connected[2] += 1
						#exactly four vertices have an edge, either there are exactly two edges total (a pair of pairs) or there are more than two edges (a quadruplet)
						elif(edged_vertices == 4):
							if(total_edges == 2):
								pair_two_vertices_connected += 1
							else:
								four_vertices_connected[0] += 1
								#counts how many edges
								if(total_edges == 3):
									four_vertices_connected[1] += 1
								elif(total_edges == 4):
									four_vertices_connected[2] += 1
								elif(total_edges == 5):
									four_vertices_connected[3] += 1
								else:
									four_vertices_connected[4] += 1
						elif(edged_vertices == 5):
							#if every vertex has at least one edge, there are at least 4 edges. If there are five edges, there is no way to assign them that avoids creating at least a connected subgraph of order 4. Thus, we just need to check that in the case of 4 edges, there is no pair of points such that neither connects to any point other than the other
							
							#is pair and triplet i-j-k and l-m
							if (total_edges == 3):
								two_and_three_vertices_connected[0] += 1
								two_and_three_vertices_connected[1] += 1
							
							elif(total_edges == 4):
								index_list = [index1, index2, index3, index4, index5]
								not_order_five = False
								for i in index_list:
									for j in [x for x in index_list if x != i]:
										#if i and j have an edge
										if(astar(arr, i, j) == 1):
											#count all the edges between i and vertices other than j, and all the edges between j and vertices other than i
											other_edges = 0
											for k in [y for y in index_list if(y != i and y != j)]:
												other_edges += astar(arr, i, k) + astar(arr, j, k)
											#if that count is 0, then i-j is an isolated pair, this is not a connec graph of order 5
											if(other_edges == 0):
												not_order_five = True
												break
										if(not_order_five):
											break
									if(not_order_five):
										break
								
								#then is pair and triplet
								if(not_order_five):
									two_and_three_vertices_connected[0] += 1
									two_and_three_vertices_connected[2] += 1
								#is quintuplet with four edges
								else:
									five_vertices_connected[0] += 1
									five_vertices_connected[1] += 1
							elif(total_edges == 5):
								five_vertices_connected[0] += 1
								five_vertices_connected[2] += 1
							elif(total_edges == 6):
								five_vertices_connected[0] += 1
								five_vertices_connected[3] += 1
							elif(total_edges == 7):
								five_vertices_connected[0] += 1
								five_vertices_connected[4] += 1
							elif(total_edges == 8):
								five_vertices_connected[0] += 1
								five_vertices_connected[5] += 1
							elif(total_edges == 9):
								five_vertices_connected[0] += 1
								five_vertices_connected[6] += 1
							elif(total_edges == 10):
								five_vertices_connected[0] += 1
								five_vertices_connected[7] += 1

	return(number_disconnected, two_vertices_connected, three_vertices_connected[0], three_vertices_connected[1], three_vertices_connected[2], pair_two_vertices_connected, four_vertices_connected[0], four_vertices_connected[1], four_vertices_connected[2], four_vertices_connected[3], four_vertices_connected[4], two_and_three_vertices_connected[0], two_and_three_vertices_connected[1], two_and_three_vertices_connected[2], five_vertices_connected[0], five_vertices_connected[1], five_vertices_connected[2], five_vertices_connected[3], five_vertices_connected[4], five_vertices_connected[5], five_vertices_connected[6], five_vertices_connected[7])


	
#Calls the functions and returns text array with the results
def analyze_adj_arr():
	
	adj_arr = construct_data_arr()
	
	count_disconnected, two_vertices_connected, three_vertices_connected, three_vertices_connected_2_edges, three_vertices_connected_3_edges, pair_two_vertices_connected, four_vertices_connected, four_vertices_connected_3_edges, four_vertices_connected_4_edges, four_vertices_connected_5_edges, four_vertices_connected_6_edges, two_and_three_vertices_connected, two_and_three_vertices_connected_3_edges, two_and_three_vertices_connected_4_edges, five_vertices_connected, five_vertices_connected_4_edges, five_vertices_connected_5_edges, five_vertices_connected_6_edges, five_vertices_connected_7_edges, five_vertices_connected_8_edges, five_vertices_connected_9_edges, five_vertices_connected_10_edges = count_connected_subgraphs(adj_arr)
	
	# should be size of deck choose five
	number_of_hands = count_disconnected + two_vertices_connected + three_vertices_connected + four_vertices_connected + five_vertices_connected + pair_two_vertices_connected + two_and_three_vertices_connected
	
	
	report = []
	report.append('Advanced Deck Analysis:')
	
	report.append('Your deck has: ' + str(number_of_hands) + ' possible hands (counting hands that are the same but with different copies of the same card)')
	
	#only one way for these to happen
	report.append('There are: ' + str(count_disconnected) + ' brick hands.')
	report.append('There are: ' + str(two_vertices_connected) + ' hands with exactly two live cards.')
	report.append('There are: ' + str(pair_two_vertices_connected) + ' hands live with exactly a pair of pairs of live cards.')
	
	#two ways for these to happen
	report.append('There are: ' + str(three_vertices_connected) + ' hands live with exactly three live cards. Of them, ' + str(three_vertices_connected_3_edges) + ' are all synergetic with one another, and ' + str(three_vertices_connected_2_edges) + ' are not.')
	
	report.append('There are: ' + str(two_and_three_vertices_connected) + ' hands with a pair and a triplet of live cards. Of them, ' + str(two_and_three_vertices_connected_4_edges) + ' have the triplet all synergetic with one another, and ' + str(two_and_three_vertices_connected_3_edges) + ' are not.')
	
	#more for this
	report.append('There are: ' + str(four_vertices_connected) + ' hands with four live cards. Of them, ' + str(four_vertices_connected_6_edges) + ' are all synergetic with one another, ' + str(four_vertices_connected_5_edges) + ' have one pair not so, ' + str(four_vertices_connected_4_edges) + ' have two pairs not so, and ' + str(four_vertices_connected_3_edges) + ' have three pairs not so')
	
	report.append('There are: ' + str(five_vertices_connected) + ' hands with five live cards. Of them, ' + str(five_vertices_connected_10_edges) + ' are all synergetic with one another, ' + str(five_vertices_connected_9_edges) + ' have one pair not so, ' + str(five_vertices_connected_8_edges) + ' have two pairs not so, ' + str(five_vertices_connected_7_edges) + ' have three pairs not so, ' + str(five_vertices_connected_6_edges) + ' have four pairs not so, ' + str(five_vertices_connected_5_edges) + ' have five pairs not so, and ' + str(five_vertices_connected_4_edges) + ' have six pairs not so.')
	
	#brick calculations
	
	
	#bricking exactly once
	brick_one_duel = count_disconnected / number_of_hands
	
	
	#not-bricking exactly twice
	no_brick_2_duels = ((1 - brick_one_duel))**2
	
	#bricking at least in two trials
	brick_2_duels_al1 = 1 - no_brick_2_duels	
	
	#not-bricking exactly three times
	no_brick_3_duels = ((1 - brick_one_duel))**3
	
	#bricking at least once in three trials
	brick_3_duels_al1 = 1 - no_brick_3_duels
	
	report.append('\n')
	
	report.append('The probability of bricking in one duel is: ' + str(round(100*brick_one_duel,1)) + '%')
	report.append('The probability of not bricking in any of two duels is: ' + str(round(100*no_brick_2_duels,1)) + '%')
	report.append('The probability of bricking in at least one of two duels is: ' + str(round(100*brick_2_duels_al1,1)) + '%')
	report.append('The probability of not bricking in any three duels is: ' + str(round(100*no_brick_3_duels,1)) + '%')
	report.append('The probability of bricking in at least one of three duels is: ' + str(round(100*brick_3_duels_al1,1)) + '%')
	
	
	return report

def create_deck_graph():
	adj_arr = construct_data_arr()
	
	#initialize graph
	deck_graph = nx.Graph()
	
	card_count_pp = len(adj_arr)
	card_count = card_count_pp - 1
	
	
	for counter, element in enumerate(adj_arr[0]):
		if(element != ''):
			#give duplicates of same card different names so they can be assigned unique vertices
			
			#if this is not the last card in the deck
			if(counter < card_count - 1):
				#if the next card has the same name as this card:
				if(element == adj_arr[0][counter + 1]):
					
					#if the next card is not the last card in the deck
					if(counter < card_count - 2):
						#if the next next card has the same name as this card:
						if(element == adj_arr[0][counter + 2]):
							#append ' (3)' to the end of that card's name
							adj_arr[0][counter + 2] = element + ' (3)'
							adj_arr[counter + 2][0] = adj_arr[0][counter]
					
					#and in any event do the following to our pair of same cards:
					
					#append ' (1)' to the end of this card's name
					adj_arr[0][counter] = element + ' (1)'
					adj_arr[counter][0] = adj_arr[0][counter]
					
					
					#append ' (2)' to the end of the next card's name
					adj_arr[0][counter + 1] = element + ' (2)'
					adj_arr[counter + 1][0] = adj_arr[0][counter]
				
			#create new vertex
			deck_graph.add_node(counter, card_name = adj_arr[0][counter])

			
			#for all cards before this card (fix to the counter-th row, checking each column from 1 to counter - 1)
			for other_card_index in range(0, counter - 1):
				#create edge between this card and the other card if they are connected.
				if(adj_arr[counter][other_card_index] == 1):
					deck_graph.add_edge(counter, other_card_index)
	return(deck_graph)

def deck_grapher():
	
	deck_graph = create_deck_graph()
	
	card_names_by_node = dict(deck_graph.nodes.data())
	
	for key, value in card_names_by_node.items():
		card_names_by_node[key] = value['card_name']
	
	#creates layout (this is that cool spring thing you read about recently)
	#deck_layout = nx.spring_layout(deck_graph)
	deck_layout = nx.circular_layout(deck_graph, scale = 5)
	
	nx.draw(deck_graph, pos = deck_layout, labels = card_names_by_node, font_size = 7, font_color = 'blue', edge_color = 'pink', node_color = 'yellow')
	plt.show()
	
	#graph_draw(deck_graph, pos, output_size=(1000, 1000), vertex_color=[1,1,1,0], vertex_size=1, edge_pen_width=1.2, output="price.png")

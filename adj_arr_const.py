from file_input_output import *

#retrieves selected entry and [the zero-valued] adjacency arrays, then uses the former to value the latter
def construct_data_arr():
	#find default directory
	pathways = []
	with open("paths.txt") as f:
		pathways = f.readlines()
		f.close()
	default_path = pathways[1]
	
	default_path = default_path.strip()
	

	#retrieve the data from the CSV files.
	adj_arr, csv_file_name = read_csv('Select Adjacency Array', default_path, True)
	
	
	#get number of cards in deck
	deck_size = len(adj_arr)

	#if adj. array already has been valued, don't bother with the rest, just.
	for i in range(1, deck_size):
		for j in range(1, deck_size):
			if(adj_arr[i][j] == 1):
				return(adj_arr)
	
	#otherwise, do all this
	
	
	entry_arr = read_csv('Select Entry Array', default_path)
	
	#get number of unique cards in deck
	unq_deck_size = len(entry_arr)
	

	#start checking from 12 in adj array (keeping in mind that the header row and leader column have the 0 spots, and 0,0 is empty
	#[11 12 13]
	#[21 22 23]
	#[31 32 33]

	#establish lower bound on needed reference in entry array (for example, for Yugioh, after the first three main deck cards are completed, it is impossible for the first entry in the entry array to come up again, so it is a waste to check it
	min_ent_rc = 1
	
	for adj_col in range(1, deck_size):
		min_ent_rc = int(adj_col // 3) + 1
		for ent_col in range(min_ent_rc, unq_deck_size):
			if(adj_arr[0][adj_col] == entry_arr[0][ent_col]):
				for adj_row in range(adj_col + 1, deck_size):
					for ent_row in range(min_ent_rc, unq_deck_size):
						if(adj_arr[adj_row][0] == entry_arr[ent_row][0]):
							adj_arr[adj_row][adj_col] = entry_arr[ent_row][ent_col] + entry_arr[ent_col][ent_row]
	
	#fill out the other half of the matrix if needed (the true adjacency matrix in our case is symmetric):
	for row in range (1, deck_size):
		for column in range(1,row):
			adj_arr[column][row] = adj_arr[row][column]
			
	
	#write adj arr to file for future use.
	with open(csv_file_name, 'w', newline = '') as csvfile:
		writerthing = csv.writer(csvfile, delimiter = ',')
		for line in adj_arr:
			writerthing.writerow(line)
		csvfile.close
	
		
	return(adj_arr)
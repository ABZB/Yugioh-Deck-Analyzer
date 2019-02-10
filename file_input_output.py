from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
import tkinter as tk
import csv
from Database_Handling import *

def save_deck_text(card_name_array, end_name, out_path, deck_counter, side_deck_counter, which_program, additional_lines = []):
	
	
	#removes .ydk extension from deck's file's name
	end_name = end_name.replace(".ydk","")
	
	# if just printing a decklist
	if(which_program == "convert_ydk_to_txt"):
	

		#gets/creates filename as per (text file, opening window in output path specified in paths.txt file, default extension of .txt, with default name being the name of the deck file)
		file_name = asksaveasfilename(initialdir = out_path,  defaultextension = ".txt", initialfile = end_name)
		
		#totals for Main and Extra Decks
		total_monsters = deck_counter[0] + deck_counter[1] + deck_counter[2]
		total_spells = deck_counter[3] + deck_counter[4] + deck_counter[5] + deck_counter[6] + deck_counter[7]
		total_traps = deck_counter[8] + deck_counter[9] + deck_counter[10]
		total_main_deck = total_monsters + total_spells + total_traps
		total_extra = deck_counter[11] + deck_counter[12] + deck_counter[13] + deck_counter[14]
		
		#totals for Side Deck
		side_total_monsters = side_deck_counter[0] + side_deck_counter[1] + side_deck_counter[2]
		side_total_spells = side_deck_counter[3] + side_deck_counter[4] + side_deck_counter[5] + side_deck_counter[6] + side_deck_counter[7]
		side_total_traps = side_deck_counter[8] + side_deck_counter[9] + side_deck_counter[10]
		side_total_extra = side_deck_counter[11] + side_deck_counter[12] + side_deck_counter[13] + side_deck_counter[14]
		side_total = side_total_monsters + side_total_spells + side_total_traps + side_total_extra
		
		#calcs
		deck_five = total_main_deck * (total_main_deck - 1) * (total_main_deck - 2) * (total_main_deck - 3) * (total_main_deck - 4) 
		deck_six = deck_five * (total_main_deck - 5)
		
		#Probability no monsters level 4 or lower
		P0L4L5 = ((total_main_deck - deck_counter[2])*(total_main_deck - deck_counter[2]-1)*(total_main_deck - deck_counter[2]-2)*(total_main_deck - deck_counter[2]-3)*(total_main_deck - deck_counter[2]-4))/deck_five
		P0L4L6 = P0L4L5 * (total_main_deck - deck_counter[2]-5) * deck_five / deck_six
		
		#Probability At Least One level 4 or lower
		
		PaL1L4L5 = 1 - P0L4L5
		PaL1L4L6 = 1 - P0L4L6
		
		
		PaL1C5 = 1 - (total_main_deck-1)*(total_main_deck - 2)*(total_main_deck - 3)*(total_main_deck - 4)*(total_main_deck - 5)/deck_five
		PaL2C5 = 1 - (total_main_deck-2)*(total_main_deck - 3)*(total_main_deck - 4)*(total_main_deck - 5)*(total_main_deck - 6)/deck_five
		PaL3C5 = 1 - (total_main_deck-3)*(total_main_deck - 4)*(total_main_deck - 5)*(total_main_deck - 6)*(total_main_deck - 7)/deck_five
		PaL4C5 = 1 - (total_main_deck-4)*(total_main_deck - 5)*(total_main_deck - 6)*(total_main_deck - 7)*(total_main_deck - 8)/deck_five
		PaL5C5 = 1 - (total_main_deck-5)*(total_main_deck - 6)*(total_main_deck - 7)*(total_main_deck - 8)*(total_main_deck - 9)/deck_five
		PaL6C5 = 1 - (total_main_deck-6)*(total_main_deck - 7)*(total_main_deck - 8)*(total_main_deck - 9)*(total_main_deck - 10)/deck_five
		PaL7C5 = 1 - (total_main_deck-7)*(total_main_deck - 8)*(total_main_deck - 9)*(total_main_deck - 10)*(total_main_deck - 11)/deck_five
		PaL8C5 = 1 - (total_main_deck-8)*(total_main_deck - 9)*(total_main_deck - 10)*(total_main_deck - 11)*(total_main_deck - 12)/deck_five
		PaL9C5 = 1 - (total_main_deck-9)*(total_main_deck - 10)*(total_main_deck - 11)*(total_main_deck - 12)*(total_main_deck - 13)/deck_five
		
		PaL1C6 = 1 - (total_main_deck-1)*(total_main_deck - 2)*(total_main_deck - 3)*(total_main_deck - 4)*(total_main_deck - 5)*(total_main_deck - 6)/deck_six
		PaL2C6 = 1 - (total_main_deck-2)*(total_main_deck - 3)*(total_main_deck - 4)*(total_main_deck - 5)*(total_main_deck - 6)*(total_main_deck - 7)/deck_six
		PaL3C6 = 1 - (total_main_deck-3)*(total_main_deck - 4)*(total_main_deck - 5)*(total_main_deck - 6)*(total_main_deck - 7)*(total_main_deck - 8)/deck_six
		PaL4C6 = 1 - (total_main_deck-4)*(total_main_deck - 5)*(total_main_deck - 6)*(total_main_deck - 7)*(total_main_deck - 8)*(total_main_deck - 9)/deck_six
		PaL5C6 = 1 - (total_main_deck-5)*(total_main_deck - 6)*(total_main_deck - 7)*(total_main_deck - 8)*(total_main_deck - 9)*(total_main_deck - 10)/deck_six
		PaL6C6 = 1 - (total_main_deck-6)*(total_main_deck - 7)*(total_main_deck - 8)*(total_main_deck - 9)*(total_main_deck - 10)*(total_main_deck - 11)/deck_six
		PaL7C6 = 1 - (total_main_deck-7)*(total_main_deck - 8)*(total_main_deck - 9)*(total_main_deck - 10)*(total_main_deck - 11)*(total_main_deck - 12)/deck_six
		PaL8C6 = 1 - (total_main_deck-8)*(total_main_deck - 9)*(total_main_deck - 10)*(total_main_deck - 11)*(total_main_deck - 12)*(total_main_deck - 13)/deck_six
		PaL9C6 = 1 - (total_main_deck-9)*(total_main_deck - 10)*(total_main_deck - 11)*(total_main_deck - 12)*(total_main_deck - 13)*(total_main_deck - 14)/deck_six

		
		with open(file_name, 'w') as d:
			d.write('Deck Name: ' + end_name + '\n' + '\n')
			d.write('Card Count:' + '\n')
			
			d.write(str(total_main_deck) + ' Cards in Main Deck' + '\n'+ '\n')
			
			d.write('\t' + str(total_monsters) + ' Monster Cards total' + '\n')
			d.write('\t' + '\t' + str(deck_counter[0]) + ' Level 7+' + '\n')
			d.write('\t' + '\t' + str(deck_counter[1]) + ' Level 5-6' + '\n')
			d.write('\t' + '\t' + str(deck_counter[2]) + ' Level 1-4' + '\n' + '\n')
			
			d.write('\t' + str(total_spells) + ' Spell Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[3]) + ' Normal Spell Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[4]) + ' Quick-Play Spell Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[5]) + ' Equip Spell Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[6]) + ' Continuous Spell Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[7]) + ' Field Spell Cards' + '\n' + '\n')
			
			d.write('\t' + str(total_traps) + ' Trap Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[8]) + ' Normal Trap Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[9]) + ' Continuous Trap Cards' + '\n')
			d.write('\t' + '\t' + str(deck_counter[10]) + ' Counter Trap Cards' + '\n' + '\n')
			
			d.write(str(total_extra) + ' Fusion, Synchro, XYZ, & Link Monsters' + '\n')
			d.write('\t' + str(deck_counter[11]) + ' Fusion Monsters' + '\n')
			d.write('\t' + str(deck_counter[12]) + ' Synchro Monsters' + '\n')
			d.write('\t' + str(deck_counter[13]) + ' XYZ Monsters' + '\n')
			d.write('\t' + str(deck_counter[14]) + ' Link Monsters' + '\n' + '\n')
			
			d.write(str(side_total) + ' Cards in Side Deck' + '\n')
			d.write('\t' + str(side_total_monsters) + ' Main Deck Monsters' + '\n')
			d.write('\t' + str(side_total_spells) + ' Spell Cards' + '\n')
			d.write('\t' + str(side_total_traps) + ' Trap Cards' + '\n')
			d.write('\t' + str(side_total_extra) + ' Fusion, Synchro, XYZ, & Link Monsters' + '\n')
		
			current_card = ''
			
			for i in card_name_array:
				if i == '#created by ...':
					i = ''
				elif i == '#main':
					d.write("\n")
					d.write('Main Deck:')
					d.write("\n")
				elif i == '#extra':
					d.write("\n")
					d.write('Extra Deck:')
					d.write("\n")
				elif i == '!side':
					d.write("\n")
					d.write('Side Deck:')
					d.write("\n")
				elif current_card != i:
					multiplicity = card_name_array.count(i)
					current_card = i
					d.write(str(multiplicity) + ' x ' + i)
					d.write("\n")
			
			d.write("\n")
			d.write("\n")
			
			d.write('Basic Deck Analysis:' + '\n' + '\n')
			#d.write('Probability of 0 Level 4 or lower Monsters in your first hand if you go first: ' + str(round(P0L4L5*100,2)) + '% / second: ' + str(round(P0L4L6*100,2)) + '%\n')
			#d.write('Probability of at least 1 Level 4 or lower Monsters in your first hand if you go first: ' + str(round(PaL1L4L5*100,2)) + '% / second: ' + str(round(PaL1L4L6*100,2)) + '%\n' + '\n')
			
			d.write('Probability of at least 1 of a card you have (x+y) copies of, where x is the number of copies of the card and y is the number of cards that can search for that card:' + '\n' + '\n')
			
			
			d.write('Probability of at least 1 of a card you have x+y = 1 of in your first hand if you go first: ' + str(round(PaL1C5*100,2)) + '% / second: ' + str(round(PaL1C6*100,2)) + '%\n')
			d.write('Probability of at least 1 of a card you have x+y = 2 of in your first hand if you go first: ' + str(round(PaL2C5*100,2)) + '% / second: ' + str(round(PaL2C6*100,2)) + '%\n')
			d.write('Probability of at least 1 of a card you have x+y = 3 of in your first hand if you go first: ' + str(round(PaL3C5*100,2)) + '% / second: ' + str(round(PaL3C6*100,2)) + '%\n')
			d.write('Probability of at least 1 of a card you have x+y = 4 of in your first hand if you go first: ' + str(round(PaL4C5*100,2)) + '% / second: ' + str(round(PaL4C6*100,2)) + '%\n')
			d.write('Probability of at least 1 of a card you have x+y = 5 of in your first hand if you go first: ' + str(round(PaL5C5*100,2)) + '% / second: ' + str(round(PaL5C6*100,2)) + '%\n')
			d.write('Probability of at least 1 of a card you have x+y = 6 of in your first hand if you go first: ' + str(round(PaL6C5*100,2)) + '% / second: ' + str(round(PaL6C6*100,2)) + '%\n')
			#d.write('Probability of at least 1 of a card you have x+y = 7 of in your first hand if you go first: ' + str(round(PaL7C5*100,2)) + '% / second: ' + str(round(PaL7C6*100,2)) + '%\n')
			#d.write('Probability of at least 1 of a card you have x+y = 8 of in your first hand if you go first: ' + str(round(PaL8C5*100,2)) + '% / second: ' + str(round(PaL8C6*100,2)) + '%\n')
			#d.write('Probability of at least 1 of a card you have x+y = 9 of in your first hand if you go first: ' + str(round(PaL9C5*100,2)) + '% / second: ' + str(round(PaL9C6*100,2)) + '%\n')
			
			#writes full report
			if(len(additional_lines) > 0):
				d.write('\n' + '\n')
				
				for lines in additional_lines:
					d.write('\n')
					d.write(lines)
			
			d.close()
			
	#if initializing the matrices for analysis
	elif(which_program == 'create_daacsv' or which_program == 'create_decsv'):
		
		
		
		#remove the header for maindeck in the card name list
		del card_name_array[1]
		
		#empties what will become the upper-left cell of the final array
		card_name_array[0] = ''
		
		
		#Create full Adjacency Matrix CSV
		
		if(which_program == 'create_daacsv' or which_program == 'create_decsv'):
			#Create the new file name
			file_name = asksaveasfilename(initialdir = out_path,  defaultextension = ".txt", initialfile = end_name[:-4] + '-Adjacency Array.csv')
			adj_arr = [0] * (len(card_name_array))
			
			for i in range(len(card_name_array)):
				adj_arr[i] = [0] * len(card_name_array)
			
			#create CSV to enter adjacency matrix
			for i,card in enumerate(card_name_array):
				
				#Append Card Name to 0th row, ith column
				adj_arr[0][i] = card
				#Append Card name to ith row, 0th column
				adj_arr[i][0] = card
			
			#Create Adjacency Array for the deck
			with open(file_name, 'w', newline = '') as csvfile:
				writerthing = csv.writer(csvfile, delimiter = ',')
				for line in adj_arr:
					writerthing.writerow(line)
				csvfile.close
		
		#Create Data-Entry CSV
		
		if(which_program == 'create_decsv'):
			#Create the new file name
			file_name = asksaveasfilename(initialdir = out_path,  defaultextension = ".txt", initialfile = end_name[:-4] + '-Entry Array.csv')
			#remove duplicate entries for the entry array
			unique_cards_in_main_deck = len(card_name_array)

			index = 0
			
			while True:
				if index >= unique_cards_in_main_deck - 1:
					break
				elif card_name_array[index] == card_name_array[index + 1]:
					del card_name_array[index]
					unique_cards_in_main_deck = unique_cards_in_main_deck - 1
				else:
					index = index + 1
			
			#create new adjacency array for entering values, all empty
			
			adj_arr = [''] * (len(card_name_array))
			
			for i in range(len(card_name_array)):
				adj_arr[i] = [''] * len(card_name_array)
			
			#create CSV to enter adjacency matrix
			for i,card in enumerate(card_name_array):
				
				#Append Card Name to 0th row, ith column
				adj_arr[0][i] = card
				#Append Card name to ith row, 0th column
				adj_arr[i][0] = card
				
			for i in range(len(card_name_array)):
				if i>0:
					for j in range(1,i+1):
						adj_arr[i][j] = 0
			
			#Create Entry Adjacency Array for the deck
			with open(file_name, 'w', newline = '') as csvfile2:
				writerthing = csv.writer(csvfile2, delimiter = ',')
				for line in adj_arr:
					writerthing.writerow(line)
				csvfile2.close
				
				

def extract(which_program, additional_lines = []):

	update_cdbs()

	#path for pulling .cdb files
	pathways = []
	with open("paths.txt") as f:
		pathways = f.readlines()
		
	output_path = pathways[1].strip()
	
	deck_path = pathways[0].strip() + "/deck/" #pathway to deck folder
	
	
	#opens open file dialogue, default directory is the /deck folder from your specified YgoPro directory
	deck_name = askopenfilename(filetypes = (("YgoPro Deck Files", "*.ydk"), ("All Files", "*.*")), initialdir = deck_path)
	
	#array to store found card names while iterating through databases
	temp_array = []
	
	
	#open .ydk file
	with open(deck_name) as f:
		#read card ids from .ydk file
		deck_list_temp = f.readlines()
		
		
	copied_cdb_path = os.getcwd() + "/"
	
	#[Monsters 7+, Monsters 5-6, Monsters 1-4, Normal Spells, Quick-Play Spells, Equip Spells, Continuous Spells, Field Spells, Normal Traps, Continuous Traps, Counter Traps, Fusion, Synchro, XYZ, Link] whitespace in array in next line seperates between monster/spell/trap/extra groupings
	deck_counter = [0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0,0]
	
	#switches between main/extra and side deck
	in_side_deck = False
	#cards in side deck
	side_deck_counter = [0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0,0]
	
	if(which_program == 'convert_ydk_to_txt'):
		counted_this_card_name = []
		#iterarates through every .cdb file in directory. Will fail if program is in different folder than the .cdb files.
		for data_number, file in enumerate([doc for doc in os.listdir(copied_cdb_path) if doc.endswith(".cdb")]):
			con = sqlite3.connect(file)
			with con:
				c = con.cursor()
				#iterate through all the lines.
				for i in range(len(deck_list_temp)):
					#remove newlines, ensures is string
					if data_number == 0:
						deck_list_temp[i] = str(deck_list_temp[i]).strip()
					
					#switches between deck and side deck
					if deck_list_temp[i] == '!side':
						in_side_deck = True
					elif(deck_list_temp[i] == '#main' or deck_list_temp[i] == '#extra'):
						in_side_deck = False
					
					#put id number in a format to be parsed by sql
					t = (deck_list_temp[i],)
					
					#grabs every name that matches card id (should only be 1)
					c.execute("SELECT name FROM texts WHERE id=?", t)
					cardname = c.fetchone()
					
					#if the current .cdb does not have current card id...
					if cardname is None:
						#if this is the first .cdb, append the card id number as a placeholder
						if(data_number == 0):
							temp_array.append(deck_list_temp[i])
							counted_this_card_name.append(False)
					#if card id is found
					else:
						#remove the extra characters picked up from SQlite
						cardname = str(cardname)
						cardname = cardname.replace("',)","")
						cardname = cardname.replace("('","")
						cardname = cardname.replace('",)',"")
						cardname = cardname.replace('("',"")
						cardname = cardname.strip()
						#if this is the first .cdb, append card name
						if(data_number == 0):
							temp_array.append(cardname)
							#append False, set it to true after we do the deck counter, otherwise we'd have to have that whole thing twice
							counted_this_card_name.append(False)
						#otherwise overwrite card id with card name in the array
						else:
							temp_array[i] = cardname
						
						#in either case, if we haven't counted this card before, count the card type to the appropriate counter array:
						if(not(counted_this_card_name[i])):
							if(in_side_deck):
								side_deck_counter = card_type_to_array(c, t, side_deck_counter)
							else:
								deck_counter = card_type_to_array(c, t, deck_counter)
							
						#now that we've found this card once, ensure that we will not count it again:
						counted_this_card_name[i] = True
	
	elif(which_program == 'create_decsv' or which_program == 'create_daacsv'):
		#iterarates through every .cdb file in directory. Will fail if program is in different folder than the .cdb files.
		for data_number, file in enumerate([doc for doc in os.listdir(copied_cdb_path) if doc.endswith(".cdb")]):
			con = sqlite3.connect(file)
			with con:
				c = con.cursor()
				#iterate through all the lines.
				for i in range(len(deck_list_temp)):
					#remove newlines, ensures is string
					if data_number == 0:
						deck_list_temp[i] = str(deck_list_temp[i]).strip()
					
					#stops checking after it finishes the main deck
					if(deck_list_temp[i] == '#extra'):
						break
					
					#put id number in a format to be parsed by sql
					t = (deck_list_temp[i],)
					
					#grabs every name that matches card id (should only be 1)
					c.execute("SELECT name FROM texts WHERE id=?", t)
					cardname = c.fetchone()
					
					#if the current .cdb does not have current card id...
					if(cardname is None):
						#if this is the first .cdb, append the card id number as a placeholder
						if data_number == 0:
							temp_array.append(deck_list_temp[i])
					#if card id is found
					else:
						#remove the extra characters picked up from SQlite
						cardname = str(cardname)
						cardname = cardname.replace("',)","")
						cardname = cardname.replace("('","")
						cardname = cardname.replace('",)',"")
						cardname = cardname.replace('("',"")
						cardname = cardname.strip()
						#if this is the first .cdb, append card name
						if(data_number == 0):
							temp_array.append(cardname)
						#otherwise overwrite card id with card name in the array
						else:
							temp_array[i] = cardname
						
			data_number += 1
						
	#opens save file dialogue with name of deck as default
	save_deck_text(temp_array, os.path.basename(deck_name), output_path, deck_counter, side_deck_counter, which_program, additional_lines)

#writes selected CSV file to 2D array, also passes up path name if needed
def read_csv(what_file, default_path, also_tell_path = False):

	#opens open file dialogue, default directory is the default output folder
	csv_file_name = askopenfilename(filetypes = ((what_file, "*.csv"), ("All Files", "*.*")), initialdir = default_path)
	
	with open(csv_file_name, 'r', newline = '') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		data_read = []
		for row_number, row in enumerate(reader):
			row_read = []
			for column, element in enumerate(row):
				if(column == 0 or row_number == 0):
					row_read.append(element)
				elif(element == ''):
					row_read.append(0)
				else:
					row_read.append(int(element))
			data_read.append(row_read)
	if(also_tell_path):
		return(data_read, csv_file_name)
	else:
		return(data_read)
import sqlite3
import sys
import os
import io
import string
import shutil
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
import tkinter as tk
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter


def	update_cdbs():
	#grab paths from text file
	pathways = []
	with open("paths.txt") as f:
		pathways = f.readlines()
		f.close()
	cdb_path = pathways[0].strip() + "/"

	
	#path for main .cdb_path
	directories_list = [cdb_path]
	
	#pathway to .cdb expansion folder
	cdb_path = cdb_path.strip() + "expansions/" #pathway to .cdb folder
	
	directories_list.append(cdb_path)
	
	#Adds in subfolders of expansions if there are.
	#if ygopro_version_check != "is_ygopro2 = true":
	#If they add new subfolders, update this list. Update to just grab list of subfolders of expansions at some point.
	temp_dir = ["live/","live2016/","live2017/","liveanime/","live2017links/","liveanimelinks/"]
	
	for i in temp_dir:
		directories_list.append(cdb_path + i)
		
	#get current directory
	current_directory = os.getcwd() + "/"
	
	#avoids overwriting of same filename in different subfolders
	filenumber = 0
	
	for j in directories_list:
		j = j.strip()
	
	#copy over .cdb databases
	for paths in directories_list:
		for file in [doc for doc in os.listdir(paths) if doc.endswith(".cdb")]:
			shutil.copy2(paths + os.path.basename(file), current_directory + str(filenumber) + os.path.basename(file))
			filenumber += 1

def get_card_type(c, t):
	c.execute("SELECT type FROM datas WHERE id=?", t)
	card_type = str(c.fetchone())
	card_type = card_type.replace("'","")
	card_type = card_type.replace("(","")
	card_type = card_type.replace(')',"")
	card_type = card_type.replace('"',"")
	card_type = card_type.replace(',',"")
	card_type = int(card_type)
	return(card_type)

def get_card_level(c, t):
	c.execute("SELECT level FROM datas WHERE id=?", t)
	card_level = str(c.fetchone())
	card_level = card_level.replace("'","")
	card_level = card_level.replace("(","")
	card_level = card_level.replace(')',"")
	card_level = card_level.replace('"',"")
	card_level = card_level.replace(',',"")
	return(card_level)
	
def card_type_to_array(c, t, deck_counter):

	card_type = get_card_type(c, t)
	#is a monster
	if card_type & 1 == 1:
		if card_type & 64 == 64:#Fusion
			deck_counter[11] += 1
		elif card_type & 8192 == 8192:#Synchro
			deck_counter[12] += 1
		elif card_type & 8388608 == 8388608:#XYZ
			deck_counter[13] += 1
		elif card_type & 67108864 == 67108864:#Link
			deck_counter[14] += 1
		else:#maindeck monster
			card_level = int(get_card_level(c, t))
			if card_level >= 7:
				deck_counter[0] += 1
			elif card_level >= 5:
				deck_counter[1] += 1
			else:
				deck_counter[2] += 1
	#is a spell
	elif card_type & 2 == 2:
		if card_type & 524288 == 524288:#Field
			deck_counter[7] += 1
		elif card_type & 65536 == 65536:#quick-play
			deck_counter[4] += 1
		elif card_type & 262144 == 262144:#Equip
			deck_counter[5] += 1
		elif card_type & 131072 == 131072:#Continuous
			deck_counter[6] += 1
		else:#normal
			deck_counter[3] += 1
	#is a trap
	else:
		if card_type & 1048576 == 1048576:#Counter
			deck_counter[10] += 1
		elif card_type & 131072 == 131072:#Continuous
			deck_counter[9] += 1
		else:#normal
			deck_counter[8] += 1
	return(deck_counter)
	
	#deck_counter indices
	#0 Monsters 7+
	#1 Monsters 5-6
	#2 Monsters 1-4
	#3 Normal Spells
	#4 Quick-Play Spells
	#5 Equip Spells
	#6 Continuous Spells
	#7 Field Spells
	#8 Normal Traps
	#9 Continuous Traps
	#10 Counter Traps
	#11 Fusion
	#12 Synchro
	#13 XYZ
	#14 Link
	
	#Monster 0x1 (1)
	#Spell 0x2 (2)--Normal Spells use this, no need to use the "Normal" for monsters.
	#Trap 0x4 (4)--Same goes for Normal traps
	#Normal 0x10 (16)
	#Effect 0x20 (32)--Don't forget this because your card may be immune to Skill Drain but we have to be fair for everyone unless it's really a unique card.
	#Fusion 0x40 (64)
	#Ritual 0x80 (128) (129 for effectless monsters, 130 for their spells)
	#Spirit 0x200 (512)
	#Union 0x400 (1024)
	#Gemini 0x800 (2048)
	#Tuner 0x1000 (4096)
	#Synchro 0x2000 (8192)
	#Token 0x4000 (16384)
	#Flip 0x200000 (2097152)
	#Toon 0x400000 (4194304)
	#Xyz 0x800000 (8388608)
	#Link 0x2000000 (67108864)
	#Pendulum 0x1000000 (16777216)
	#Special-summon 0x2000000 (32965616)
	#Quick-Play 0x10000 (65536)
	#Continuous 0x20000 (131072) --Same goes here, both Spell and Traps use this.
	#Equip 0x40000 (262144)
	#Field 0x80000 (524288)
	#Counter 0x100000 (1048576)

def save_deck_text(card_name_array, end_name, out_path, deck_counter, side_deck_counter, which_program, additional_lines = []):
	
	
	#removes .ydk extension from deck's file's name
	end_name = end_name.replace(".ydk","")
	
	# if running a decklist
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
			
	#if running graph-node thing
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
		f.close()
		
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
		f.close()
		
		
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
		#remembers if a particular card has been already read (some cards appear in more than 1 database)
		count_only_once = []
		for file in [doc for doc in os.listdir(copied_cdb_path) if doc.endswith(".cdb")]:
			con = sqlite3.connect(file)
			with con:
				c = con.cursor()
				#iterate through all the lines.
				for i in range(len(deck_list_temp)):
					#remove newlines, ensures is string
					if data_number == 0:
						deck_list_temp[i] = str(deck_list_temp[i]).strip()
					
					#stops checking after it finishes the main deck
					if deck_list_temp[i] == '#extra':
						break
					
					#put id number in a format to be parsed by sql
					t = (deck_list_temp[i],)
					
					#grabs every name that matches card id (should only be 1)
					c.execute("SELECT name FROM texts WHERE id=?", t)
					cardname = c.fetchone()
					
					#if the current .cdb does not have current card id...
					if cardname is None:
						#if this is the first .cdb, append the card id number as a placeholder
						if data_number == 0:
							temp_array.append(deck_list_temp[i])
							count_only_once.append(0)
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
						if data_number == 0:
							temp_array.append(cardname)
							if in_side_deck == 0:
								deck_counter = card_type_to_array(c, t, deck_counter)
							else:
								side_deck_counter = card_type_to_array(c, t, side_deck_counter)
							count_only_once.append(1)
						#otherwise overwrite card id with card name in the array
						else:
							temp_array[i] = cardname
							if count_only_once[i] == 0:
								if in_side_deck == 0:
									deck_counter = card_type_to_array(c, t, deck_counter)
								else:
									side_deck_counter = card_type_to_array(c, t, side_deck_counter)
								count_only_once[i] = 1
						
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
		return data_read

	
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


def analyze_and_display():
	report = analyze_adj_arr()
	words_report = ''
	for line in report:
		words_report += line + '\n' 
	root = tk.Tk()
	T = tk.Text(root, height=500, width=500)
	T.pack()
	T.insert(1.0, words_report)

def data_entry_refresh_warning():
	
	root_refresh_warning = tk.Tk()

	frame_refresh_warning = tk.Frame(root_refresh_warning)
	frame_refresh_warning.pack()

	
	if(tk.messagebox.askyesno('Warning:', 'You will need to re-enter all values in the Data-Entry form if you overwrite the old one. Proceed?')):
		extract("create_decsv")
	root_refresh_warning.mainloop()

	
def update_paths(folder_selection):
	
	if(os.path.exists('paths.txt')):
	
		with open("paths.txt", 'r') as f:
			pathways = f.readlines()
			f.close()
			
		if(len(pathways) >= 2):
			if(folder_selection == 'ygopro'):
				chosen_path = pathways[0].strip()
			elif(folder_selection == 'output'):
				chosen_path = pathways[1].strip()
			chosen_path = askdirectory(initialdir = chosen_path) + '\n'
		else:
			chosen_path = askdirectory() + '\n'
	else:
		chosen_path = askdirectory() + '\n'
	
	#if file is empty, write the current selection to line 1, and blank to line 2
	if(len(pathways) == 0):
		pathways = [' \n','']
	#if only one entry, then write the new entry to it's appropriate slot, and assume the other entry is correct for the other entry, so just duplicate it.
	elif(len(pathways) == 1):
		pathways.append(pathways[0])
	
	#now either we have [entry, blank line], [blank line, entry], or [entry1, entry 2]
	if(folder_selection == 'ygopro'):
		pathways[0] = chosen_path
	elif(folder_selection == 'output'):
		pathways[1] = chosen_path
	
	with open("paths.txt", 'w') as f:
		for line in pathways:
			f.write(line)
		
	
def select_directories():
	root_options_menu = tk.Tk()

	frame_options_menu = tk.Frame(root_options_menu)
	frame_options_menu.pack()
		
	root_options_menu.title('Select Directory to Update')
	
	tk.Button(frame_options_menu, text = 'Select YgoPro Folder', command = lambda: update_paths('ygopro'), height = 2, width = 50, pady = 1).pack()
	
	tk.Button(frame_options_menu, text = 'Select Output Folder', command = lambda: update_paths('output'), height = 2, width = 50, pady = 1).pack()
	
	tk.Button(frame_options_menu, text="Exit", command = root_options_menu.destroy, height = 2, width = 25, pady = 1).pack()
	
	root_options_menu.lift()
	
	root_options_menu.mainloop()
	
def button_prompt_main_menu():
	root_main_menu = tk.Tk()

	frame_main_menu = tk.Frame(root_main_menu)
	frame_main_menu.pack()
		
	root_main_menu.title('Select a Subprogram to Run')

	tk.Button(frame_main_menu, text = 'Convert .ydk to .txt', command = lambda: extract("convert_ydk_to_txt"), height = 2, width = 50, pady = 1).pack()

	tk.Button(frame_main_menu, text = 'Write Analysis and Deck List to file', command = lambda: extract('convert_ydk_to_txt', analyze_adj_arr()), height = 2, width = 50, pady = 1).pack()

	tk.Button(frame_main_menu, text = 'Analyse Deck and Display Results', command = analyze_and_display, height = 2, width = 50, pady = 1).pack()

	tk.Button(frame_main_menu, text = 'Display Deck Network', command = deck_grapher, height = 2, width = 50, pady = 1).pack()

	tk.Button(frame_main_menu, text = 'Create/Refresh Deck Array from .ydk', command = lambda: extract("create_daacsv"), height = 2, width = 50, pady = 1).pack()

	tk.Button(frame_main_menu, text = 'Create/Refresh data-entry form from .ydk', command = data_entry_refresh_warning, height = 2, width = 50, pady = 1).pack()
	
	directory_select = tk.Menubutton(frame_main_menu, text = 'Select Directories', height = 2, width = 50, pady = 1)
	
	picks = tk.Menu(directory_select, tearoff = False)
	
	picks.add_command(label = 'Select YgoPro Folder', command = lambda: update_paths('ygopro'))
	
	picks.add_command(label = 'Select Output Folder', command = lambda: update_paths('output'))
	
	directory_select['menu'] = picks
	
	directory_select.config(bd = 1, relief = 'raised')
	
	directory_select.pack()
	
	
	tk.Button(frame_main_menu, text="Exit", command = root_main_menu.destroy, height = 2, width = 25, pady = 1).pack()
	
	root_main_menu.mainloop()	


button_prompt_main_menu()

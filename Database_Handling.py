import sqlite3
import sys
import os
import io

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
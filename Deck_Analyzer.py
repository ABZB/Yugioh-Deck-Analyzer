from graph_math import *
from adj_arr_const import *

def analyze_and_display():
	report = analyze_adj_arr()
	words_report = ''
	for line in report:
		words_report += line + '\n' 
	analysis_window = tk.Tk()
	T = tk.Text(analysis_window, height=500, width=500)
	T.pack()
	T.insert(1.0, words_report)
	analysis_window.mainloop()

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

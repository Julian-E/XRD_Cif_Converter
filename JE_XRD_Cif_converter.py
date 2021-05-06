import sys
import os
import os.path
from os import path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import askdirectory
import ctypes  # for def Mbox

def Mbox(title, text, style):
	##  Styles:
	##  0 : OK
	##  1 : OK | Cancel
	##  2 : Abort | Retry | Ignore
	##  3 : Yes | No | Cancel
	##  4 : Yes | No
	##  5 : Retry | Cancel 
	##  6 : Cancel | Try Again | Continue

    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global root
    root = tk.Tk() #opens GUI window
    top1 = Toplevel1(root) #sets GUI-Window as Toplevel1! Toplevels can be considered as Windows. Define in own Class!
    #top2 = tk.Toplevel() #-------would create a second window (Topleve2). tkinter-method!!! TAKE CARE: If u close the second Window, you will not get outta root.mainloop!
    #top2.title('Second Window') #titel for second Toplevel
    #Button2 = tk.Button(master=top2, text="Hi", command=func_Button2) #Button2 refers to top2 "master=top2"
    #Button2.pack()#pack-methode to get Button2 on its Master (top2)
    
    #print(top1)
    root.mainloop()

def activate_Button1():
	directory_cif = askdirectory()
	Entry1.delete(0, tk.END)
	Entry1.insert(0, directory_cif)

def activate_Button2():
	if output_radiobuttons.get() == 2:
		directory_output = askdirectory()
		Entry2.delete(0, tk.END)
		Entry2.insert(0, directory_output)

def activate_Button3():
	directory_log = askdirectory()
	Entry3.delete(0, tk.END)
	Entry3.insert(0, directory_log)
	read_Entry4 = Entry4.get()
	if read_Entry4 == os.getcwd():
		Entry4.delete(0, tk.END)
		Entry4.insert(0, directory_log)

def activate_Button4():
	directory_error = askdirectory()
	Entry4.delete(0, tk.END)
	Entry4.insert(0, directory_error)

def activate_Button5():
	count = int(1) #will be needed in line 200, if radiobutton2 is active and there are cif files with the same name but in different directories

	#check if Entry1 (cif-directory) is existing and not empty!
	if Entry1.get() == "":
		Mbox("Error", "cif-directory cannot be empty. Please sign in a valid path.", 0)
		return #return can not only return a value which will be passed to a variable but can also exit a def-function!!!!
	else:
		if path.exists(str(Entry1.get())) == False:
			Mbox("Error", "cif-directory doesn't exist. Please sign in a valid path.", 0)
			Entry1.delete(0, tk.END)
			return #exit def
	#if second radiobutton is checked, check if Entry2 isn't empty!
	if output_radiobuttons.get() == 2:
		if Entry2.get() == "":
			Mbox("Error", "output-directory cannot be empty. Please sign in a valid path.", 0)
			return #exit def

	#search for all .cif-files in given directory Entry1.get() and stores them in list_cif_files
	list_cif_files = []
	for dirpath, dirnames, filenames in os.walk(Entry1.get()):
		for filename in [f for f in filenames if f.endswith(".cif")]:
			list_cif_files.append(os.path.join(dirpath, filename))
	#print(list_cif_files)
	#print(list_cif_files[0])

	#logs the found cif.files at given directory Entry3.get()--------
	handle_log_files = open(f"{Entry3.get()}/files.log", "w", encoding="utf-8")
	for file in list_cif_files:
		handle_log_files.write(file + "\n")
	handle_log_files.close()

	#opens error.log-file at given directory Entry4.get() to write down empty or "?" values in .cif-file; see line ~147
	handle_log_errors = open(f"{Entry4.get()}/errors.log", "w", encoding="utf-8")

	for file in list_cif_files:
		dic_cif_table = {
			"_chemical_formula_sum": "",
			"_chemical_formula_weight": "",
			#"_exptl_crystal_size_max/_mid/_min":
			"_exptl_crystal_size_max": "",
			"_exptl_crystal_size_mid": "",
			"_exptl_crystal_size_min": "",
			#---
			"_space_group_crystal_system": "",
			"_space_group_name_H-M_alt": "",
			"_cell_length_a": "",
			"_cell_length_b": "",
			"_cell_length_c": "",
			"_cell_angle_alpha": "",
			"_cell_angle_beta": "",
			"_cell_angle_gamma": "",
			"_cell_volume": "",
			"_cell_formula_units_Z": "",
			"_exptl_crystal_density_diffrn": "",
			"_exptl_absorpt_coefficient_mu": "",
			"_exptl_crystal_F_000": "",
			"_diffrn_ambient_temperature": "",
			"_diffrn_measurement_device_type": "",
			"_diffrn_radiation_type": "",
			#"_diffrn_radiation_wavelength": "",#Achtung zusätzliche Spalte im vgl zu Denis
			#_diffrn_reflns_theta_min < _max
			"_diffrn_reflns_theta_max": "",
			"_diffrn_reflns_theta_min": "",
			#---
			#_diffrn_reflns_limit_h_min_/max
			"_diffrn_reflns_limit_h_max": "",
			"_diffrn_reflns_limit_h_min": "",
			#---
			#_diffrn_reflns_limit_k_min_/max
			"_diffrn_reflns_limit_k_max": "",
			"_diffrn_reflns_limit_k_min": "",
			#---
			#_diffrn_reflns_limit_l_min_/max
			"_diffrn_reflns_limit_l_max": "",
			"_diffrn_reflns_limit_l_min": "",
			#---
			"_diffrn_reflns_number": "",
			"_reflns_number_total": "",
			"_diffrn_reflns_point_group_measured_fraction_max": "",
			#_exptl_absorpt_correction_T_max/_min
			"_exptl_absorpt_correction_T_max": "",
			"_exptl_absorpt_correction_T_min": "",
			#---
			"_diffrn_reflns_av_R_equivalents": "",
			"_diffrn_reflns_av_unetI/netI": "",#Rsigma
			#_refine_ls_number_reflns/_restraints/_parameters
			"_refine_ls_number_reflns": "",
			"_refine_ls_number_restraints": "",
			"_refine_ls_number_parameters": "",
			#---
			"_refine_ls_restrained_S_all": "",
			"_refine_ls_R_factor_gt": "",
			"_refine_ls_wR_factor_gt": "",
			"_refine_ls_R_factor_all": "",
			"_refine_ls_wR_factor_ref": "",
			}
		list_keys = dic_cif_table.keys()
		
		#read the lines of current cif-file into a list
		handle_cif_file = open(file, "r", encoding="utf-8")
		list_file_lines = handle_cif_file.readlines()
		handle_cif_file.close()
		
		#checks every line in list for all of the keys from the dictionary. If key is in line,which is a string, (so return is NOT -1): Strip everything in line, including the key -> only value is left. Assign it into dictionary
		for line in  list_file_lines:
			for key in list_keys:
				if line.find(key) != -1:
					if key == "_diffrn_measurement_device_type":
						dic_cif_table[key] = line.strip("\n").strip("\t").strip(key).strip()
					else:
						dic_cif_table[key] = line.strip("\n").strip("\t").strip(key).replace(" ","")
					#print(key)

		#after dictionary SHOULD be full. Check the whole dictionary; if a value is empty or "?": log the key and value. start = True tells code, that it should log the filename at the beginn
		start = True #needed to check, if its the first error to note down. if yes then write file-name above.
		for key in list_keys:
			if (dic_cif_table[key] == "") or (dic_cif_table[key] == "?") or (dic_cif_table[key] == " ") or (dic_cif_table[key] == "\n"):
				if start == True:
					handle_log_errors.write(f"{file}\n")
					handle_log_errors.write(f"{key} = {dic_cif_table[key]}\n")
					start = False
				else:
					handle_log_errors.write(f"{key} = {dic_cif_table[key]}\n")
		if start == False:                
			handle_log_errors.write("\n")#carriage return after the dictionary was checked completely -> so after every file, where an error was found!   
		start = True 

		#print(dic_cif_table)

		#WriteOutputTables-------------------------------------------------------------------------------------------------------------------------------------------------
		#checks if the output table-files will be stored in same or different dir as cif.files, depending on output_radiobuttons.get() == 1 or ==2
		if output_radiobuttons.get() == 1:
			filename = file.strip(".cif")
			handle_write_table = open(f"{filename}_cifTable.txt", "w", encoding="utf-8")
		elif output_radiobuttons.get() == 2:
			file_replaced = file.replace("/", "\\")
			tuble_filesplit=file_replaced.rpartition("\\")
			filename = str(tuble_filesplit[2]).strip(".cif")
			if path.exists(f"{Entry2.get()}/{filename}_cifTable.txt") == True: #checks if file is already existing. If so, put a _count behind it. count = 1 at start.
				filename = f"{filename}_{count}"
				#count = count + 1 #count will be set up by one after the cifValue.txt is written! not here yet!
			handle_write_table = open(f"{Entry2.get()}/{filename}_cifTable.txt", "w", encoding="utf-8")
		#write down dictionary in file in table form. Some values will be wrote together, so there are some If-statements.
		for key in list_keys:
			if key == "_space_group_name_H-M_alt":
				handle_write_table.write(f"{key}".ljust(70) + f"{dic_cif_table[key]}\n".replace("'", ""))
				handle_write_table.write("_unit_cell_dimensions\n")
			#_exptl_crystal_size_max/_mid/_min-------
			elif key == "_exptl_crystal_size_max":
				handle_write_table.write("_exptl_crystal_size_max/_mid/_min".ljust(70) + f"{dic_cif_table['_exptl_crystal_size_max']} x {dic_cif_table['_exptl_crystal_size_mid']} x {dic_cif_table['_exptl_crystal_size_min']}\n")
			elif key == "_exptl_crystal_size_mid":
				continue
			elif key == "_exptl_crystal_size_min":
				continue
			#----------------------------------------
			#get the molyb alpha string--------------
			elif key == "_diffrn_radiation_type":
				molyb = dic_cif_table[key].find("Mo")
				if molyb == -1:
					handle_write_table.write(f"{key}".ljust(70) + f"{dic_cif_table[key]}\n".replace("'", ""))
				else:
					handle_write_table.write("_diffrn_radiation_type".ljust(70) + "Mo-Kα\n")
			#----------------------------------------
			#_diffrn_reflns_theta_min<_max---------
			elif key == "_diffrn_reflns_theta_max":
				handle_write_table.write("_diffrn_reflns_theta_min<_max".ljust(70) + f"{dic_cif_table['_diffrn_reflns_theta_min']} < θ < {dic_cif_table['_diffrn_reflns_theta_max']}\n")
			elif key == "_diffrn_reflns_theta_min":
				continue
			#----------------------------------------
			#_diffrn_reflns_limit_h_min_/max---------
			elif key == "_diffrn_reflns_limit_h_max":
				handle_write_table.write("_diffrn_reflns_limit_h_min_/max".ljust(70) + f"{dic_cif_table['_diffrn_reflns_limit_h_min']} < h < {dic_cif_table['_diffrn_reflns_limit_h_max']}\n")
			elif key == "_diffrn_reflns_limit_h_min":
				continue
			#----------------------------------------
			#_diffrn_reflns_limit_k_min_/max---------
			elif key == "_diffrn_reflns_limit_k_max":
				handle_write_table.write("_diffrn_reflns_limit_k_min_/max".ljust(70) + f"{dic_cif_table['_diffrn_reflns_limit_k_min']} < k < {dic_cif_table['_diffrn_reflns_limit_k_max']}\n")
			elif key == "_diffrn_reflns_limit_k_min":
				continue
			#----------------------------------------
			#_diffrn_reflns_limit_l_min_/max---------
			elif key == "_diffrn_reflns_limit_l_max":
				handle_write_table.write("_diffrn_reflns_limit_l_min_/max".ljust(70) + f"{dic_cif_table['_diffrn_reflns_limit_l_min']} < l < {dic_cif_table['_diffrn_reflns_limit_l_max']}\n")
			elif key == "_diffrn_reflns_limit_l_min":
				continue
			#----------------------------------------
			#_exptl_absorpt_correction_T_max/_min----
			elif key == "_exptl_absorpt_correction_T_max":
				handle_write_table.write("_exptl_absorpt_correction_T_max/_min".ljust(70) + f"{dic_cif_table['_exptl_absorpt_correction_T_max']} and {dic_cif_table['_exptl_absorpt_correction_T_min']}\n")
			elif key == "_exptl_absorpt_correction_T_min":
				continue
			#----------------------------------------
			#_refine_ls_number_reflns/_restraints/_parameters---
			elif key == "_refine_ls_number_reflns":
				handle_write_table.write("_refine_ls_number_reflns/_restraints/_parameters".ljust(70) + f"{dic_cif_table['_refine_ls_number_reflns']} / {dic_cif_table['_refine_ls_number_restraints']} / {dic_cif_table['_refine_ls_number_parameters']}\n")
			elif key == "_refine_ls_number_restraints":
				continue
			elif key == "_refine_ls_number_parameters":
				continue
			#----------------------------------------------------
			else:
				handle_write_table.write(f"{key}".ljust(70) + f"{dic_cif_table[key]}\n".replace("'", ""))
		handle_write_table.close()
		#-------------------------------------------------------------------------------------------------------------------------------------------------

		##riteOutputValues-------------------------------------------------------------------------------------------------------------------------------------------------
		#checks if the output value-files will be stored in same or different dir as cif.files, depending on output_radiobuttons.get() == 1 or ==2
		if output_radiobuttons.get() == 1:
			filename = file.strip(".cif")
			handle_write_values = open(f"{filename}_cifValues.txt", "w", encoding="utf-8")
		elif output_radiobuttons.get() == 2:
			file_replaced = file.replace("/", "\\")
			tuble_filesplit=file_replaced.rpartition("\\")
			filename = str(tuble_filesplit[2]).strip(".cif")
			#if path.exists(f"{Entry2.get()}/{filename}_cifValue.txt") == True: #checks if file is already existing. If so, put a _count behind it. count = 1 at start.
			#	filename = f"{filename}_{count}"
			#	count = count + 1
			handle_write_values = open(f"{Entry2.get()}/{filename}_cifValues.txt", "w", encoding="utf-8")
		#write down dictionary in file but only values! Some values will be wrote together, so there are some If-statements.
		for key in list_keys:
			if key == "_space_group_name_H-M_alt":
				handle_write_values.write(f"{dic_cif_table[key]}\n".replace("'", ""))
				handle_write_values.write("\n")
			#_exptl_crystal_size_max/_mid/_min-------
			elif key == "_exptl_crystal_size_max":
				handle_write_values.write(f"{dic_cif_table['_exptl_crystal_size_max']} x {dic_cif_table['_exptl_crystal_size_mid']} x {dic_cif_table['_exptl_crystal_size_min']}\n")
			elif key == "_exptl_crystal_size_mid":
				continue
			elif key == "_exptl_crystal_size_min":
				continue
			#----------------------------------------
			#get the molyb alpha string--------------
			elif key == "_diffrn_radiation_type":
				molyb = dic_cif_table[key].find("Mo")
				if molyb == -1:
					handle_write_values.write(f"{dic_cif_table[key]}\n".replace("'", ""))
				else:
					handle_write_values.write("Mo-Kα\n")
			#----------------------------------------
			#_diffrn_reflns_theta_min<_max---------
			elif key == "_diffrn_reflns_theta_max":
				handle_write_values.write(f"{dic_cif_table['_diffrn_reflns_theta_min']} < θ < {dic_cif_table['_diffrn_reflns_theta_max']}\n")
			elif key == "_diffrn_reflns_theta_min":
				continue
			#----------------------------------------
			#_diffrn_reflns_limit_h_min_/max---------
			elif key == "_diffrn_reflns_limit_h_max":
				handle_write_values.write(f"{dic_cif_table['_diffrn_reflns_limit_h_min']} < h < {dic_cif_table['_diffrn_reflns_limit_h_max']}\n")
			elif key == "_diffrn_reflns_limit_h_min":
				continue
			#----------------------------------------
			#_diffrn_reflns_limit_k_min_/max---------
			elif key == "_diffrn_reflns_limit_k_max":
				handle_write_values.write(f"{dic_cif_table['_diffrn_reflns_limit_k_min']} < k < {dic_cif_table['_diffrn_reflns_limit_k_max']}\n")
			elif key == "_diffrn_reflns_limit_k_min":
				continue
			#----------------------------------------
			#_diffrn_reflns_limit_l_min_/max---------
			elif key == "_diffrn_reflns_limit_l_max":
				handle_write_values.write(f"{dic_cif_table['_diffrn_reflns_limit_l_min']} < l < {dic_cif_table['_diffrn_reflns_limit_l_max']}\n")
			elif key == "_diffrn_reflns_limit_l_min":
				continue
			#----------------------------------------
			#_exptl_absorpt_correction_T_max/_min----
			elif key == "_exptl_absorpt_correction_T_max":
				handle_write_values.write(f"{dic_cif_table['_exptl_absorpt_correction_T_max']} and {dic_cif_table['_exptl_absorpt_correction_T_min']}\n")
			elif key == "_exptl_absorpt_correction_T_min":
				continue
			#----------------------------------------
			#_refine_ls_number_reflns/_restraints/_parameters---
			elif key == "_refine_ls_number_reflns":
				handle_write_values.write(f"{dic_cif_table['_refine_ls_number_reflns']} / {dic_cif_table['_refine_ls_number_restraints']} / {dic_cif_table['_refine_ls_number_parameters']}\n")
			elif key == "_refine_ls_number_restraints":
				continue
			elif key == "_refine_ls_number_parameters":
				continue
			#----------------------------------------------------
			else:
				handle_write_values.write(f"{dic_cif_table[key]}\n".replace("'", ""))
		handle_write_values.close()
		#-------------------------------------------------------------------------------------------------------------------------------------------------
				
	handle_log_errors.close()
	exit()
	#print(dic_cif_table)

def activate_Radiobuttons():
	if output_radiobuttons.get() == 1: 
		Entry2.configure(state=tk.DISABLED)	
		Button2.configure(state=tk.DISABLED)	
	elif output_radiobuttons.get() == 2:
		Entry2.configure(state=tk.NORMAL)
		Button2.configure(state=tk.ACTIVE)
		
class Toplevel1:
	"""Class creates the main GUI window of the Script.
	Global objects:

	-Entry1 (=cif-files directory)
	-Entry2 (=output-files directory)
	-Entry3 (=log-file directory)
	-Entry4 (=error-file directory)
	---One can read Entries by e.g. $string = Entry1.read()---
	---One can write in Entries by e.g. Entry2.insert(0, $string)---

	-output_radiobuttons
	---output_radiobuttons.get() =1 for Radiobutton1 active ; =2 for Radiobutton2 active---

	-Button2
	---Button2 is ENABLED and DISABLED by def activate_Radiobuttons()---
	"""
	def __init__(self, top):
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'

		#ttk style for Buttons 1-4
		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use("winnative")#('winnative')
		
		self.top = top
		self.top.geometry("596x491+776+285")
		self.top.minsize(120, 1)
		self.top.maxsize(3844, 1181)
		self.top.resizable(0,  0)
		self.top.title("JulezxXx: cif - Converter")
		self.top.configure(background="#1cb7e3")
		
		self.Frame1 = tk.Frame(top)
		self.Frame1.place(x=20, y=20, height=195, width=555)
		self.Frame1.configure(relief='groove')
		self.Frame1.configure(borderwidth="2")
		self.Frame1.configure(relief="groove")
		self.Frame1.configure(background="#1cb7e3")
		self.Frame1.configure(highlightbackground="#f0f0f0f0f0f0")
		self.Frame1.configure(highlightcolor="#646464646464")
		
		self.Label1 = tk.Label(self.Frame1)
		self.Label1.place(x=10, y=10, height=26, width=349)
		self.Label1.configure(anchor='w')
		self.Label1.configure(background="#1cb7e3")
		self.Label1.configure(disabledforeground="#a3a3a3")
		self.Label1.configure(font="-family {Segoe UI} -size 11 -weight bold")
		self.Label1.configure(foreground="#000000")
		self.Label1.configure(text='''Choose the directory to search for your cif-files:''')
		
		global Entry1
		Entry1 = tk.Entry(self.Frame1)
		Entry1.place(x=10, y=40, height=22, width=424)
		Entry1.configure(background="white")
		Entry1.configure(disabledforeground="#a3a3a3")
		Entry1.configure(font="TkFixedFont")
		Entry1.configure(foreground="#000000")
		Entry1.configure(insertbackground="black")
		
		self.Button1 = ttk.Button(self.Frame1)
		self.Button1.place(x=460, y=39, height=24, width=67)
		self.Button1.configure(text='''Load...''')
		self.Button1.configure(command=activate_Button1)
		
		global output_radiobuttons
		output_radiobuttons = tk.IntVar()
		self.Radiobutton1 = tk.Radiobutton(self.Frame1, value=1, variable=output_radiobuttons)
		self.Radiobutton1.place(relx=0.018, rely=0.462, relheight=0.159, relwidth=0.647)
		self.Radiobutton1.configure(activebackground="#1cb7e3")
		self.Radiobutton1.configure(activeforeground="#000000")
		self.Radiobutton1.configure(background="#1cb7e3")
		self.Radiobutton1.configure(disabledforeground="#a3a3a3")
		self.Radiobutton1.configure(font="-family {Segoe UI} -size 11")
		self.Radiobutton1.configure(foreground="#000000")
		self.Radiobutton1.configure(highlightbackground="#d9d9d9")
		self.Radiobutton1.configure(highlightcolor="black")
		self.Radiobutton1.configure(justify='left')
		self.Radiobutton1.configure(text='''Save created files in the same directory as cif-files''')	
		self.Radiobutton1.select()
		self.Radiobutton1.configure(command=activate_Radiobuttons)
		
		self.Radiobutton2 = tk.Radiobutton(self.Frame1, value=2, variable=output_radiobuttons)
		self.Radiobutton2.place(relx=0.011, rely=0.615, relheight=0.159, relwidth=0.555)
		self.Radiobutton2.configure(activebackground="#1cb7e3")
		self.Radiobutton2.configure(activeforeground="#000000")
		self.Radiobutton2.configure(background="#1cb7e3")
		self.Radiobutton2.configure(disabledforeground="#a3a3a3")
		self.Radiobutton2.configure(font="-family {Segoe UI} -size 11")
		self.Radiobutton2.configure(foreground="#000000")
		self.Radiobutton2.configure(highlightbackground="#d9d9d9")
		self.Radiobutton2.configure(highlightcolor="black")
		self.Radiobutton2.configure(justify='left')
		self.Radiobutton2.configure(text='''Save all created files in a given directory:''')
		self.Radiobutton2.configure(command=activate_Radiobuttons)

		global Entry2
		Entry2 = tk.Entry(self.Frame1)
		Entry2.place(x=10, y=150, height=22, width=424)
		Entry2.configure(background="white")
		Entry2.configure(disabledbackground="#9b9b9b")
		Entry2.configure(disabledforeground="#a3a3a3")
		Entry2.configure(font="TkFixedFont")
		Entry2.configure(foreground="#000000")
		Entry2.configure(highlightbackground="#d9d9d9")
		Entry2.configure(highlightcolor="black")
		Entry2.configure(insertbackground="black")
		Entry2.configure(selectbackground="blue")
		Entry2.configure(selectforeground="white")
		Entry2.configure(state=tk.DISABLED)	
		
		global Button2
		Button2 = ttk.Button(self.Frame1)
		Button2.place(x=460, y=149, height=24, width=67)
		Button2.configure(text='''Load...''')
		Button2.configure(command=activate_Button2)
		Button2.configure(state=tk.DISABLED)
		
		self.Frame2 = tk.Frame(top)
		self.Frame2.place(x=20, y=240, height=162, width=555)
		self.Frame2.configure(relief='groove')
		self.Frame2.configure(borderwidth="2")
		self.Frame2.configure(relief="groove")
		self.Frame2.configure(background="#1cb7e3")
		
		self.Label1_1 = tk.Label(self.Frame2)
		self.Label1_1.place(x=10, y=10, height=26, width=309)
		self.Label1_1.configure(activebackground="#f9f9f9")
		self.Label1_1.configure(activeforeground="black")
		self.Label1_1.configure(anchor='w')
		self.Label1_1.configure(background="#1cb7e3")
		self.Label1_1.configure(disabledforeground="#a3a3a3")
		self.Label1_1.configure(font="-family {Segoe UI} -size 11 -weight bold")
		self.Label1_1.configure(foreground="#000000")
		self.Label1_1.configure(highlightbackground="#d9d9d9")
		self.Label1_1.configure(highlightcolor="black")
		self.Label1_1.configure(text='''Choose the directory to save your file.log:''')
		
		global Entry3
		Entry3 = tk.Entry(self.Frame2)
		Entry3.place(x=10, y=40, height=22, width=424)
		Entry3.configure(background="white")
		Entry3.configure(disabledforeground="#a3a3a3")
		Entry3.configure(font="TkFixedFont")
		Entry3.configure(foreground="#000000")
		Entry3.configure(highlightbackground="#d9d9d9")
		Entry3.configure(highlightcolor="black")
		Entry3.configure(insertbackground="black")
		Entry3.configure(selectbackground="blue")
		Entry3.configure(selectforeground="white")
		Entry3.insert(0, os.getcwd())
		
		self.Button3 = ttk.Button(self.Frame2)
		self.Button3.place(x=460, y=39, height=24, width=67)
		self.Button3.configure(text='''Load...''')
		self.Button3.configure(command=activate_Button3)
		
		self.Label1_1_1 = tk.Label(self.Frame2)
		self.Label1_1_1.place(x=10, y=90, height=26, width=309)
		self.Label1_1_1.configure(activebackground="#f9f9f9")
		self.Label1_1_1.configure(activeforeground="black")
		self.Label1_1_1.configure(anchor='w')
		self.Label1_1_1.configure(background="#1cb7e3")
		self.Label1_1_1.configure(disabledforeground="#a3a3a3")
		self.Label1_1_1.configure(font="-family {Segoe UI} -size 11 -weight bold")
		self.Label1_1_1.configure(foreground="#000000")
		self.Label1_1_1.configure(highlightbackground="#d9d9d9")
		self.Label1_1_1.configure(highlightcolor="black")
		self.Label1_1_1.configure(text='''Choose the directory to save your error.log:''')
		
		global Entry4
		Entry4 = tk.Entry(self.Frame2)
		Entry4.place(x=10, y=120, height=22, width=424)
		Entry4.configure(background="white")
		Entry4.configure(disabledforeground="#a3a3a3")
		Entry4.configure(font="TkFixedFont")
		Entry4.configure(foreground="#000000")
		Entry4.configure(highlightbackground="#d9d9d9")
		Entry4.configure(highlightcolor="black")
		Entry4.configure(insertbackground="black")
		Entry4.configure(selectbackground="blue")
		Entry4.configure(selectforeground="white")
		Entry4.insert(0, os.getcwd())
		
		self.Button4 = ttk.Button(self.Frame2)
		self.Button4.place(x=460, y=119, height=24, width=67)
		self.Button4.configure(text='''Load...''')
		self.Button4.configure(command=activate_Button4)
		
		self.Button5 = tk.Button(top)
		self.Button5.place(x=250, y=430, height=34, width=97)
		self.Button5.configure(activebackground="#ececec")
		self.Button5.configure(activeforeground="#000000")
		self.Button5.configure(background="#d9d9d9")
		self.Button5.configure(disabledforeground="#a3a3a3")
		self.Button5.configure(font="-family {Segoe UI} -size 11 -weight bold")
		self.Button5.configure(foreground="#000000")
		self.Button5.configure(highlightbackground="#d9d9d9")
		self.Button5.configure(highlightcolor="black")
		self.Button5.configure(pady="0")
		self.Button5.configure(text='''Convert''')
		self.Button5.configure(command=activate_Button5)

if __name__ == '__main__':
	vp_start_gui()
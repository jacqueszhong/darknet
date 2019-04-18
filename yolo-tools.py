# coding : utf-8
# Author : Jacques Zhong
# Date : 14/03/2019

import os,sys,glob
import argparse
import cv2

#Define some paths
cur_dir =os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(cur_dir, "target_dir") #Directory where all files are generated (to avoid accidently deleting data)

#Basic tools
def shuffle_txt(txt_path):
	"""
		Shuffling lines in txt file.
	"""
	print("Shuffling : {}".format(txt_path))
	os.system('shuf '+txt_path+' -o '+txt_path)

def read_yolo_bbox(file) :
	"""
	correct yolo bbox file checking might be needed
	"""
	res = []
	f = open(file, 'r')
	for line in f:
		s = line.rstrip().split(" ")
		res.append(s)
	f.close()
	return res

#Commands
def append_img_path(img_dir, trainfile, testfile, percentage_test=0.2):
	"""
		Splits database and writes the path of the images from 'img_dir' into 'trainfile' and 'testfile'.
	"""

	# Create and/or truncate train.txt and test.txt
	file_train = open(trainfile, 'a')
	file_test = open(testfile, 'a')

	# Populate train.txt and test.txt
	counter = 1
	if not percentage_test :
		index_test = -1
	else :
		index_test = round(1 / percentage_test)
	for pathAndFilename in glob.iglob(os.path.join(img_dir, "*.jpg")):
	    title, ext = os.path.splitext(os.path.basename(pathAndFilename)) 	

	    if counter == index_test:
	        counter = 1
	        file_test.write(os.path.join(img_dir, title + '.jpg') + "\n")
	    else:
	        file_train.write(os.path.join(img_dir, title + '.jpg') + "\n")
	        counter = counter + 1

	file_train.close()
	file_test.close()

def process_subsets(in_dirs, output_dir, ptest=0.2,recursive=False):
	"""
		Outputs train.txt and test.txt files with shuffling.
	"""
	train = os.path.join(output_dir,'train.txt')
	test = os.path.join(output_dir,'test.txt')

	#Add paths to txt files
	for i,d in enumerate(in_dirs):
		if os.path.isdir(d):
		
			#Process current dir	
			abs_dir = os.path.join(cur_dir,d)
			print("Found dir : {}".format(abs_dir))
			append_img_path(abs_dir,train,test,ptest)

			#Process subdirs
			if recursive :
				print("recursive")
				for root,dirs,files in os.walk(d): #Parcours des dossiers
					for subd in dirs :
						abs_dir = os.path.join(cur_dir,root,subd)
						print("Found dir : {}".format(abs_dir))
						append_img_path(abs_dir,train,test,ptest)
	
	#Shuffle outputs
	shuffle_txt(train)
	shuffle_txt(test)

def empty_labels(input_dir):
	"""
		Creates empty .txt for all .jpg files in directory 'in_dir'.
	"""

	filenames = os.listdir(input_dir)
	for n in filenames :
		s, ext = os.path.splitext(n)
		if ext == '.jpg' :
			spath = os.path.join(out_dir,s+".txt")
			print(spath)
			f = open(spath,'w')
			f.close()

def change_labels(input_dir,init_label,final_label,output_dir=out_dir,replace=False,verbose=False):
	"""
		Changes the class labels of all bounding boxes annotations contained in .txt files of directory 'in_dir'.
	"""

	#Force la comparaison sur les chaines de caracteres
	init_label = str(init_label)
	final_label = str(final_label)

	filenames = os.listdir(input_dir)
	for filename in filenames: 

		#Read only .txt
		s, ext = os.path.splitext(filename)
		if ext == '.txt' :

			#Read bboxes
			res = read_yolo_bbox(os.path.join(input_dir,filename))
			if verbose :
				print("initial : "+str(res))


			#Change bboxes class
			for r in res:
				if r[0] == init_label:
					r[0] = final_label
			if verbose :
				print("final : "+str(res))

			#Write bboxes
			if replace :
				f = open(os.path.join(input_dir,filename), 'w') 
			else :
				f = open(os.path.join(output_dir,filename), 'w')
	
			for r in res :
				f.write(" ".join(r)+"\n")
			f.close()

def change_labels_rec(input_dir,init_label,final_label,output_dir=out_dir,replace=False,verbose=False):
	if not replace :
		print("!Might be replicated files accross folders.!")
	change_labels(input_dir,init_label,final_label,output_dir,replace,verbose)
	for root,dirs,files in os.walk(input_dir):
		for d in dirs:
			print("Found {}".format(d))
			change_labels(os.path.join(root,d),init_label,final_label,output_dir,replace,verbose)


def swap_labels(input_dir,label_1, label_2,output_dir=out_dir,replace=False,verbose=False):
	"""
		Swap classes of all bounding boxes annotations contained in .txt files of directory 'in_dir'.
	"""

	label_1 = str(label_1)
	label_2 = str(label_2)

	filenames = os.listdir(input_dir)
	for filename in filenames:

		#Read only .txt
		s, ext = os.path.splitext(filename)
		if ext == '.txt' :

			#Read bboxes
			res = read_yolo_bbox(os.path.join(input_dir,filename))
			if verbose:
				print("initial : "+str(res))

			#Change bboxes class
			for r in res:
				if r[0] == label_1:
					r[0] = label_2
				elif r[0] == label_2:
					r[0] = label_1
			if verbose:
				print("final : "+str(res))

			#Write bboxes
			if replace :
				f = open(os.path.join(input_dir,filename), 'w') 
			else :
				f = open(os.path.join(output_dir,filename), 'w')
	
			for r in res :
				f.write(" ".join(r)+"\n")
			f.close()

def swap_labels_rec(input_dir,label_1, label_2,output_dir=out_dir,replace=False,verbose=False):
	if not replace :
		print("!Might be replicated files accross folders.!")
	swap_labels(input_dir,label_1, label_2,output_dir,replace,verbose)
	for root,dirs,files in os.walk(input_dir):
		for d in dirs:
			swap_labels(os.path.join(root,d),label_1, label_2,output_dir,replace,verbose)



def delete_labels(input_dir,label,output_dir=out_dir,replace=False,verbose=False):
	"""
		Deletes annotations with class 'label' in directory 'in_dir'.
	"""

	label=str(label)
	filenames = os.listdir(input_dir)
	for filename in filenames: 

		#Read only .txt
		s, ext = os.path.splitext(filename)
		if ext == '.txt' :

			#Read bboxes
			res = read_yolo_bbox(os.path.join(input_dir,filename))

			#Change bboxes class
			i = 0
			while (i < len(res)):
				if res[i][0] == label :
					if verbose:
						print("Deleted : {},{} in {}".format(i,res[i], filename))
					del res[i]
				else :
					i=i+1

			#Write bboxes
			if replace :
				f = open(os.path.join(input_dir,filename), 'w') 
			else :
				f = open(os.path.join(output_dir,filename), 'w')
	
			for r in res :
				f.write(" ".join(r)+"\n")
			f.close()

def delete_labels_rec(input_dir,label,output_dir=out_dir,replace=False,verbose=False):
	if not replace :
		print("!Might be replicated files accross folders.!")
	delete_labels(input_dir,label,output_dir,replace,verbose)
	for root,dirs,files in os.walk(input_dir):
		for d in dirs:
			delete_labels(os.path.join(root,d),label,output_dir,replace,verbose)

def count_labels(in_dir, n = 80):
	print("Counting labels in {} up to {}".format(in_dir,n))

	counts = [0] * int(n)

	for root,dirs,files in os.walk(in_dir):

		for filename in files :
			#Read only .txt (bbox)
			s, ext = os.path.splitext(filename)
			if ext == '.txt' :
				lines = read_yolo_bbox(os.path.join(root,filename))	 

				for l in lines :
					index = int(l[0])
					if index < n :
						counts[index] = counts[index] + 1

	for i, c in enumerate(counts) :
		if c :
			print("Class {} has {} occurence(s).".format(i,c))

def print_help():
	print("Available commands : ")
	print("\t process_subsets")
	print("\t change_labels")
	print("\t count_labels")
	print("\t empty_labels")
	print("\t swap_labels")	
	print("\t delete_labels")

def image_resize(in_dir, width, height):
	"""
		Resize all images in directory 'in_dir' to size ('width', 'height').
	"""
	print("not now")

def check_bbox(bbox_path):
	"""
		Check bounding box txt files and print found errors. Return 1 if no errors.
	"""
	bboxes = read_yolo_bbox(bbox_path)
	err_flag = 1

	for bbox in bboxes:
		try:
			v=int(bbox[0])
		except ValueError:
			print("\tError in {} : invalid class label {}.".format(bbox_path,bbox[0]))
			err_flag = 0

		if len(bbox[1:]) != 4:
			print("\tError in {} : number of coordinates should be 4 but got {}.".format(bbox_path,bbox[1:]))
			err_flag = 0

		for i,coord in enumerate(bbox[1:]):
			try:
				v = float(coord)
			except ValueError:
				print("\tError in {} : invalid coordinate {} at index {}.".format(bbox_path,coord,i))
				err_flag = 0

	return err_flag


def check_jpg(jpg_path):
	img = cv2.imread(jpg_path)
	try :
		if img.size != 0:
			return 1

		else :
			return 0
	except :
		print("\tError in {} : bad jpg.".format(jpg_path))
		return 0

def check_data_integrity(input_dir):
	filenames=os.listdir(input_dir)
	print("Checking {}".format(input_dir))
	for filename in os.listdir(input_dir):
		s,ext = os.path.splitext(filename)
		if ext == '.jpg':
			#Check .jpg integrity
			check_jpg(os.path.join(input_dir,filename))

			#Check bbox .txt integrity
			try:
				check_bbox(os.path.join(input_dir,s+".txt"))
			except FileNotFoundError:
				print("\tError in {} : file not found.".format(os.path.join(input_dir,s+".txt")))

	print("Done")

def check_data_integrity_rec(input_dir):
	check_data_integrity(input_dir)
	for root,dirs,files in os.walk(input_dir):
		for d in dirs:
			check_data_integrity(os.path.join(root,d))


def remove_bad_img(input_dir):
	for filename in os.listdir(input_dir):
		s,ext = os.path.splitext(filename)
		if ext == '.jpg':
			fpath = os.path.join(input_dir,filename)
			if not check_jpg(fpath):
				os.remove(fpath)
				print("\tRemoved {}.".format(fpath))
	print("done.")


if __name__ == "__main__" :

	#Little command-line API for convenience

	#Shared optional arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-v","--verbose",action='store_true',help="maybe there's nothing more to say.")
	parser.add_argument("-r","--recursive",action='store_true',help="if possible, command recursively done on directories.")
	parser.add_argument("--replace",action='store_true',help="if set, overrides existing files.")
	parser.add_argument("-o","--output_dir",default=out_dir,help="custom output directory for processed files.")

	#Specific optional arguments (pas hyper prore)
	parser.add_argument("-p",type=float,default=0.2,help="proportion (for process_subsets).")	
	parser.add_argument("-n","--number_labels",type=int,default=80,help="max number of labels considered (for count_labels).")

	parser.add_argument("cmd_args",nargs='+')
	arg1 = parser.parse_args()

	#Positionnal arguments
	usrCmd = arg1.cmd_args[0]
	parser2 = argparse.ArgumentParser()

	if usrCmd == 'empty_labels':
		parser2.add_argument("input_dir")
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		#empty_labels(arg2.input_dir,replace=arg1.replace,output_dir=arg1.output_dir,recursive=arg1.recursive)
		empty_labels(arg2.input_dir)

	elif usrCmd == 'change_labels':
		parser2.add_argument("input_dir")
		parser2.add_argument("init_label",type=int)
		parser2.add_argument("final_label",type=int)
		arg2 = parser2.parse_args(arg1.cmd_args[1:])

		print(arg1)
		print(arg2)
		if arg1.recursive:
			change_labels_rec(arg2.input_dir, arg2.init_label, arg2.final_label, replace=arg1.replace,output_dir=arg1.output_dir,verbose=arg1.verbose)
		else:
			change_labels(arg2.input_dir, arg2.init_label, arg2.final_label, replace=arg1.replace,output_dir=arg1.output_dir,verbose=arg1.verbose)

	elif usrCmd == 'swap_labels':
		parser2.add_argument("input_dir")
		parser2.add_argument("label1",type=int)
		parser2.add_argument("label2",type=int)
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		if arg1.recursive:
			swap_labels_rec(arg2.input_dir, arg2.label1, arg2.label2, replace=arg1.replace,output_dir=arg1.output_dir,verbose=arg1.verbose)
		else:
			swap_labels(arg2.input_dir, arg2.label1, arg2.label2, replace=arg1.replace,output_dir=arg1.output_dir,verbose=arg1.verbose)

	elif usrCmd == 'delete_labels' :
		parser2.add_argument("input_dir")
		parser2.add_argument("label",type=int)
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		if arg1.recursive:
			delete_labels_rec(arg2.input_dir,arg2.label)
		else:
			delete_labels(arg2.input_dir,arg2.label)
			

	elif usrCmd == 'process_subsets':
		parser2.add_argument("input_dirs",nargs='+')
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		process_subsets(arg2.input_dirs,output_dir=arg1.output_dir,ptest=arg1.p,recursive=arg1.recursive)

	elif usrCmd == 'count_labels':
		parser2.add_argument("input_dir")
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		count_labels(arg2.input_dir,n=arg1.number_labels)

	elif usrCmd == 'check_data':
		parser2.add_argument("input_dir")
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		if arg1.recursive:
			check_data_integrity_rec(arg2.input_dir)
		else:
			check_data_integrity(arg2.input_dir)


	elif usrCmd == 'rm_corrupt':
		parser2.add_argument("input_dir")
		arg2 = parser2.parse_args(arg1.cmd_args[1:])
		remove_bad_img(arg2.input_dir)

	else:
		print_help()
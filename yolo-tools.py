# coding : utf-8

import os,sys,glob

flag_nocp = False #If true, replace .txt files, save your data before doing that !

#Define some paths
cur_dir =os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(cur_dir, "target_dir") #Directory where all files are generated (to avoid accidently deleting data)

def append_img_path(img_dir, trainfile, testfile, percentage_test=0.2):
	"""
		Splits database and writes the path of the images from 'img_dir' into 'trainfile' and 'testfile'.
	"""

	# Create and/or truncate train.txt and test.txt
	file_train = open(trainfile, 'a')
	file_test = open(testfile, 'a')

	# Populate train.txt and test.txt
	counter = 1
	index_test = round(1 / percentage_test)
	for pathAndFilename in glob.iglob(os.path.join(img_dir, "*.txt")):
	    title, ext = os.path.splitext(os.path.basename(pathAndFilename)) 	

	    if counter == index_test:
	        counter = 1
	        file_test.write(os.path.join(img_dir, title + '.jpg') + "\n")
	    else:
	        file_train.write(os.path.join(img_dir, title + '.jpg') + "\n")
	        counter = counter + 1

	file_train.close()
	file_test.close()


def shuffle_txt(txt_name):
	"""
		Shuffling lines in txt file.
	"""
	print("Shuffling : {}".format(txt_name))
	os.system('shuf '+txt_name+' -o '+txt_name)


def process_subsets(in_dirs, percentage_test=0.2):
	"""
		Outputs train.txt and test.txt files with shuffling.
	"""

	#Add paths to txt files
	for i,d in enumerate(in_dirs):
		if os.path.isdir(d):
			abs_dir = os.path.join(cur_dir,d)
			print("Found dir : {}".format(abs_dir))
			append_img_path(abs_dir,'train.txt','test.txt',percentage_test)


	#Shuffle outputs
	shuffle_txt('train.txt')
	shuffle_txt('test.txt')

def empty_labels(in_dir):
	"""
		Creates empty .txt for all .jpg files in directory 'in_dir'.
	"""

	filenames = os.listdir(in_dir)
	for n in filenames :
		s, ext = os.path.splitext(n)
		if ext == '.jpg' :
			spath = os.path.join(out_dir,s+".txt")
			print(spath)
			f = open(spath,'w')
			f.close()


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


def change_labels(in_dir,init_label,final_label):
	"""
		Changes the class labels of all bounding boxes annotations contained in .txt files of directory 'in_dir'.
	"""

	#for root, dirs, files in os.walk(in_dir):
	filenames = os.listdir(in_dir)

	for filename in filenames: 

		#Read only .txt
		s, ext = os.path.splitext(filename)
		if ext == '.txt' :

			#Read bboxes
			res = read_yolo_bbox(os.path.join(in_dir,filename))
			print("initial : "+str(res))


			#Change bboxes class
			for r in res:
				if r[0] == init_label:
					r[0] = final_label
			print("final : "+str(res))

			#Write bboxes
			if flag_nocp :
				f = open(os.path.join(in_dir,filename), 'w') 
			else :
				f = open(os.path.join(out_dir,filename), 'w')
	
			for r in res :
				f.write(" ".join(r)+"\n")
			f.close()

def swap_labels(in_dir,label_1, label_2):
	"""
		Swap classes of all bounding boxes annotations contained in .txt files of directory 'in_dir'.
	"""

	filenames = os.listdir(in_dir)
	for filename in filenames: 

		#Read only .txt
		s, ext = os.path.splitext(filename)
		if ext == '.txt' :

			#Read bboxes
			res = read_yolo_bbox(os.path.join(in_dir,filename))
			print("initial : "+str(res))

			#Change bboxes class
			for r in res:
				if r[0] == label_1:
					r[0] = label_2
				elif r[0] == label_2:
					r[0] = label_1
			print("final : "+str(res))

			#Write bboxes
			if flag_nocp :
				f = open(os.path.join(in_dir,filename), 'w') 
			else :
				f = open(os.path.join(out_dir,filename), 'w')
	
			for r in res :
				f.write(" ".join(r)+"\n")
			f.close()

def delete_labels(in_dir,label):
	"""
		Deletes annotations with class 'label' in directory 'in_dir'.
	"""
	filenames = os.listdir(in_dir)
	for filename in filenames: 

		#Read only .txt
		s, ext = os.path.splitext(filename)
		if ext == '.txt' :

			#Read bboxes
			res = read_yolo_bbox(os.path.join(in_dir,filename))

			#Change bboxes class
			i = 0
			while (i < len(res)):
				if res[i][0] == label :
					print("Deleted : {},{} in {}".format(i,res[i], filename))
					del res[i]
				else :
					i=i+1
			

			#Write bboxes
			if flag_nocp :
				f = open(os.path.join(in_dir,filename), 'w') 
			else :
				f = open(os.path.join(out_dir,filename), 'w')
	
			for r in res :
				f.write(" ".join(r)+"\n")
			f.close()


def count_labels(in_dir, n = 80):
	print("Counting labels in {} up to {}".format(in_dir,n))

	counts = [0] * int(n)

	#filenames = os.listdir(in_dir)
	#for filename in filenames :
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
	print("Arguments : ")
	print("\t process_subsets <dir>")
	print("\t empty_labels <dir>")
	print("\t change_labels <dir> <init_label> <final_label>")
	print("\t swap_labels <dir> <init_label> <final_label>")	
	print("\t delete_labels <dir> <label>")

def parse_args():
	print("eventuellement faire qqch de plus propre.")
	"""
	for a in sys.argv:
		print(a)
		if a == "-nocp":
			flag_nocp = True
	"""

def image_resize(in_dir, width, height):
	"""
		Resize all images in directory 'in_dir' to size ('width', 'height').
	"""
	print("not now")


if __name__ == "__main__" :


	if len(sys.argv) < 2 :
		print("Too few arguments")
		print_help()
		quit()


	usrCmd = sys.argv[1]
	if usrCmd == 'empty_labels' : 
		if len(sys.argv) != 3 :
			print_help()
		else :
			empty_labels(sys.argv[2])


	elif usrCmd == 'change_labels' :
		if len(sys.argv) != 5 :
			print_help()
		else :
			change_labels(sys.argv[2],sys.argv[3],sys.argv[4])

	elif usrCmd == 'swap_labels' :
		if len(sys.argv) != 5 :
			print_help()
		else :
			swap_labels(sys.argv[2],sys.argv[3],sys.argv[4])

	elif usrCmd == 'process_subsets' :
		if len(sys.argv) < 3 :
			print_help()
		else :
			process_subsets(sys.argv[2:])

	elif usrCmd == 'delete_labels' :
		if len(sys.argv) != 4 :
			print_help()
		else :
			delete_labels(sys.argv[2],sys.argv[3])

	elif usrCmd == 'count_labels' :
		if len(sys.argv) < 3 :
			print_help()
		elif len(sys.argv) == 3 :
			count_labels(sys.argv[2])
		else : 
			count_labels(sys.argv[2], n=int(sys.argv[3]))
			

	else:
		print("Invalid command")
		print_help()

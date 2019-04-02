#For fast process on EC2 server

EBS_DIR="/home/ubuntu/my_data"
DARKNET_DIR="/home/ubuntu/darknet"

cp $DARKNET_DIR/"yolo-tools.py" $EBS_DIR/"data_0104"
cd $EBS_DIR/"data_0104"


#DoorChair_freeze
python yolo-tools process_subsets transfer2/chair_00 transfer2/chair_01 transfer2/door_00 transfer2/door_01 transfer2/openimg
cat test.txt >> train.txt #Dont need to create another validation set here
mv *.txt $DARKNET_DIR/"cfg_DoorChair_freeze"

#DoorChair_80
python yolo-tools process_subsets transfer80/chair_00 transfer80/chair_01 transfer80/door_00 transfer80/door_01 transfer80/openimg
cat test.txt >> train.txt #Dont need to create another validation set here
mv *.txt $DARKNET_DIR/"cfg_DoorChair_80"
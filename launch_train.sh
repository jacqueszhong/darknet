
#DATA="cfg_SimpleDoorChair/obj.data"
#CONFIG="cfg_SimpleDoorChair/yolov3-tiny.cfg"


#DATA=cfg_DoorChair/obj.data
#CONFIG=cfg_DoorChair/yolov3-tiny_DoorChair.cfg

DATA=cfg_transfer80/obj.data
CONFIG=cfg_transfer80/yolov3-tiny.cfg


#WEIGHTS="backup/yolov3-tiny_last.weights"
#WEIGHTS="../yolov3-tiny.conv.15"
#WEIGHTS="../yolov2.weights"
#WEIGHTS="backup/yolov2_last.weights"
#WEIGHTS=../yolov3_long_test.weights
#WEIGHTS=backup/yolov3-tiny_DoorChair_last.weights
WEIGHTS=models/yolov3-tiny.weights


OPTIONS="-dont_show -mjpeg_port 8090 -map"

./darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

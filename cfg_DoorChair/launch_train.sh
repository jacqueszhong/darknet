#For fast launch on EC2 server


DATA=cfg_DoorChair/obj.data
CONFIG=cfg_DoorChair/yolov3-tiny_DoorChair.cfg
WEIGHTS=models/yolov3-tiny.conv.15

#OPTIONS="-dont_show -mjpeg_port 8090 -map"
OPTIONS = "-dont_show -gpus 0,1"

./darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

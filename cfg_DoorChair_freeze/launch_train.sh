#For fast launch on EC2 server


DATA=obj.data
CONFIG=yolov3-tiny_DoorChair_freeze.cfg
WEIGHTS=../models/yolov3-tiny.conv.15

#OPTIONS="-dont_show -mjpeg_port 8090 -map"
OPTIONS="-dont_show"

./../darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

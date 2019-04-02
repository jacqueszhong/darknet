#For fast launch on EC2 server


DATA=obj.data
CONFIG=yolov3-tiny_DoorChair_80.cfg
WEIGHTS=../models/yolov3-tiny.weights

#OPTIONS="-dont_show -mjpeg_port 8090 -map"
OPTIONS="-dont_show"

./../darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

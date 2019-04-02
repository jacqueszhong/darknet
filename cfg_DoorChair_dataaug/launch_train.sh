#For fast launch on EC2 server
CUR_DIR=`pwd`

DATA=$CUR_DIR/obj.data
CONFIG=$CUR_DIR/yolov3-tiny_DoorChair_dataaug.cfg
cd ..
WEIGHTS=models/yolov3-tiny.conv.15
OPTIONS="-dont_show"
#OPTIONS="-dont_show -mjpeg_port 8090 -map"

./darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

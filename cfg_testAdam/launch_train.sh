#For fast launch on EC2 server
CUR_DIR=`pwd`

DATA=$CUR_DIR/obj.data
CONFIG=$CUR_DIR/yolov3-tiny_testAdam.cfg
WEIGHTS=models/yolov3-tiny.conv.15
OPTIONS=" -map"

cd ..
./darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

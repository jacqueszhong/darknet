#For fast launch on EC2 server
CUR_DIR=`pwd`

DATA=$CUR_DIR/obj.data
CONFIG=$CUR_DIR/yolov3.cfg
cd ..
WEIGHTS=models/darknet53.conv.74
OPTIONS="-dont_show -map"
#OPTIONS=" -map"

./darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

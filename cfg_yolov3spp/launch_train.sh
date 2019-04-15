#Yolo model with the best mAP on COCO dataset
#For fast launch on EC2 server
CUR_DIR=`pwd`

DATA=$CUR_DIR/obj.data
CONFIG=$CUR_DIR/yolov3-spp.cfg
WEIGHTS=models/yolov3-spp.weights

#OPTIONS="-dont_show -mjpeg_port 8090 -map"
OPTIONS="-dont_show"

cd ..
./darknet detector train $DATA $CONFIG $WEIGHTS $OPTIONS

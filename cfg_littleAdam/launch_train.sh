#Launch in cfg directory
DATA=cfg_littleAdam/obj.data
CFG=cfg_littleAdam/yolov3-tiny.cfg
WEIGHTS=models/yolov3-tiny.conv.15
OPTIONS="-map"

cd ..
./darknet detector train $DATA $CFG $WEIGHTS $OPTIONS

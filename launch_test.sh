

#21/03
#Environ 500 itérations, avec base complète, transfert de tous les poids, chair=56 et door=0.
#./darknet detector demo cfg_transfer80/obj.data cfg_transfer80/yolov3-tiny.cfg models/2103_test_500it.weights -c 1


#27/03 : leger entrainement sur aws
./darknet detector demo cfg_transfer80/obj.data cfg_transfer80/yolov3-tiny.cfg models/back3.weights -c 1


#./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg ../WEIGHTS/yolov3-tiny.weights -c 1


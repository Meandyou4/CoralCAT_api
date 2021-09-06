# CoralCAT_API

1. Download tensorflow: https://codeload.github.com/tensorflow/tensorflow/zip/c565660e008cf666c582668cb0d0937ca86e71fb
2. For train, run: 
``` python examplesimage_retrainingretrain.py --bottleneck_dir=nn_filesbottlenecks --how_many_training_steps 500 --model_dir=nn_filesinception --output_graph=nn_filesretrained_graph.pb --output_labels=nn_filesretrained_labels.txt --image_dir nn_filesphotos
python tensorflow/tensorflow/examples/image_retraining/retrain.py --bottleneck_dir=nn_files/bottlenecks --how_many_training_steps 500 --model_dir=nn_files/inception --output_graph=nn_files/retrained_graph.pb --output_labels=nn_files/retrained_labels.txt --image_dir nn_files/photos ```

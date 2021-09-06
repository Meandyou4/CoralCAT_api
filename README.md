# CoralCAT_API

1. Download tensorflow: https://codeload.github.com/tensorflow/tensorflow/zip/c565660e008cf666c582668cb0d0937ca86e71fb
2. Download nn_files: https://drive.google.com/drive/folders/1XX-DtpuwCUL5sMBONaJ_tb7ClLUGCSzO?usp=sharing
3. For train, run: 
``` python examplesimage_retrainingretrain.py --bottleneck_dir=nn_filesbottlenecks --how_many_training_steps 500 --model_dir=nn_filesinception --output_graph=nn_filesretrained_graph.pb --output_labels=nn_filesretrained_labels.txt --image_dir nn_filesphotos
python tensorflow/tensorflow/examples/image_retraining/retrain.py --bottleneck_dir=nn_files/bottlenecks --how_many_training_steps 500 --model_dir=nn_files/inception --output_graph=nn_files/retrained_graph.pb --output_labels=nn_files/retrained_labels.txt --image_dir nn_files/photos ```



Output
```
{
    "first": "EXOTIC SHORTHAIR",
    "first_prediction_procent": "65.1%",
    "id_first": 20,
    "id_second": 28,
    "id_third": 35,
    "other_breeds": "6.7%",
    "second": "MUNCHKIN ",
    "second_prediction_procent": "26.4%",
    "third": "RAGAMUFFIN",
    "third_prediction_procent": " 1.8%"
}
```

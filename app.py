# Author: Sasa Lazic
# python app.py
import tensorflow as tf
import sys
import time
import os
import PIL
import piexif
import shutil
import random
import base64
import requests
import json
import glob
import pathlib
from  flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
from flask_restful import Resource, Api, reqparse
from io import BytesIO
from os import path


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
api = Api(app)

def rasa_unos(unos):
    file = open("./files/rasa.txt","a+") 
    rasa_macke=unos      
    # Reading from file
    file.write("\n")
    file.write(rasa_macke)
    file.close()

def rasa_citac():
    with open('./files/rasa.txt') as myfile:
        return(list(myfile)[-1])

def moveit(extension):
    list_of_files = glob.glob('*.'+extension)
    latest_file = max(list_of_files, key=os.path.getctime)
    #print(os.path.abspath(latest_file))

    source_path = os.path.abspath(latest_file)
    source=pathlib.Path(latest_file).parent.resolve()
    if path.exists(source_path):
        destination_path = "images"
        new_location = shutil.move(os.path.join(source, latest_file), os.path.join(destination_path, latest_file))
        #print(new_location)
        print("The %s is moved to the location, %s" %(source_path, new_location))
    else:
        print("File does not exist.")

def predict(input_image):
    print('File uploading...')
    # change this as you see fit
    image_path = input_image

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile("nn_files/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("nn_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        # print(str(top_k))
        number=0
        rez=0
        arr=[]
        print('*'*50)
        for node_id in top_k:
            if number!=2:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                arr.append('%s : %.1f' % (human_string.upper(), score*100)+ "%")
                # return jsonify(
                #     prediction=('%s : %.1f' % (human_string.upper(), score*100)+ "%")
                #     )
                number+=1
                rez=rez+score
            else:
                break
        #print(arr)
        size1 = len(arr[0])
        size2 = len(arr[1])
        size3 = len(arr[2])


        first=arr[0][:size1 - 8]
        second=arr[1][:size2 - 8]
        third=arr[2][:size3 - 8]

        with open('./files/labels.json') as f:
                data = json.load(f)

        name_by_id = dict([(str(p['id']), p['name']) for p in data])
        id_by_name = dict([(p['name'], p['id']) for p in data])

        moveit("jpg")
        return jsonify(
            id_first=id_by_name[first.lower()],
            first=first,
            first_prediction_procent=arr[0][-5:],
            id_second=id_by_name[second.lower()],
            second=arr[1][:size2 - 7],
            second_prediction_procent=arr[1][-5:],
            third=arr[2][:size3 - 7],
            id_third=id_by_name[third.lower()],
            third_prediction_procent=arr[2][-5:],
            other_breeds=format_other_breeds)

        rez=0
        #print('*'*50)

# while True:
#     sasa=input("Unesi path: ")
#     start = time.time()
#     print(predict(sasa))
#     end = time.time()
#     print("time: ",end - start)

#print(predict(str(rasa_citac())))

@app.route("/cat/<path:url>", methods=['GET', 'POST'])
def image_check(url):
    # ----- SECTION 1 -----  
    #File naming process for nameless base64 data.
    #We are using the timestamp as a file_name.
    from datetime import datetime
    dateTimeObj = datetime.now()
    file_name_for_base64_data = dateTimeObj.strftime("%d-%b-%Y--(%H-%M-%S)")
    
    #File naming process for directory form <file_name.jpg> data.
    #We are taken the last 8 characters from the url string.
    file_name_for_regular_data = url[-10:-4]
    
    # ----- SECTION 2 -----
    try:
        # Base64 DATA
        if "data:image/jpeg;base64," in url:
            base_string = url.replace("data:image/jpeg;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = file_name_for_base64_data + ".jpg"
            rasa_unos(os.path.abspath(file_name))
            #print(os.path.abspath(file_name) + "sasasasasa")
            img.save(file_name, "jpeg")

        # Base64 DATA
        elif "data:image/png;base64," in url:
            base_string = url.replace("data:image/png;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = file_name_for_base64_data + ".png"
            img.save(file_name, "png")
            rasa_unos(os.path.abspath(file_name))
            #print(os.path.abspath(file_name) + "sasasasasa")

        # Regular URL Form DATA
        else:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            file_name = file_name_for_regular_data + ".jpg"
            path="./images/"
            print(file_name)
            img.save(file_name, "jpeg")
            rasa_unos(os.path.abspath(file_name))
            #print(os.path.abspath(file_name) + "sasasasasa")

    # ----- SECTION 3 -----    
        status = "Image has been succesfully sent to the server."
    except Exception as e:
        status = "Error! = " + str(e)

    #rasa_unos(os.path.abspath(file_name))
    return (predict(str(rasa_citac())))
    #return os.path.abspath(file_name)     

@app.route("/", methods=['GET', 'POST'])
def error1():
    return jsonify(
        error_id='3',
        error=' Insert /cat/path:url correctly!!!'
        )

@app.route("/cat/", methods=['GET', 'POST'])
def error2():
    return jsonify(
        error_id='2',
        error=' Please insert path/url!!!'
        )

app.run(debug=True)
#app.run(host="192.168.100.151", port="5001")
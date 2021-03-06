import tensorflow as tf
import sys

# change this as you see fit
image_path = sys.argv[1]

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
    broj=0
    rezultat=0

    print('*'*50)
    for node_id in top_k:
        if broj!=2:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s = %.1f' % (human_string.upper(), score*100)+ "%")
            broj+=1
            rezultat=rezultat+score
        else:
            break
    format_rezultat = "{:.3f}".format(rezultat)
    other_breeds=((1-float(format_rezultat))*100)
    format_other_breeds ='Other breeds: '+str("{:.1f}".format(other_breeds)) + "%"
    # print(format_rezultat)
    print(format_other_breeds)
    rezultat=0
    print('*'*50)
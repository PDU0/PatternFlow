import glob
import tensorflow as tf
from model import *
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import TensorBoard

#Load data
image_files = glob.glob('../../../ISIC2018_Data/ISIC2018_Images/*.jpg')
label_files = glob.glob('../../../ISIC2018_Data/ISIC2018_Labels/*.png')

split_ratio = 0.8
split_size = int(len(image_files)*split_ratio)
data_split_size = int(len(image_files)*split_ratio*split_ratio)

#Shuffle before splitting?
train_ds = tf.data.Dataset.from_tensor_slices((image_files[:data_split_size], 
                                               label_files[:data_split_size]))
validate_ds = tf.data.Dataset.from_tensor_slices((image_files[data_split_size:split_size], 
                                               label_files[data_split_size:split_size]))
test_ds = tf.data.Dataset.from_tensor_slices((image_files[split_size:], 
                                               label_files[split_size:]))

#Pre-process data
train_ds = train_ds.shuffle(data_split_size)
validate_ds = validate_ds.shuffle(split_size-data_split_size)
test_ds = test_ds.shuffle(len(image_files)-split_size)

def map_fn(image, label):
    img = tf.io.read_file(image)
    img = tf.io.decode_jpeg(img, channels = 3)
    img = tf.image.resize(img, (256,256))
    img = tf.cast(img, tf.float32) / 255.0
    img.set_shape([256,256,3])
    
    lbl = tf.io.read_file(label)
    lbl = tf.io.decode_png(lbl, channels = 0)
    lbl = tf.image.resize(lbl, (256,256))
    lbl = tf.keras.backend.round(lbl / 255.0) #Is this fine?
    lbl = tf.cast(lbl, tf.uint8)
    lbl = tf.one_hot(lbl, depth = 2, axis = 2) #Is one-hot encoding needed for only 2 classes?
    lbl = tf.cast(lbl, tf.float32)
    lbl = tf.squeeze(lbl)
    lbl.set_shape([256,256,2])
    return img, lbl

train_ds = train_ds.map(map_fn)
validate_ds = validate_ds.map(map_fn)
test_ds = test_ds.map(map_fn)

#Check batching is working
for image, label in train_ds.take(1):
    print('Image shape: ', image.numpy().shape)
    print('Label shape: ', label.numpy().shape)
    h, w, n_channels = image.numpy().shape

#Print data size info
print("\nData info:")
print("height: %d" % h)
print("width: %d" % w)
print("channels: %d" % n_channels)

image_batch, label_batch = next(iter(train_ds.batch(1)))
test_image = np.asarray(image_batch[0])
test_label = np.asarray(label_batch[0][:,:,1])
plt.figure(figsize = (20,20))
plt.subplot(1,2,1); plt.imshow(test_image); plt.title('Image'); plt.axis('off')
plt.subplot(1,2,2); plt.imshow(test_label); plt.title('Label'); plt.axis('off')

#Build model
input_layer, output_layer = ImprovedUnet(h, w, n_channels)
model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
model.summary()

#Compile model


#Train model


#Evaluate model


#Predictions

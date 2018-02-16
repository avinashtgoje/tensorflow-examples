
import tensorflow as tf
import numpy as np

TF_RECORDS_FILE = 'example_02.tf'


# --------------------------------------------------- #
# HELPER FUNCTIONS FOR TYPES AND LISTS OF TYPES
# (https://github.com/bgshih/seglink/blob/master/tool/create_datasets.py)
# --------------------------------------------------- #
def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
def _float_feature(value):
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
def _bytes_list_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))
def _int64_list_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=value))
def _float_list_feature(value):
  return tf.train.Feature(float_list=tf.train.FloatList(value=value))


# --------------------------------------------------- #
# FUNCTION FOR CREATING TF_RECORDS DATA
# --------------------------------------------------- #

def create_tfrecords(data) :

  writer = tf.python_io.TFRecordWriter(TF_RECORDS_FILE)

  # IT'S CRITICAL THAT THIS STRUCTURE MATCHES THE DATA STRUCTURE
  # YOU ARE TRYING TO SAVE!!!
  for indx in range( data.shape[0] ):
    example = tf.train.Example(features=tf.train.Features(feature={
        'x': _float_list_feature(data[indx])    
    }))
    writer.write(example.SerializeToString())

  writer.close()

# --------------------------------------------------- #
# FUNCTIONS FOR READING TF_RECORDS DATA
# --------------------------------------------------- #

# this first method grabs the data from the file
def read_and_decode(filename_queue):
  reader = tf.TFRecordReader()

  _, serialized_example = reader.read(filename_queue)

  features = tf.parse_single_example(
      serialized_example,
      features={
          'x': tf.FixedLenFeature([6], tf.float32),
      })

  x = tf.cast(features['x'], tf.float32)
  return x


# FUNCTION CALLED BY THE TENSORFLOW FETCH OPERATION
def inputs():
  filenames = [TF_RECORDS_FILE]
  filename_queue = tf.train.string_input_producer(filenames)
  x = read_and_decode(filename_queue)
  return x


# --------------------------------------------------- #
# START THE TENSORFLOWWING!!!
# --------------------------------------------------- #


# create a 2-d array
foo = [[1, 2, 3, 4, 5, 6.01], [101, 102, 103, 104, 10.5, 106.1]]
foo = np.asarray( foo )
foo = foo.astype(np.float32)

# save to tfrecords
create_tfrecords(foo)

# create an 'input' variable
d1 = inputs()

init_op = tf.group(tf.global_variables_initializer(),
                   tf.local_variables_initializer())

with tf.Session() as sess:
  sess.run(init_op)

  coord   = tf.train.Coordinator()
  threads = tf.train.start_queue_runners(coord=coord)

  for n in range(0, 5):
      retval_x = sess.run([d1])
      print(retval_x)

  coord.request_stop()
  coord.join(threads)
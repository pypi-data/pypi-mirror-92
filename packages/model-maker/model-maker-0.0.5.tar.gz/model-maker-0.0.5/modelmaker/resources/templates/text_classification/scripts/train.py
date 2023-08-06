import numpy as np
import os
import sys
import tensorflow as tf
import tensorflow_datasets as tfds

from tensorflow import keras

file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(file_path)
project_directory = os.path.dirname(current_directory)
sys.path.insert(0, project_directory)
from {{ package_name }}.models import {{ project_name }}

######################################################################
# Prepare data
######################################################################

BUFFER_SIZE = 10000
BATCH_SIZE = 64
VOCAB_SIZE = 1000

# load and prepare data
dataset, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

# shuffle and batch data
train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
test_dataset = test_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# create text encoder
encoder = keras.layers.experimental.preprocessing.TextVectorization(max_tokens=VOCAB_SIZE)
encoder.adapt(train_dataset.map(lambda text, label: text))

######################################################################
# Train Model
######################################################################

EPOCHS = 10
VALIDATION_STEPS = 30

# load model in training mode
model = {{ project_name }}(encoder)

# train model
model.fit_model(train_dataset, test_dataset, epochs=EPOCHS, validation_steps=VALIDATION_STEPS)

######################################################################
# Save Model
######################################################################

model_folder = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ),
    "saved_models"
)
model.save_model(os.path.join(model_folder, '{{ package_name }}'))
import os
import sys
import numpy as np
from tensorflow import keras
file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(file_path)
project_directory = os.path.dirname(current_directory)
sys.path.insert(0, project_directory)
from {{ package_name }}.models import {{ project_name }}

# load model
model_path = os.path.join(project_directory, 'saved_models', '{{ package_name }}')
model = {{ project_name }}().load_model(model_path)

# load mnist dataset
_, (x_test, y_test) = keras.datasets.mnist.load_data(path="mnist.npz")

for i, x in enumerate(x_test[0:10]):
    print(model(x), y_test[i])
import numpy as np
import os
import pandas as pd
import sklearn
import sys

from sklearn.datasets import load_iris
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(file_path)
project_directory = os.path.dirname(current_directory)
sys.path.insert(0, project_directory)
from {{ package_name }}.models import {{ project_name }}

######################################################################
# Load Data
######################################################################

# load data
iris = load_iris()
df = pd.concat(
    [
        pd.DataFrame(data=iris.data, columns=iris.feature_names),
        pd.DataFrame(data=iris.target, columns=['species'])
    ],
    axis=1
)

######################################################################
# Prepare Train/Test Dataset
######################################################################

# split train test, onehot encode, generate features and target
X = pd.concat(
    [
        df.drop(['species', 'sepal length (cm)'], axis=1),
        pd.get_dummies(df['species'])
    ],
    axis=1
)
y = df['sepal length (cm)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=777)

######################################################################
# Train Model
######################################################################

# load model in training mode
model = {{ project_name }}()

# train model
model.fit_model(X_train, y_train)

######################################################################
# Validate Model
######################################################################

y_pred = model(X_test)
median_error = median_absolute_error(y_test, y_pred)
mean_error = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"{'r2:':<25} {r2}")
print(f"{'median absolute error:':<25} {median_error}")
print(f"{'mean absolute error:':<25} {mean_error}")

######################################################################
# Save Model
######################################################################

# save model
model_folder = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ),
    "saved_models"
)
model.save_model(os.path.join(model_folder, '{{ package_name }}'))

import tensorflow as tf
import numpy as np
from tensorflow import keras        
from modelmaker import ClassificationModelInterface
from .utils import normalize, rescale2d

class {{ project_name }}(ClassificationModelInterface):

    def setup(self):
        pass

    @property
    def labels(self):
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9
        }

    def get_model(self):
        num_classes = len(self.labels)
        model = keras.Sequential([
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(num_classes, activation=tf.nn.softmax),
        ])
        return model

    def fit_model(self, xy_train, xy_val, epochs=1):
        keras.backend.clear_session()
        self.model = self.get_model()
        self.model.compile(
            optimizer=keras.optimizers.Adam(),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        self.model.fit(
            xy_train,
            epochs=epochs,
            validation_data=xy_val
        )
        return self

    def save_model(self, path):
        self.model.save(path)
        return self

    def load_model(self, path):
        self.model = keras.models.load_model(path)
        return self

    def preprocess(self, x):
        y = rescale2d(x, (28, 28))
        return normalize(y, 0, 1)

    def predict(self, x):
        return self.model.predict(np.expand_dims(x, axis=0)) # insert batch axis

    def postprocess(self, x, orig):
        one_hot = self.softmax_to_one_hot(x)
        return self.one_hot_to_label(one_hot)
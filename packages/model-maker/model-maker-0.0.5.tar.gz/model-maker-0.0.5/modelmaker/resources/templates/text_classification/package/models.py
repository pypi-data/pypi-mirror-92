import numpy as np
import tensorflow as tf

from .utils import normalize
from .utils import rescale2d
from modelmaker import ClassificationModelInterface
from tensorflow import keras

class {{ project_name }}(ClassificationModelInterface):

    def setup(self, encoder=None):
        self.encoder = encoder

    @property
    def labels(self):
        return {
            0: 0,
            1: 1
        }

    def get_model(self, encoder):
        """ Get Model
        Args:
            encoder (keras.layers.experimental.preprocessing.TextVectorization): text encoder for tokenizing text

        Returns:
            keras.Model: model
        """

        model = keras.Sequential([
            encoder,
            keras.layers.Embedding(
                input_dim=len(encoder.get_vocabulary()),
                output_dim=64,
                mask_zero=True
            ),
            keras.layers.Bidirectional(
                keras.layers.LSTM(64)
            ),
            keras.layers.Dense(64, activation=tf.nn.relu),
            keras.layers.Dense(1),
        ])

        return model

    def fit_model(self, xy_train, xy_val, epochs=1, validation_steps=1):
        keras.backend.clear_session()
        self.model = self.get_model(self.encoder)
        self.model.compile(
            loss=keras.losses.BinaryCrossentropy(from_logits=True),
            optimizer=keras.optimizers.Adam(1e-4),
            metrics=['accuracy']
        )
        self.model.fit(
            xy_train,
            epochs=epochs,
            validation_data=xy_val,
            validation_steps=validation_steps
        )
        return self

    def save_model(self, path):
        self.model.save(path)
        return self

    def load_model(self, path):
        self.model = keras.models.load_model(path)
        return self

    def preprocess(self, xs):
        """
        Args:
            xs (list[str]): list of text strings
        """
        return np.array([*xs])

    def predict(self, x):
        """
        Args:
            x (np.array): input to model
        
        Returns:
            np.array: model scores
        """
        return self.model.predict(x)
        

    def postprocess(self, xs, orig):
        return np.ravel(xs)

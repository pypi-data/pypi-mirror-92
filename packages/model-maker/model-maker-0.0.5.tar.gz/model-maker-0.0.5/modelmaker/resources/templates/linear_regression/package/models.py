import numpy as np
from modelmaker import ModelInterface
from sklearn import linear_model
import pickle

class {{ project_name }}(ModelInterface):

    def setup(self):
        pass

    def get_model(self):
        return linear_model.LinearRegression()

    def fit_model(self, X, y):
        self.model = self.get_model()
        self.model.fit(self.preprocess(X), y)
        return self

    def save_model(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        return self

    def load_model(self, path):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        return self

    def preprocess(self, x):
        return x

    def predict(self, x):
        return self.model.predict(x)

    def postprocess(self, x, orig):
        return x
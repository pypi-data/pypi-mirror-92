import numpy as np
import pandas as pd
from forward_model import forward_model

class evaluation_metrics:
    def __init__(self, labels, input,parameters,activation_functions):
        self.input = input
        self.Y_true = labels
        self.parameters=parameters
        self.activations=activation_functions

    def confusionMatrix(self):
        y_hat=[]
        predictions,packet_of_packets=forward_model().forward_model(self.input,self.parameters,self.activations)
        predictions=predictions.T
        for i in range(predictions.shape[0]):
            max=np.argmax(predictions[i])
            y_hat.append(max)

        classes = set(self.Y_true[0])
        number_of_classes = len(classes)
        conf_matrix = pd.DataFrame(
            np.zeros((number_of_classes, number_of_classes), dtype=int),
            index=classes,
            columns=classes)
        for i, j in zip(self.Y_true[0], y_hat):
            conf_matrix.loc[i, j] += 1
        return conf_matrix.values, conf_matrix

    def TP(self):
        values, cm = self.confusionMatrix()
        return np.diag(cm)

    def FP(self):
        values, cm = self.confusionMatrix()
        return np.sum(cm, axis=0) - self.TP()

    def FN(self):
        values, cm = self.confusionMatrix()
        return np.sum(cm, axis=1) - self.TP()

    def Accuracy(self, data_size):
        return np.sum(self.TP()/data_size)

    def Precision(self):
        return np.mean(self.TP() / (self.TP() + self.FP()))

    def Recall(self):
        return np.mean(self.TP() / (self.TP() + self.FN()))

    def F1_score(self):
        if self.TP() > 0:
            return 2 * ((self.Precision() * self.Recall()) / (self.Precision() + self.Recall()))
        else:
            return 0




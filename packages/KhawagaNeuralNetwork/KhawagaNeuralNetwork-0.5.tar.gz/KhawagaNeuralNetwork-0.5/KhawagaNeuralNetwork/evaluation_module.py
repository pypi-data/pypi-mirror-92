import numpy as np
import pandas as pd

class Evaluation_Module:
    def __init__(self, true, pred):
        self.true = np.array(true)
        self.pred = np.array(pred)
        self.Category =range(self.true.shape[1])
        self.lowestCategory = len(self.Category)
        arrayinit = np.zeros((true.shape[1], true.shape[1]))
        self.matrix = pd.DataFrame(arrayinit, index=range(self.true.shape[1]), columns=range(self.true.shape[1]))

    def confusion_matrix(self):
        for i in range(self.true.shape[0]):
            for j in range(self.true.shape[1]):
                if self.true[i][j] == self.pred[i][j] == 1:
                    self.matrix.loc[[self.Category[j]], [self.Category[j]]] += 1

                if self.true[i][j] != self.pred[i][j]:
                    self.matrix.loc[[self.Category[np.argmax(self.pred[i])]], self.Category[np.argmax(self.true[i])]] += 1
                    break


                
        return self.matrix.rename(index = {self.Category[i]: "pred: " + str(i) for i in self.Category}, columns= {self.Category[i]: "true: " + str(i) for i in self.Category})


    def accuracy(self):
        diagonal = np.diag(self.matrix)
        acc = diagonal.sum(dtype=np.float)/(self.matrix.to_numpy().sum(dtype=np.float))
        return acc

    def percision(self):
        arrayinit = np.zeros((1, self.lowestCategory))
        precisionmatrix = pd.DataFrame(arrayinit, index=["percision"], columns=self.Category)
        print(self.lowestCategory)
        for i in range(self.lowestCategory):
            out = (self.matrix.loc[self.Category[i], self.Category[i]])/(self.matrix.loc[self.Category[i],:].to_numpy().sum(dtype=np.float))
            out = np.nan_to_num(out)
            precisionmatrix.loc["percision",self.Category[i]] = out
        return precisionmatrix

    def recall(self):
        arrayinit = np.zeros((1, self.lowestCategory))
        recallmatrix = pd.DataFrame(arrayinit, index=["recall"], columns=self.Category)
        for i in range(self.lowestCategory):
            out = (self.matrix.loc[self.Category[i], self.Category[i]])/(self.matrix.loc[:,self.Category[i]].to_numpy().sum(dtype=np.float))
            out = np.nan_to_num(out)
            recallmatrix.loc["recall",self.Category[i]] = out
        return recallmatrix

    def f1_score(self):
        arrayinit = np.zeros((1, self.lowestCategory))
        f1_scorematrix = pd.DataFrame(arrayinit, index=["f1_score"], columns=self.Category)
        recall = self.recall()
        percision = self.percision()
        for i in range(self.lowestCategory):
            out = 2*(recall.loc["recall",self.Category[i]] * percision.loc["percision",self.Category[i]])/(recall.loc["recall",self.Category[i]] + percision.loc["percision",self.Category[i]])
            out = np.nan_to_num(out)
            f1_scorematrix.loc["f1_score",self.Category[i]] = out
        return f1_scorematrix
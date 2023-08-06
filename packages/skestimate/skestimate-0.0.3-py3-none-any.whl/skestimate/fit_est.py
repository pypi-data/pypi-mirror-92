
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


class Xest:
    """
    A class of estimator, with a number of methods to evaluate the pipeline estimator performance.
    Some of the initial parameters passed to create an instance of Xest are saved into the class 
    instance to make it available as an attribute of that instance. This can be done in ___init__(),
    or other methods.
    """
    
    def __init__(self, estimator, data, target_label, ts):
        """Split data into train & test with test ratio of 'ts', 0<ts<1.
        data is also split into X and y.
        """
        self.data = data
        self.X = data.drop(target_label, axis=1)
        self.y = data[target_label]
        self.target_label = target_label
        self.estimator = estimator

        train, test = train_test_split(self.data, train_size=1-ts, test_size=ts, stratify=self.data[self.target_label],
        random_state=42)

        print(f'train: {train.shape}, test: {test.shape}')

        # Separate class label and data
        self.y_train = train[self.target_label]
        self.X_train = train.drop(self.target_label, axis=1)
        self.y_test = test[self.target_label]
        self.X_test = test.drop(self.target_label, axis=1)


    def xunique(self):
        """ Reports counts of unique values in each column of X """

        nunique_sort = self.X.nunique().sort_values(ascending=False)
        # data_types = self.X.dtypes
        return nunique_sort

    def xskew(self, imb=0.99):
        '''
        Returns the sorted list of feature names in X
        with imbalance amount exceeding "imb" parameter
        '''

        self.X = self.X.copy()

        # get the skew value of each column
        
        skew = pd.Series({col: self.X[col].value_counts().max()/self.X[col].value_counts().
        sum() for col in self.X.columns}).sort_values(ascending=False)
           
        skew_series = skew[skew >= imb]

        return skew_series


    def xfit(self):
        """
        fits a pipeline estimator and returns the estimator, and train/test scores
        """

        print("\n fitting ...")
        # The estimator attribute of the class is updated in place
        self.estimator.fit(self.X_train, self.y_train)

        print("\n predicting ...")
        y_pred = self.estimator.predict(self.X_test)

        score_train = self.estimator.score(self.X_train, self.y_train)
        score_test = self.estimator.score(self.X_test, self.y_test)

        print("\n score ...")
        print('Training score', score_train)
        print('Testing score', score_test)

        return self.estimator, score_train, score_test


    def xscore(self, fit=True):
        """ 
        Calculates accuracy, recall and precision of a classifier and plots the confusion matrix.
        If fit parameter is True, it will fit the estimator before calculating the metrics.
        """

        if fit:
            self.xfit()

        print("\n predicting y ...")
        y_pred = self.estimator.predict(self.X_test)

        print("\n plotting confusion matrix ...")
        plt.rcParams['figure.dpi'] = 80
        plot_confusion_matrix(self.estimator, self.X_test, self.y_test, values_format='.0f',
        xticks_rotation='vertical')

        print("\n calculating confusion matrix ...")
        C = pd.DataFrame(confusion_matrix(self.y_test, y_pred))
        print(C)

        truth_sum = C.sum(axis=1)
        predict_sum = C.sum(axis=0)
        pred_t = pd.Series([C.iloc[i,i] for i in range(len(C))])

        recall = pred_t / truth_sum
        precision = pred_t / predict_sum
        accuracy = pred_t.sum() / truth_sum.sum()

        print("\n classification report ...")
        print(classification_report(self.y_test, y_pred, target_names=self.estimator.classes_.astype(str)))

        print(f"******\n accuracy is {accuracy:.2f}\n******")
        print("******\n precision is ******\n", precision)
        print("******\n recall is ******\n", recall)

        return accuracy, precision, recall

def example():
    """
    This helper function is for testing the package. It loaded a dataset and create
    an instance of the Xest class. By running it in thr main .py file we create an
    instance of the Xest class in the main name space.
    
    In the main python file:
    >>> import skestimate
    >>> myest = skestimate.example()
    >>> myest.xskew(0.9)
    """
    data = pd.read_csv(
        "https://github.com/skhabiri/PredictiveModeling-CoverType-u2build/blob/master/data/train.csv?raw=true")
    
    
    from sklearn.ensemble import RandomForestClassifier
    rfc = RandomForestClassifier()

    return Xest(rfc, data, 'Cover_Type', 0.2)
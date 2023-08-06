# unittest supports a type of tests called unit tests
# A unit is the smallest cohesive piece of code we can test
# (usually something like a function or method)
# Other types of tests (you won't write now, just to be aware):
# - Integration: testing multiple pieces working together
# - End to end: testing a full "flow"/use case
# There are also manual/non-code tests that are common
# - User acceptance testing: show it to a user, get feedback
# - Manual running and checking


from fit_est import *
import unittest
import random


class Test_Xest(unittest.TestCase):
    """Tests the instantiation and use of SocialMediaUser."""

    def setUp(self):
        self.xest = example()
        # overwriting the ts number with a random number
        self.xest = Xest(self.xest.estimator, self.xest.data, self.xest.target_label, ts=random.uniform(0.1,0.5))

    def test_xskew(self):
        """Test that the minimum value of listed skew columns
        is greater than imb parameter"""
       
        skew_series = self.xest.xskew(imb=0.9)
        self.assertTrue(skew_series.values[-1] >= 0.9)


    def test_xfit(self):
        """Test the accuracy score of test and train data split for a random split!"""

        self.xest.estimator, score_train, score_test = self.xest.xfit()
        accuracy_score_train = accuracy_score(
            self.xest.y_train, self.xest.estimator.predict(self.xest.X_train))
        accuracy_score_test = accuracy_score(
            self.xest.y_test, self.xest.estimator.predict(self.xest.X_test))

        self.assertFalse(abs(score_train - accuracy_score_train) > 0.01)
        self.assertTrue(abs(score_test - accuracy_score_test) < 0.01)

    def test_xscore(self):
        """Test the accuracy of xscore vs fit"""

        self.assertTrue(abs(self.xest.xscore(fit=True)[0] - self.xest.xfit()[-1]) < 0.01)


if __name__ == '__main__':
    # This conditional is for code that will be run
    # when we execute our file from the command line
    unittest.main()

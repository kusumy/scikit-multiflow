import operator

from skmultiflow.data import influential_stream, random_rbf_generator
from skmultiflow.evaluation import evaluate_influential
from skmultiflow.trees import HoeffdingTreeClassifier
from skmultiflow.bayes import naive_bayes
from skmultiflow.core import Pipeline
from prettytable import PrettyTable
from skmultiflow.data.random_rbf_generator import RandomRBFGenerator
from skmultiflow.data.random_rbf_generator_drift import RandomRBFGeneratorDrift
import matplotlib.pyplot as plt


def demo():
    """ _test_influential

    This demo tests if the streams are correctly created and
    if the classifier chooses a new sample based on the weights
    of the streams.

    :return:
    """
    equal = PrettyTable()
    fulfilling = PrettyTable()
    defeating = PrettyTable()
    table_names = ["Run", "Feature number", "False Negative", "True Positive", "True Negative", "False positive",
                   "p-value"]
    defeating.field_names = table_names
    equal.field_names = table_names
    fulfilling.field_names = table_names

    positive_influence_fulfilling = []
    negative_influence_fulfilling = []

    positive_influence_equal = []
    negative_influence_equal = []

    positive_influence_defeating = []
    negative_influence_defeating = []

    runs = 20

    for i in range(runs):
        stream = influential_stream.InfluentialStream(self_defeating=1, self_fulfilling=1,
                                                      streams=[RandomRBFGenerator(model_random_state=99,
                                                                                  sample_random_state=50,
                                                                                  n_classes=2, n_features=2,
                                                                                  n_centroids=50),
                                                               RandomRBFGeneratorDrift(model_random_state=112,
                                                                                       sample_random_state=50,
                                                                                       n_classes=2,
                                                                                       n_features=2,
                                                                                       n_centroids=50 + i,
                                                                                       change_speed=2,
                                                                                       num_drift_centroids=50 + i)])
        evaluating(stream, i, equal, positive_influence_equal, negative_influence_equal)

    for i in range(runs):
        stream = influential_stream.InfluentialStream(self_defeating=1, self_fulfilling=1.001,
                                                      streams=[RandomRBFGenerator(model_random_state=99,
                                                                                  sample_random_state=50,
                                                                                  n_classes=2, n_features=2,
                                                                                  n_centroids=50),
                                                               RandomRBFGeneratorDrift(model_random_state=112,
                                                                                       sample_random_state=50,
                                                                                       n_classes=2,
                                                                                       n_features=2,
                                                                                       n_centroids=50 + i,
                                                                                       change_speed=2,
                                                                                       num_drift_centroids=50 + i)])
        evaluating(stream, i, fulfilling, positive_influence_fulfilling, negative_influence_fulfilling)

    for i in range(runs):
        stream = influential_stream.InfluentialStream(self_defeating=0.999, self_fulfilling=1,
                                                      streams=[RandomRBFGenerator(model_random_state=99,
                                                                                  sample_random_state=50,
                                                                                  n_classes=2, n_features=2,
                                                                                  n_centroids=50),
                                                               RandomRBFGeneratorDrift(model_random_state=112,
                                                                                       sample_random_state=50,
                                                                                       n_classes=2,
                                                                                       n_features=2,
                                                                                       n_centroids=50 + i,
                                                                                       change_speed=2,
                                                                                       num_drift_centroids=50 + i)])
        evaluating(stream, i, defeating, positive_influence_defeating, negative_influence_defeating)

    # print("equal")
    # print(equal)
    y = [*range(0, runs, 1)]
    plt.figure(1)
    plt.plot(y, positive_influence_equal)
    plt.xlabel("runs")
    plt.ylabel('p value')
    plt.title('p values positive influence, equal weights')

    plt.figure(2)
    plt.plot(y, negative_influence_equal)
    plt.xlabel('runs')
    plt.ylabel('p value')
    plt.title('p values negative influence, equal weights')

    plt.figure(3)
    plt.plot(y, positive_influence_fulfilling)
    plt.xlabel('runs')
    plt.ylabel('p value')
    plt.title('p values positive influence, self fulfilling')

    plt.figure(4)
    plt.plot(y, negative_influence_fulfilling)
    plt.xlabel('runs')
    plt.ylabel('p value')
    plt.title('p values negative influence, self fulfilling')

    plt.figure(5)
    plt.plot(y, positive_influence_defeating)
    plt.xlabel('runs')
    plt.ylabel('p value')
    plt.title('p values positive influence, self defeating')

    plt.figure(6)
    plt.plot(y, negative_influence_defeating)
    plt.xlabel('runs')
    plt.ylabel('p value')
    plt.title('p values negative influence, self defeating')

    plt.show()

    # print("defeating")
    # print(defeating)
    # print("fulfilling")
    # print(fulfilling)


def evaluating(stream, run, x, positive_influence, negative_influence):
    classifier = naive_bayes.NaiveBayes()
    # classifier = PerceptronMask()
    # classifier = HoeffdingTreeClassifier()
    # classifier = PassiveAggressiveClassifier()

    # 3. Setup the evaluator
    evaluator = evaluate_influential.EvaluateInfluential(show_plot=False,
                                                         pretrain_size=200,
                                                         max_samples=2200,
                                                         batch_size=1,
                                                         n_time_windows=2,
                                                         n_intervals=4,
                                                         metrics=['accuracy'],
                                                         data_points_for_classification=False,
                                                         weight_output=True)

    pipe = Pipeline([('Naive Bayes', classifier)])

    # 4. Run evaluation
    evaluator.evaluate(stream=stream, model=pipe)
    for result in evaluator.table_positive_influence:
        result.insert(0, run)
        if result[1] == 0:
            positive_influence.append(result[6])
            x.add_row(result)

    for result in evaluator.table_negative_influence:
        result.insert(0, run)
        if result[1] == 0:
            x.add_row(result)
            negative_influence.append(result[6])


if __name__ == '__main__':
    demo()
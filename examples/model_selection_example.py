"""MetaOD prediction with the trained model
"""
# License: BSD 2 clause

from sklearn.metrics import average_precision_score

from pyod.utils.data import generate_data
from pyod.models.loda import LODA
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.ocsvm import OCSVM


from metaod.models.utility import prepare_trained_model
from metaod.models.predict_metaod import select_model


if __name__ == "__main__":
    contamination = 0.1  # percentage of outliers
    n_train = 1000  # number of training points
    n_test = 100  # number of testing points

    # Generate sample data
    X_train, y_train, X_test, y_test = \
        generate_data(n_train=n_train,
                      n_test=n_test,
                      n_features=3,
                      contamination=contamination,
                      random_state=42)
    # load pretrained models
    prepare_trained_model()

    # recommended models
    selected_models = select_model(X_train, n_selection=100)


    print("Showing the top recommended models...")
    for i, model in enumerate(selected_models):
        print(i, model)

    print()

    model_1 = LODA(n_bins=5, n_random_cuts=100)
    print("1st model Average Precision", average_precision_score(y_train, model_1.fit(X_train).decision_scores_))

    model_10 = LODA(n_bins=5, n_random_cuts=20)
    print("10th model Average Precision", average_precision_score(y_train, model_10.fit(X_train).decision_scores_))


    model_50 = OCSVM(kernel= 'sigmoid', nu=0.6) 
    print("50th model Average Precision", average_precision_score(y_train, model_50.fit(X_train).decision_scores_))

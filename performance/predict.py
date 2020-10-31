import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


class Predict:

    def __init__(self, file_location):
        """<h2 style='color:blue'>Data Load: Load banglore home prices into a dataframe</h2>"""

        df = pd.read_csv(file_location)

        if df.empty:
            raise Exception('Dataframe is empty')

        X = df.drop(['points'], axis='columns')

        y = df.points

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

        self.lr_clf = LinearRegression()
        self.lr_clf.fit(X_train, y_train)
        self.score = self.lr_clf.score(X_test, y_test)

        """<h2 style='color:blue'>Use K Fold cross validation to measure accuracy of our LinearRegression model</h2>"""

        cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

        cross_val_score(LinearRegression(), X, y, cv=cv)

        """**We can see that in 5 iterations we get a score above 80% all the time. This is pretty good but we want to test few other algorithms for regression to see if we can get even better score. We will use GridSearchCV for this purpose**
        
        <h2 style='color:blue'>Find best model using GridSearchCV</h2>
        """

    def find_best_model_using_gridsearchcv(X, y):
        algos = {
            'linear_regression': {
                'model': LinearRegression(),
                'params': {
                    'normalize': [True, False]
                }
            },
            'lasso': {
                'model': Lasso(),
                'params': {
                    'alpha': [1, 2],
                    'selection': ['random', 'cyclic']
                }
            },
            'decision_tree': {
                'model': DecisionTreeRegressor(),
                'params': {
                    'criterion': ['mse', 'friedman_mse'],
                    'splitter': ['best', 'random']
                }
            }
        }
        scores = []
        cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
        for algo_name, config in algos.items():
            gs = GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
            gs.fit(X, y)
            scores.append({
                'model': algo_name,
                'best_score': gs.best_score_,
                'best_params': gs.best_params_
            })

        return pd.DataFrame(scores, columns=['model', 'best_score', 'best_params'])

        # find_best_model_using_gridsearchcv(X, y)

    def predict_points(self, **stats):
        return self.lr_clf.predict([tuple(stats.values())])[0]

        # """<h2 style='color:blue'>Export the tested model to a pickle file</h2>"""
        #
        # with open('banglore_home_prices_model.pickle', 'wb') as f:
        #     pickle.dump(lr_clf, f)
        #
        # """<h2 style='color:blue'>Export location and column information to a file that will be useful later on in our prediction application</h2>"""
        #
        # columns = {
        #     'data_columns': [col.lower() for col in X.columns]
        # }
        # with open("columns.json", "w") as f:
        #     f.write(json.dumps(columns))

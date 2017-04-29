import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.tree import  DecisionTreeClassifier

df = pd.read_csv("iris_pandas.csv")

featurs = df.columns[:4].tolist()
x=df[featurs]
y=df["Species"]


# Podela podataka na trening i test skup
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

# Parametri za unakrsnu validacuju
parameters = [{'criterion': ['gini', 'entropy'],
               'min_samples_split':[15, 10, 15],
               'min_samples_leaf': [2, 4, 6],
               'min_impurity_split': [0, 0.0001, 0.001]
               }]

scores = ['precision', 'f1']

for score in scores:
    print("Mera ", score)
    print()

    """
    GridSearchCV - klasa za pravljenje modela sa razlicitim parametrima za zadati klasifikator

    parametri:
    estimator - klasifikator
    param_grid - recnik ili lista recnika sa definisanim mogucim vrednostima za parametre klasifikatora
    scoring -  mera za proveru modela
    cv - generator unakrsne validacije
    default= 3-fold
    refit - da li ponovo napraviti model sa najboljim parametrima nad celim skupom podataka.
            Da bi mogla da se radi predikcija nad drugim skupom potrebno je staviti True.
            default=True

    atributi:
    cv_results_ - recnik sa podacima o zadatim parametrima i rezultatima
    best_estimator_ - najbolji klasifikator
    best_score_ - najbolji skor
    best_params_  - parametri koji daju najbolji rezultat
    scorer_  - funkcija za skor
    """

    clf = GridSearchCV(DecisionTreeClassifier(), parameters, cv=5, scoring='%s_macro' % score)
    clf.fit(x_train, y_train)

    print("Najbolji parametri:")
    print(clf.best_params_)
    print()
    print("Ocena uspeha po klasifikatorima:")
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) za %s" % (mean, std * 2, params))
    print()

    print("Izvestaj za test skup:")
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred))
    print()

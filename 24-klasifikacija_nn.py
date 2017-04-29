import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import sklearn.metrics as met
from termcolor import colored

def class_info(clf, y_test, y_pred):

    print(clf)

    cnf_matrix = met.confusion_matrix(y_test, y_pred)
    print("Matrica konfuzije", cnf_matrix, sep="\n")
    print("\n")

    accuracy = met.accuracy_score(y_test, y_pred)
    print("Preciznost", accuracy)
    print("\n")

    class_report = met.classification_report(y_test, y_pred, target_names=df["Species"].unique())
    print("Izvestaj klasifikacije", class_report, sep="\n")

    print('Gubitak: ', clf.loss_)
    print('Broj iteracija: ', clf.n_iter_)
    print('Broj slojeva: ', clf.n_layers_)
    print('Koeficijenti:', clf.coefs_, sep='\n')
    print('Bias:', clf.intercepts_, sep='\n')

df = pd.read_csv("iris.csv")

featurs = df.columns[:4].tolist()

x=df[featurs]
x.columns = featurs
y=df["Species"]


#podela na trening i test skup
x_train_original, x_test_otiginal, y_train, y_test = train_test_split(x, y, train_size=0.7, stratify=y)

#standardizacija podataka
scaler = preprocessing.StandardScaler().fit(x_train_original)
x_train =pd.DataFrame(scaler.transform(x_train_original))
x_train.columns = featurs
x_test = pd.DataFrame(scaler.transform(x_test_otiginal))
x_test.columns = featurs

"""
hidden_layer_sizes  - brojevi neurona u skrivenim slojevima
                      default=100

activation - aktivaciona fja
                      identity    f(x) = x
                      logistic    sigmoidna fja  f(x) = 1 / (1 + exp(-x))
                      tanh        tangens hiperbolicki f(x) = tanh(x)
                      relu        f(x) = max(0, x)

solver - resavac za optimizaciju tezina
                      sgd   stohastickog opadajuceg gradijenta

batch_size - velicina serija: broj instanci u jednom koraku za racunanje gradijenta
             default = 200

learning_rate - stopa ucenja pri azuriranju tezina
              constant   konstantna, zadata sa learning_rate_init
              invscaling  postepeno smanjenje stope ucenja u koraku t, effective_learning_rate = learning_rate_init / pow(t, power_t)
              adaptive    stopa ucenja se ne menja dok se vrednost fje gubitka  smanjuje.
                          Kad se u dva uzastopna koraka gubitak ne smanji za bar vrednost tol,
                          ili se precisnost nad skupom za validaciju (ako je zadato da postoji takav skup)
                          za bar vrednost tol, stopa ucenja se seli sa

learning_rate_init - inicijalna stopa ucenja
              default=0.001
power_t
         default=0.5

max_iter - maksimalan broj iteracija
               default=200

tol - tolerancija optimizacije za gubitak ili preciznost
               default = 1e-4

shuffle - da li izvrsiti mesanje instanci za svaku iteraciju
          default=False

verbose - da li ispisati poruke o progresu na standardni izlaz

early_stopping - da li izvrsiti rano zaustavljanje kada se preciznost nad skupom za validaciju
                 ne povecava, za validaciju se onda uzima 10% trening skupa
                 default=False

validation_fraction - koji deo skupa za treniranje se koristi za validaciju
                      Primenjivo ako je early_stopping=True
                default=0.1
"""

params = [{'solver':'sgd', 'learning_rate':'constant', 'learning_rate_init':0.2, 'momentum':0,
           'max_iter':300}]

activations = ['identity', 'logistic', 'tanh', 'relu' ]
batch_sizes = [1, 5, 10, 20]
learning_rate_inits = [0.01, 0.005, 0.002, 0.001]
learning_rates = ['constant', 'invscaling', 'adaptive']
max_iters = [100, 200, 250]
early_stoppings =[True]


clfs = []

for activation in activations:
    for batch_size in batch_sizes:
        for learning_rate_init in learning_rate_inits:
            for learning_rate in learning_rates:
                for max_iter in max_iters:
                    for early_stopping in early_stoppings:

                        clf =MLPClassifier(solver='sgd',
                                           learning_rate=learning_rate,
                                           learning_rate_init=learning_rate_init,
                                           activation=activation,
                                           batch_size=batch_size,
                                           max_iter=max_iter,
                                           early_stopping=early_stopping,
                                           hidden_layer_sizes=(10,)
                                           )

                        clf.fit(x_train, y_train)
                        y_pred = clf.predict(x_test)
                        accuracy = met.accuracy_score(y_test, y_pred)
                        f1_score = met.f1_score(y_test, y_pred, average='macro')
                        clfs.append((clf, accuracy, f1_score, y_pred))


max_accuracy = max(clfs,key=lambda item:item[1])[1]
max_f1 = max(clfs,key=lambda item:item[2])[2]

print('Maksimalna preciznost: ', max_accuracy)
print('Maksimalna f1 mera: ', max_f1)

for clf in clfs:
    if clf[1] == max_accuracy:
        print(colored('model with max accuracy', 'blue'))
        class_info(clf[0], y_test, clf[3])

    elif clf[2] == max_f1 and max_accuracy!=1:
        print(colored('model with max f1', 'red'))
        class_info(clf[0], y_test, clf[3])

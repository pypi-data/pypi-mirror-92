class mlbnm:
    def ml1():
        print(f"import csv\n")
        print('updated')
        print(f"with open('tennis.csv', 'r') as f: \n reader = csv.reader(f) \n your_list = list(reader)\n h = [['0', '0', '0', '0', '0', '0']]\nfor i in your_list:\n")
        print(f"if i[-1] == Yes:\n j = 0\n for x in i:\n if x != Yes:\n if x != h[0][j] and h[0][j] == '0':\nh[0][j] = x\nelif x != h[0][j] and h[0][j] != '0':\nh[0][j] = '?'\n")
        print(f"else:\npass\nj=j+1\nprint(h)")

    def ml2():
        a='''import pandas as pd
df = pd.read_csv('carmodel.csv')
hold=list()

for i in range(df.shape[0]):
  print(list(df.iloc[i]))
  hold.append(list(df.iloc[i]))
    
g=list()
s = hold[0].copy()# first row
#print(s)
s.pop() # first row without last column
print(s)
z=1

hold

for i in hold[1:]: 
  if i[-1] == 'Positive':
    print(f"Step {z}") 
    z=z+1
    for j in range(len(s)):
      if i[j] != s[j] :
        print(i[j],s[j])
        s[j] = '?'
        print('\n S:'.format(i),s)
        print('\n G:'.format(i),g)
  else:
    print(f"Step {z}")  
    z=z+1
    for j in range(len(s)):
      v = ['?','?','?','?','?','?']
      if i[j] != s[j] and s[j]!='?' :
        v[j]=s[j]
        # print(i[j],first[j])
        g.append(v)
        print('\n S:'.format(i),s)
        print('\n G:'.format(i),g)
 k=0
for i in g:
  for j in i:
    if j != '?' and j not in s:
      print(g[k])  
      g.pop(k)
  k=k+1 

print("\nFinal Hypothesis :")
print("\nSpecialized :",s)
print("Generalized :",g)
'''
        print(a)

    
    def ml3():
        b='''import pandas as pd
import math


# function to calculate the entropy of entire dataset
def base_entropy(dataset):
    p = 0
    n = 0
    target = dataset.iloc[:, -1]
    targets = list(set(target))
    for i in target:
        if i == targets[0]:
            p = p + 1
        else:
            n = n + 1
    if p == 0 or n == 0:
        return 0
    elif p == n:
        return 1
    else:
        entropy = 0 - (
            ((p / (p + n)) * (math.log2(p / (p + n))) + (n / (p + n)) * (math.log2(n / (p + n)))))
        return entropy


# function to calculate the entropy of attributes
def entropy(dataset, feature, attribute):
    p = 0
    n = 0
    target = dataset.iloc[:, -1]
    targets = list(set(target))
    for i, j in zip(feature, target):
        if i == attribute and j == targets[0]:
            p = p + 1
        elif i == attribute and j == targets[1]:
            n = n + 1
    if p == 0 or n == 0:
        return 0
    elif p == n:
        return 1
    else:
        entropy = 0 - (
            ((p / (p + n)) * (math.log2(p / (p + n))) + (n / (p + n)) * (math.log2(n / (p + n)))))
        return entropy
        def counter(target, attribute, i):
    p = 0
    n = 0
    targets = list(set(target))
    for j, k in zip(target, attribute):
        if j == targets[0] and k == i:
            p = p + 1
        elif j == targets[1] and k == i:
            n = n + 1
    return p, n
def Information_Gain(dataset, feature):
    Distinct = list(set(feature))
    Info_Gain = 0
    for i in Distinct:
        Info_Gain = Info_Gain + feature.count(i) / len(feature) * entropy(dataset, feature, i)
    Info_Gain = base_entropy(dataset) - Info_Gain
    return Info_Gain



# function that generates the childs of selected Attribute
def generate_childs(dataset, attribute_index):
    distinct = list(dataset.iloc[:, attribute_index])
    childs = dict()
    for i in distinct:
        childs[i] = counter(dataset.iloc[:, -1], dataset.iloc[:, attribute_index], i)
    return childs


# function that modifies the dataset according to the impure childs
def modify_data_set(dataset,index, feature, impurity):
    size = len(dataset)
    subdata = dataset[dataset[feature] == impurity]
    del (subdata[subdata.columns[index]])
    return subdata
def greatest_information_gain(dataset):
    max = -1
    attribute_index = 0
    size = len(dataset.columns) - 1
    for i in range(0, size):
        feature = list(dataset.iloc[:, i])
        i_g = Information_Gain(dataset, feature)
        if max < i_g:
            max = i_g
            attribute_index = i
    return attribute_index


# function to construct the decision tree
def construct_tree(dataset, tree):
    target = dataset.iloc[:, -1]
    impure_childs = []
    attribute_index = greatest_information_gain(dataset)
    childs = generate_childs(dataset, attribute_index)
    tree[dataset.columns[attribute_index]] = childs
    targets = list(set(dataset.iloc[:, -1]))
    for k, v in childs.items():
        if v[0] == 0:
            tree[k] = targets[1]
        elif v[1] == 0:
            tree[k] = targets[0]
        elif v[0] != 0 or v[1] != 0:
            impure_childs.append(k)
    for i in impure_childs:
        sub = modify_data_set(dataset,attribute_index, dataset.columns[attribute_index], i)
        tree = construct_tree(sub, tree)
    return tree

'''
        print(b)



    def ml4():
        c='''import numpy as np
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)
X = X/np.amax(X,axis=0) # maximum of X array longitudinally
y = y/100
def sigmoid (x):
    return 1/(1 + np.exp(-x))
def derivatives_sigmoid(x):
    return x * (1 - x)
#Variable initialization
epoch=7000 #Setting training iterations
lr=0.1 #Setting learning rate
inputlayer_neurons = 2 #number of features in data set
hiddenlayer_neurons = 3 #number of hidden layers neurons
output_neurons = 1 #number of neurons at output layer
#weight and bias initialization
wh=np.random.uniform(size=(inputlayer_neurons,hiddenlayer_neurons))
bh=np.random.uniform(size=(1,hiddenlayer_neurons))
wout=np.random.uniform(size=(hiddenlayer_neurons,output_neurons))
bout=np.random.uniform(size=(1,output_neurons))
#draws a random range of numbers uniformly of dimx*y
for i in range(epoch):
    #Forward Propogation
    hinp1=np.dot(X,wh)
    hinp=hinp1 + bh
    hlayer_act = sigmoid(hinp)
    outinp1=np.dot(hlayer_act,wout)
    outinp= outinp1+ bout
    output = sigmoid(outinp)
    
    #Backpropagation
    EO = y-output
    outgrad = derivatives_sigmoid(output)
    d_output = EO* outgrad
    EH = d_output.dot(wout.T)
    hiddengrad = derivatives_sigmoid(hlayer_act)
    
    #how much hidden layer wts contributed to error
    d_hiddenlayer = EH * hiddengrad
    wout += hlayer_act.T.dot(d_output) *lr
    
    # dotproduct of nextlayererror and currentlayerop
    bout += np.sum(d_output, axis=0,keepdims=True)*lr
    
    #Updating Weights
    wh += X.T.dot(d_hiddenlayer) *lr

print("Input: \n" + str(X))
print("Actual Output: \n" + str(y))
print("Predicted Output: \n" ,output)'''
        print(c)

    def ml5():
        d='''print("\nNaive Bayes Classifier for concept learning problem")
import csv
import random
import math
import operator

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y
	
def loadCsv(filename):
	lines = csv.reader(open(filename))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset
 
def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	i=0
	while len(trainSet) < trainSize:
		#index = random.randrange(len(copy))
		
		trainSet.append(copy.pop(i))
	return [trainSet, copy]
 
def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated
 
def mean(numbers):
	return safe_div(sum(numbers),float(len(numbers)))
	
def stdev(numbers):
	avg = mean(numbers)		
	variance = safe_div(sum([pow(x-avg,2) for x in numbers]),float(len(numbers)-1))
	return math.sqrt(variance)
 
#Calculate mean and stddev for each attribute in the dataset
def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries
 
def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	summaries = {}	
	for classValue, instances in separated.items():		
		summaries[classValue] = summarize(instances)
	print(summaries)
	return summaries
 
def calculateProbability(x, mean, stdev):	
	exponent = math.exp(-safe_div(math.pow(x-mean,2),(2*math.pow(stdev,2))))
	final = safe_div(1 , (math.sqrt(2*math.pi) * stdev)) * exponent
	return final
 
def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]			
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities
			
def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel
 
def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions
 
def getAccuracy(testSet, predictions):
	correct = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	accuracy = safe_div(correct,float(len(testSet))) * 100.0
	return accuracy
 
def main():
	filename = 'ConceptLearning.csv'
	splitRatio = 0.95
	dataset = loadCsv(filename)
	trainingSet, testSet = splitDataset(dataset, splitRatio)
	print('Split {0} rows into'.format(len(dataset)))
	print('Number of Training data: ' + (repr(len(trainingSet))))
	print('Number of Test Data: ' + (repr(len(testSet))))
	print("\nThe values assumed for the concept learning attributes are\n")
	print("OUTLOOK=> Sunny=1 Overcast=2 Rain=3\nTEMPERATURE=> Hot=1 Mild=2 Cool=3\nHUMIDITY=> High=1 Normal=2\nWIND=> Weak=1 Strong=2")
	print("TARGET CONCEPT:PLAY TENNIS=> Yes=10 No=5")
	print("\nThe Training set are:")
	for x in trainingSet:
		print(x)
	print("\nThe Test data set are:")
	for x in testSet:
		print(x)
	print("\n")
	# prepare model
	summaries = summarizeByClass(trainingSet)
	# test model
	predictions = getPredictions(summaries, testSet)
	actual = []
	for i in range(len(testSet)):
		vector = testSet[i]
		actual.append(vector[-1])
	# Since there are five attribute values, each attribute constitutes to 20% accuracy. So if all attributes match with predictions then 100% accuracy
	print('Actual values: {0}%'.format(actual))	
	print('Predictions: {0}%'.format(predictions))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: {0}%'.format(accuracy))
 
main()
'''
        print(d)

    def ml6():
        print('''import numpy as np
import pandas as pd
import sklearn
data = pd.read_csv("PlayTennis.csv")
data.head()
data=data.apply(LabelEncoder().fit_transform)
data.head()
#Define the features and the target variables.
features = ["Outlook", "Temperature", "Humidity", "Wind"]
target = "Play Tennis"
features_train, features_test, target_train, target_test = train_test_split(data[features],data[target],
test_size = 0.23,random_state = 54)
model = GaussianNB()
model.fit(features_train, target_train)


#----METRICS
pred = model.predict(features_test)
accuracy = accuracy_score(target_test, pred)
recall=recall_score(target_test, pred)
precision=precision_score(target_test, pred)
print(accuracy,recall,precision,sep='\n')''')

    def ml7():
        print('''import numpy as np
import csv
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
#read Cleveland Heart Disease data
heartDisease = pd.read_csv('heart.csv')
heartDisease.head()

del heartDisease['oldpeak']
del heartDisease['slope']
del heartDisease['ca']
del heartDisease['thal']

heartDisease = heartDisease.replace('?',np.nan)
heartDisease.head()
model = BayesianModel([('age', 'trestbps'), ('age', 'fbs'), ('gender', 'trestbps'), ('gender', 'fbs'), 
                       ('exang', 'trestbps'),('trestbps','heartdisease'),('fbs','heartdisease'),
                      ('heartdisease','restecg'),('heartdisease','thalach'),('heartdisease','chol')])
print('\n Learning CPD using Maximum likelihood estimators')
model.fit(heartDisease,estimator=MaximumLikelihoodEstimator)
print('\n Probability of HeartDisease for given Age')
print(model.get_cpds('age'))
print('\n Probability of HeartDisease for given Gender')
print(model.get_cpds('gender'))
print("Inferencing with Bayesian Network")

from pgmpy.inference import VariableElimination
HeartDisease_infer = VariableElimination(model)

# Computing the probability of bronc given smoke.
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'age': 28})
print(q)
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'chol': 100})
print(q)''')

    def ml8():
        print('''import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
iris = load_iris()

import pandas as pd
X = pd.DataFrame(iris.data)
y = pd.DataFrame(iris.target)

import numpy as np
colormap = np.array(['red', 'lime', 'black'])
plt.figure(figsize=(14,7))

from sklearn.cluster import KMeans
model = KMeans(n_clusters=3)
model.fit(X)
plt.subplot(1, 2, 2)
plt.scatter(X[2],X[3], c=colormap[model.labels_])
plt.title('K Mean Classification')

import sklearn.metrics as sm
print(sm.accuracy_score(y, model.labels_))

from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3)
gmm.fit(X)
y_cluster_gmm=gmm.predict(X)
plt.subplot(1, 2, 1)
plt.scatter(X[2],X[3], c=colormap[y_cluster_gmm])
plt.title('GMM Classification')

print(sm.accuracy_score(y, y_cluster_gmm))
print(sm.confusion_matrix(y, y_cluster_gmm))
''')
    def ml9():
        print('''from sklearn.datasets import load_iris 
from sklearn.neighbors import KNeighborsClassifier 
import numpy as np 
from sklearn.model_selection import train_test_split 
iris_dataset=load_iris() 
X_train, X_test, y_train, y_test = train_test_split(iris_dataset["data"], iris_dataset["target"], random_state=0) 
kn = KNeighborsClassifier() 
kn.fit(X_train, y_train) 
prediction = kn.predict(X_test)
print("ACCURACY:"+ str(kn.score(X_test, y_test)))
target_names = iris_dataset.target_names
for pred,actual in zip(prediction,y_test):
    print("Prediction is "+str(target_names[pred])+", Actual is "+str(target_names[actual]))''')


    def ml10():
        print('''from math import ceil
import numpy as np
from scipy import linalg  
 
 
def lowess(x, y, f= 2. / 3., iter=3):
    
    n = len(x) # Number of x  points 
    r = int(ceil(f * n))  # Computing the residual of smoothing functions 
    h = [np.sort(np.abs(x - x[i]))[r] for i in range(n)] # 
    w = np.clip(np.abs((x[:, None] - x[None, :]) / h), 0.0, 1.0)  # Weight Function 
    w = (1 - w ** 3) ** 3  # Tricube Weight Function
    ypred = np.zeros(n) # Initialisation of predictor 
    delta = np.ones(n)  # Initialisation of delta
   
    for iteration in range(iter):
        for i in range(n):
            weights = delta * w[:, i] # Cumulative Weights 
            b = np.array([np.sum(weights * y), np.sum(weights * y * x)]) # Matrix B
            A = np.array([[np.sum(weights), np.sum(weights * x)],
                          [np.sum(weights * x), np.sum(weights * x * x)]]) # Matrix A
                      
            beta = linalg.solve(A, b) # Beta,Solution of AX= B equation 
            ypred[i] = beta[0] + beta[1] * x[i]
             
        residuals = y - ypred   # Finding Residuals
        s = np.median(np.abs(residuals))  # Median of Residuals
        delta = np.clip(residuals / (6.0 * s), -1, 1)  # Delta
        delta = (1 - delta ** 2) ** 2   # Delta 
 
    return ypred

if __name__ == '__main__':  # Main Function
    
    import math
    
    n = 100  # Number of data points
   
    #Case1: Sinusoidal Fitting 
    x = np.linspace(0, 2 * math.pi, n)
    print(x)
    y = np.sin(x) + 0.3 * np.random.randn(n) 
    
    #Case2 : Straight Line Fitting
    #x=np.linspace(0,2.5,n) # For Linear
    #y= 1 + 0.25*np.random.randn(n) # For Linear
    
    f = 0.25
    ypred = lowess(x, y, f=f, iter=3)
    
    import pylab as pl
    pl.clf()
    pl.plot(x, y, label='Y NOISY')
    pl.plot(x, ypred, label='Y PREDICTED')
    pl.legend()
    pl.show()
''')

        
            

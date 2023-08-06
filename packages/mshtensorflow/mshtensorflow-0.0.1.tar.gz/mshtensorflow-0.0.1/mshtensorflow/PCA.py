import numpy as np

#X is matrix of m*d where m is no. of samples and d is no. of features
#n is an integer >= 1 indiacting no. of components or n is a decimal between 0 and 1 indicating variance
#returns reduced_x matrix of k*m where k is no. of reduced features and m no of samples

class PCA:
    def __init__(self, n):
        if n <1:
            self.variance = n
            self.choice=False
        else:
            self.n_components = n
            self.choice = True
        self.components = None
        self.mean = None
        self.std = None

    def fit(self, X):
        # Mean centering
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)+0.00001 #adding af small value to prevent dividing by zero

        X = (X - self.mean)/self.std

        # covariance, function needs samples as columns
        cov = np.cov(X.T)
        # eigenvalues, eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(cov)
        # -> eigenvector v = [:,i] column vector, transpose for easier calculations
        # sort eigenvectors
        eigenvectors = eigenvectors.T
        idxs = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idxs]
        eigenvectors = eigenvectors[idxs]

        if self.choice == True:
            # store first n eigenvectors
            self.components = eigenvectors[0:self.n_components]
        else:
            # Identifying components that explain at least variance equals n*100
            variance_vector= []
            for i in eigenvalues:
                variance_vector.append((i / sum(eigenvalues)) * 100)
            accumlated_variance = np.cumsum(variance_vector)
            self.n_components = len(  accumlated_variance[  accumlated_variance< (self.variance * 100)])
            self.components = eigenvectors[0:self.n_components]


    def transform(self, X):
        # project data
        #X = (X - self.mean)/self.std
        reduced_x=(np.dot(X, self.components.T)).T
        return reduced_x


#testing using iris dataset
'''import pandas as pd
import matplotlib.pyplot as plt
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data" # Get the IRIS dataset
data = pd.read_csv(url, names=['sepal length', 'sepal width', 'petal length', 'petal width', 'target'])
# prepare the data
x = data.iloc[:, 0:4]
# prepare the target
target = data.iloc[:, 4]

# Applying it to PCA function(how to use PCA class)

pca=PCA(2)  #using no. components
#pca=PCA(0.98)  #using variance
pca.fit(x)
print(x.shape)
mat_reduced = (pca.transform(x)).T
print(mat_reduced.shape)
# Creating a Pandas DataFrame of reduced Dataset
principal_df = pd.DataFrame(mat_reduced, columns=['PC1', 'PC2'])
# Concat it with target variable to create a complete Dataset
finalDf = pd.concat([principal_df, pd.DataFrame(target)], axis=1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'PC1']
               , finalDf.loc[indicesToKeep, 'PC2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()
plt.show()'''

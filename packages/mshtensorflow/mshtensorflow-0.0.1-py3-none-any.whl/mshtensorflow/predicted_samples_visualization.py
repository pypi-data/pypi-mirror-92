import matplotlib.pyplot as plt
import numpy as np

def sample_visualization(M_C,y_test,x_test,test_pred_class):
        correct_index = [[None for i in range(5)] for j in range(10)]
        wrong_index=[[None for i in range(5)] for j in range(10)]
        
        #x_test dimensions are (m,c,h,w)
        
        '''
        #change dimensions to (m,h,w,c) (easier to plot)
        
        x_test = x_test.transpose(0,2,3,1)
        '''
        
        
        '''
        #to change from (m,c,h,w) to (number of features,m)
        
        x_test = x_test.reshape(m,-1).T
        '''

        for i in range(10) :
            label=np.where(y_test == i )[0]
            pred=np.where(test_pred_class ==i)[0]
            #print(*label)
            #print("\n")
            #print(*pred)
            #print("\n")
            #print("\n")
            correct = []
            wrong = []
            for k in pred:
                if( k in label) :
                    correct.append(k)
                else:
                    wrong.append (k)
            #print(*correct)
            #print("\n")
            #print(*wrong)
            #print("\n")
            #print("\n")
            #print(len(correct))
            #print(len(wrong))

            for j in range(len(correct)):
                if j==5:
                    break
                else:
                    correct_index[i][j]=correct[j]
                    #print(*correct_index)
            for k in range(len(wrong)):
                if k==5:
                    break
                else:
                    wrong_index[i][k]=wrong[k]
                    #print(*wrong_index)
            #print(*correct_index)
            #print("\n")
            #print(*wrong_index)
            #print("\n")
        fig, axes = plt.subplots(10, 10, figsize=(20, 20))
        fig.subplots_adjust(hspace=0.1, wspace=0.1)

        for i in range(10):
            for j in range(5):
                if correct_index[i][j]!=-1:
                   indx1 = correct_index[i][j]
                   if M_C == True : # MNIST dataset
                       axes[j, i].imshow(x_test[:, indx1].reshape((28,28)),cmap='gray')
                   else: #CIFAR-10 dataset
                       #axes[j, i].imshow(x_test[:, indx1].reshape((32,32,3)))  #used instead of following lines when using tensorflow
                       img = x_test[:, indx1]
                       R = img[0:1024].reshape(32, 32)
                       G = img[1024:2048].reshape(32, 32)
                       B = img[2048:].reshape(32, 32)
                       img = np.dstack((R, G, B))
                       axes[j, i].imshow(img, interpolation='bicubic')
            for k in range(5):
                if wrong_index[i][k]!= -1:
                   indx2= wrong_index[i][k]
                   if M_C == True : # MNIST dataset
                       axes[k+5, i].imshow(x_test[:, indx2].reshape((28,28)),cmap='gray')
                   else: #CIFAR-10 dataset
                       #axes[k + 5, i].imshow(x_test[:, indx2].reshape((32, 32,3))) #used instead of following lines when using tensorflow
                       img = x_test[:, indx2]
                       R = img[0:1024].reshape(32, 32)
                       G = img[1024:2048].reshape(32, 32)
                       B = img[2048:].reshape(32, 32)
                       img = np.dstack((R, G, B))
                       axes[k + 5, i].imshow(img, interpolation='bicubic')
        if M_C == True:  # MNIST dataset
            fig.suptitle('MNIST dataset \n \n1st 5 rows of correct prediction samples & 2nd 5 rows of wrong prediction samples',size=16)
        else:  # CIFAR-10 dataset
            fig.suptitle('CIFAR-10 dataset \n \n1st 5 rows of correct prediction samples & 2nd 5 rows of wrong prediction samples',
                size=16)

        plt.show(block=True)


#testing by using tensorflow
'''def test(M_C ):
    if M_C == True:  # MNIST dataset
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers
        from tensorflow.keras.datasets import mnist
        import os
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train = x_train.reshape(-1, 28 * 28).astype("float32") / 255
        x_test = x_test.reshape(-1, 28 * 28).astype("float32") / 255
        X_test = x_test.T
        # Sequential API (Very convenient, not very flexible)
        model = keras.Sequential(
            [
                keras.Input(shape=(28 * 28)),
                layers.Dense(512, activation="relu"),
                layers.Dense(256, activation="relu"),
                layers.Dense(10),
            ])
        model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=0.001))
        model.fit(x_train, y_train, epochs=20)
        test_pred_class = np.argmax(model.predict(x_test), axis=1)
    else:  # CIFAR-10 dataset:
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers
        from tensorflow.keras.datasets import mnist
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        x_train = x_train.reshape(-1, 32 * 32 * 3).astype('float32') / 256
        x_test = x_test.reshape(-1, 32 * 32 * 3).astype('float32') / 256
        X_test = x_test.T
        # Sequential API (Very convenient, not very flexible)
        model = keras.Sequential(
            [
                keras.Input(shape=(32 * 32 * 3)),
                layers.Dense(512, activation="relu"),
                layers.Dense(256, activation="relu"),
                layers.Dense(10),
            ]
        )
        model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=0.001))
        model.fit(x_train, y_train, epochs=20)
        test_pred_class = np.argmax(model.predict(x_test), axis=1)
    return y_test, X_test, test_pred_class
    #print(*test_pred_class)'''

''''#calling test
#y_test =Label_Train
#x_test =Features_Test
#test_pred_class ----> output of model.predict(after np.argmax())
M_C = True
y_test,x_test,test_pred_class=test(M_C)
sample_visualization(M_C,y_test,x_test,test_pred_class)
M_C = False
y_test,x_test,test_pred_class=test(M_C)
sample_visualization(M_C,y_test,x_test,test_pred_class)'''
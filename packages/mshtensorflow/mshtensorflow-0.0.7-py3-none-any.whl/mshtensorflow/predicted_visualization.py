import matplotlib.pyplot as plt
import numpy as np

def sample_visualization(M_C, y_test, x_test, test_pred_class):
        correct_index = [[None for i in range(5)] for j in range(10)]
        wrong_index = [[None for i in range(5)] for j in range(10)]

        for i in range(10):
            label = np.where(y_test == i)[0]
            pred = np.where(test_pred_class == i)[0]
            # print(*label)
            # print("\n")
            # print(*pred)
            # print("\n")
            # print("\n")
            correct = []
            wrong = []
            for k in pred:
                if (k in label):
                    correct.append(k)
                else:
                    wrong.append(k)
            # print(*correct)
            # print("\n")
            # print(*wrong)
            # print("\n")
            # print("\n")
            # print(len(correct))
            # print(len(wrong))

            for j in range(len(correct)):
                if j == 5:
                    break
                else:
                    correct_index[i][j] = correct[j]
                    # print(*correct_index)
            for k in range(len(wrong)):
                if k == 5:
                    break
                else:
                    wrong_index[i][k] = wrong[k]
                    # print(*wrong_index)

        fig, axes = plt.subplots(10, 10, figsize=(10, 10))
        fig.subplots_adjust(hspace=0.1, wspace=0.1)

        for i in range(10):
            for j in range(5):
                if correct_index[i][j] != None:
                    indx1 = correct_index[i][j]
                    if M_C == True:  # MNIST dataset
                        axes[j, i].imshow((x_test[indx1].reshape(28,28)), cmap='gray')
                    else:  # CIFAR-10 dataset
                        #axes[j, i].imshow(x_test[indx1].reshape(32,32,3))  # used instead of following lines when using tensorflow
                        img = x_test[indx1].reshape(32, 32, 3)
                        img = img.reshape(32 * 32 * 3)
                        R = img[0:1024].reshape(32, 32)
                        G = img[1024:2048].reshape(32, 32)
                        B = img[2048:].reshape(32, 32)
                        img = np.dstack((R, G, B))
                        axes[j, i].imshow(img, interpolation='bicubic')
            for k in range(5):
                if wrong_index[i][k] != None:
                    indx2 = wrong_index[i][k]
                    if M_C == True:  # MNIST dataset
                        axes[k + 5, i].imshow((x_test[indx2].reshape(28,28)), cmap='gray')
                    else:  # CIFAR-10 dataset
                        #axes[k + 5, i].imshow(x_test[indx2].reshape(32,32,3))  # used instead of following lines when using tensorflow
                        img = x_test[indx2].reshape(32,32,3)
                        img=img.reshape(32*32*3)
                        R = img[0:1024].reshape(32, 32)
                        G = img[1024:2048].reshape(32, 32)
                        B = img[2048:].reshape(32, 32)
                        img = np.dstack((R, G, B))
                        axes[k + 5, i].imshow(img, interpolation='bicubic')
        if M_C == True:  # MNIST dataset
            fig.suptitle(
                'MNIST dataset \n \n1st 5 rows of correct predicted samples & 2nd 5 rows of wrong predicted samples',
                size=16)
        else:  # CIFAR-10 dataset
            fig.suptitle(
                'CIFAR-10 dataset \n \n1st 5 rows of correct predicted samples & 2nd 5 rows of wrong predicted samples',
                size=16)

        plt.show(block=True)

''''#test function for mnist and cifar10 data on fully connected model

import DL
def test(M_C):
    if M_C==True:
        Label_Train, Features_Train, Label_Test, Features_Test = DL.ReadFile("F:\\eural\\project2\\Deep-Learning-framework-main\\MNISTcsv")
        # %% training
        batch_size = 64
        num_epochs = 1
        num_classes = 10
        hidden_units = 300
        input_dimensions = (28, 28, 1)
        # change each label from scaler value to vector( 2 ---> [0, 0, 1, 0, 0, ...] ) (hot one)
        Label_Train_hotone = DL.hot_one(Label_Train, num_classes)

        model = DL.model()
        model.input_dims(input_dimensions)
        model.add('flatten')
        model.add('Relu', hidden_units)
        model.add('Linear', num_classes)
        optim = DL.optimizer(0.5, 0.5)
        loss_fn = DL.loss_Function('SoftmaxCrossEntropy')
        loss_fn.setLambda(0)
        model.fit(Features_Train, Label_Train_hotone,
                  batch_size, num_epochs, optim, loss_fn)
        predicted_labels = np.argmax(model.predict(Features_Test), axis=0)

    else:
        Label_Train, Features_Train, Label_Test, Features_Test = DL.ReadFile(
            "F:\\eural\\project2\\Deep-Learning-framework-main\\cifar-10-batches-py")
        # %% training
        batch_size = 128
        num_epochs = 3
        num_classes = 10
        hidden_units = 100
        input_dimensions = (32, 32, 3)
        # change each label from scaler value to vector( 2 ---> [0, 0, 1, 0, 0, ...] ) (hot one)
        Label_Train_hotone = DL.hot_one(Label_Train, num_classes)
        model = DL.model()
        model.input_dims(input_dimensions)
        model.add('flatten')
        model.add('Relu', hidden_units)
        model.add('Linear', num_classes)
        optim = DL.optimizer(0.001)
        loss_fn = DL.loss_Function('SoftmaxCrossEntropy')
        loss_fn.setLambda(0)
        model.fit(Features_Train, Label_Train_hotone,
                  batch_size, num_epochs, optim, loss_fn)
        z = model.predict(Features_Test)
        # print ("predicted labels dimensions",z.shape)
        predicted_labels = np.argmax(z, axis=0)

    return Label_Test, Features_Test, predicted_labels'''

'''#calling test
M_C = True
Label_Test, Features_Test, predicted_labels=test(M_C)
sample_visualization(M_C, Label_Test, Features_Test, predicted_labels)
M_C = False
Label_Test, Features_Test, predicted_labels=test(M_C)
sample_visualization(M_C, Label_Test, Features_Test, predicted_labels)'''

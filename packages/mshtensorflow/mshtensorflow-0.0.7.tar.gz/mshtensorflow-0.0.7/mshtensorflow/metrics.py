###################################
#metrics module
####################################
##by Kirollos Samir
####################################

import numpy as np
import pandas as pd



def absolute_fun (predicted_output,desired_output):
    absolute=0
    for (x , y) in zip(predicted_output , desired_output) :
        
        absolute=absolute+(abs(x-y))
    absolute=absolute/len(predicted_output)
    
    return absolute


#test for absolute_fun

#predicted_output=[1,2,3,4,5]
#desired_output=[5,4,3,2,1]
#absolute=absolute_fun(predicted_output,desired_output)
#print(absolute)



def accuracy (predicted_class,actual_class):
    count=0
    for (x, y) in zip(predicted_class,actual_class):
        
        if x==y :
            count=count+1
    
    acc=count/len(predicted_class)
    
    return acc


#test for accuracy
#predicted_class=[1,2,3,4,5]
#desired_class=[1,2,0,8,5]
#acc=accuracy(predicted_class,desired_class)
#print(acc)




def F1_score(predicted,actual):
    tp = 0
    fp = 0
    fn = 0
    i=0
    while i < len (predicted):
        if actual[i]==1 and predicted[i] ==1 :
            tp += 1
        if actual[i]==0 and predicted[i] ==1 :
            fp += 1
        if actual[i]==1 and predicted[i] ==0 :
            fn += 1
        i+=1

    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)

        return 2*((precision*recall)/(precision+recall))
    else:
        return 0


#test F1_score
#y_actual = [0,0,0,1,1,1,1]
#y_predicted   = [0,1,1,1,1,1,0]
#f1 = F1_score(y_predicted,y_actual)
#print (f1)

def confusion_matrix(predicted, actual):

    conf_arr = [[0, 0],
                [0, 0]]

    for i in range(len(predicted)):
        if int(actual[i]) == 0:
            if predicted[i] == 0 :
                conf_arr[0][0] = conf_arr[0][0] + 1
            elif predicted[i] == 1 :
                conf_arr[1][0] = conf_arr[1][0] + 1
        elif int(actual[i]) == 1:
            if predicted[i] == 0 :
                conf_arr[0][1] = conf_arr[0][1] + 1
            elif predicted[i] == 1 :
                conf_arr[1][1] = conf_arr[1][1] + 1
    return conf_arr

#test for confusion matrix
#y_actual = [1,1,0,0,1,0,0,1,0,1,1,1,0,1]
#y_predicted   = [0,1,1,0,1,0,0,0,0,0,0,0,1,1]
#con = confusion_matrix(y_predicted, y_actual )
#print(con)

def multiclass_confusion_matrix(predicted, actual):

    classes = np.unique(actual)
    matrix = np.zeros((len(classes), len(classes)))

    for i in range(len(classes)):
        for j in range(len(classes)):

            matrix[i, j] = np.sum((actual == classes[i]) & (predicted == classes[j]))

    return matrix

#test for multiclasses confusion matrix
#y_predicted   = [1,2,3,4,5,6,7]
#y_actual = [1,2,3,4,50,6,70]
#z=multiclass_confusion_matrix(y_predicted, y_actual)
#print(z)

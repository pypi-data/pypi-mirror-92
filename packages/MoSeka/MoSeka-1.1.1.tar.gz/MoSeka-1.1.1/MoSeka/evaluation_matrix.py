#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
#from Utils import  load_data
#from dense import  net
import numpy as np


# In[ ]:


from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix


# In[ ]:


y=   [2,3,4,5,1,0,0,1,2,3,4,5]
pred=[1,3,2,5,4,0,1,1,2,3,4,5]


# In[ ]:


def micro_F1_SCORE  (y , pred):
    # micro_F1_SCORE == recall == precision
    TP = 0
    FP=0
    for i in range (len(y)):
        if y[i] == pred[i]:
            TP+=1
        else:
            FP+=1
    return TP/(TP+FP)


# In[ ]:


def hot_form (y, labels_num ):

    #new_mat = [[0 for x in range(labels_num)] for y in range(len (y))]
    new_mat = np.empty((len (y), labels_num))
    for i in range (len (y)):
        for j in range (labels_num):
            if ( j == y[i] ):
                new_mat[i][j]= 1
            else :
                new_mat[i][j]=0
    return new_mat


# In[ ]:


def f1_score_labels (y_hot_form ,pred_hot_form):
        num_of_exam =y_hot_form.shape[0]
        labels_num =y_hot_form.shape[1]
        TP= [0]*labels_num     #[ [0] * labels_num for _ in range(num_of_exam)]
        FP=[0]*labels_num
        TN=[0]*labels_num
        FN=[0]*labels_num
        precision=[0]*labels_num
        recall=[0]*labels_num
        f1_score=[0]*labels_num
        for i in range (num_of_exam):
            for j in range (labels_num):
                if ( y_hot_form[i][j] == 1 and pred_hot_form[i][j]== 1):
                    TP[j]+= 1
                elif( y_hot_form[i][j] == 0 and pred_hot_form [i][j] == 0) :
                    TN[j]+= 1
                elif( y_hot_form[i][j] == 1 and pred_hot_form [i][j] == 0) :
                    FN[j]+= 1
                elif( y_hot_form[i][j] == 0 and pred_hot_form [i][j] == 1) :
                    FP[j]+= 1
        for i in range (labels_num):
            precision[i] = TP[i]/(TP[i]+FP[i])
            recall[i]=TP[i]/(TP[i]+FN[i])
            f1_score[i] =2 * (precision[i] * recall[i])/(precision[i] + recall[i])
        return f1_score, precision, recall
# In[ ]:





# In[ ]:




# In[ ]:


def macro_f1_score(f1_score_arr,precision_arr,recall_arr,labels_num):
    macro_f1_score=sum(f1_score_arr)/labels_num
    macro_precision=sum(precision_arr)/labels_num
    macro_recall=sum(recall_arr)/labels_num
    return macro_f1_score,macro_precision,macro_recall


# In[ ]:


def confusion_matrix(y_hot_form,pred_hot_form):
    num_of_exam =y_hot_form.shape[0]
    labels_num =y_hot_form.shape[1]
    confusion_matrix =[ [0] * labels_num for _ in range(labels_num)]
    for i in range (num_of_exam):
        for j in range(labels_num):
            if (y_hot_form[i][j]==1):
                col=j
                break
        for j in range(labels_num):
            if (pred_hot_form[i][j]==1):
                row=j
                break
        confusion_matrix[row][col]+=1
    return np.array(confusion_matrix)




# In[ ]:



def visualise_confusion_for_mnist(mat):
    df_cm = pd.DataFrame(mat, index = [i for i in "0123456789"],
                  columns = [i for i in "0123456789"])
    plt.figure(figsize = (10,7))
    sn.heatmap(df_cm, annot=True)
    #plt.matshow(df_cm)
# 
# <br>
# X_train,y_train,_=load_data("mnist_train.csv")<br>
# X_test,y_test,_ = load_data("mnist_test.csv")<br>
# # (X_train, y_train), (X_test, y_test) = mnist.load_data()<br>
# X_train, X_test = X_train.reshape(-1,X_train.shape[1]), X_test.reshape(-1,X_test.shape[1])<br>
# y_train, y_test = y_train.reshape(-1, 1), y_test.reshape(-1, 1)<br>
# # normalizing and scaling data<br>
# X_train, X_test = X_train.astype('float32')/255, X_test.astype('float32')/255<br>
# y_train, y_test=y_train.astype('int8'), y_test.astype('int8')<br>
# out = net(X_test)<br>
# preds_test = np.argmax(out, axis=1).reshape(-1, 1)<br>
# 

# In[ ]:
'''

micro_f1 = micro_F1_SCORE(y,pred)
print(micro_f1)
print("##############################################################################")
print("##############################################################################")


# In[ ]:


hot_form_y=hot_form(y,6)
hot_form_pred=hot_form(pred,6)
print(hot_form_y)
print(hot_form_pred)


# In[ ]:


print("##############################################################################")
print("##############################################################################")


# In[ ]:


f1_score_arr, precision_arr, recall_arr =f1_score_labels(hot_form_y ,hot_form_pred)


# In[ ]:


print(f1_score_arr)
print(precision_arr)
print(recall_arr)
print("##############################################################################")
print("##############################################################################")


# In[ ]:


macro_f1_score,macro_precision,macro_recall = macro_f1_score(f1_score_arr, precision_arr, recall_arr ,5)


# In[ ]:


print(macro_f1_score)
print(macro_precision)
print(macro_recall)
print("##############################################################################")
print("##############################################################################")


# In[ ]:


confusion_matrix=confusion_matrix(hot_form_y,hot_form_pred)
print(confusion_matrix)


# In[ ]:


print("##############################################################################")
print("##############################################################################")


# In[ ]:


array = [[33,2,0,0,0,0,0,0,0,1,3],
            [3,31,0,0,0,0,0,0,0,0,0],
            [0,4,41,0,0,0,0,0,0,0,1],
            [0,1,0,30,0,6,0,0,0,0,1],
            [0,0,0,0,38,10,0,0,0,0,0],
            [0,0,0,3,1,39,0,0,0,0,4],
            [0,2,2,0,4,1,31,0,0,0,2],
            [0,1,0,0,0,0,0,36,0,2,0],
            [0,0,0,0,0,0,1,5,37,5,1],
            [3,0,0,0,0,0,0,0,0,39,0],
            [0,0,0,0,0,0,0,0,0,0,38]]
df_cm = pd.DataFrame(array, index = [i for i in "ABCDEFGHIJK"],
                  columns = [i for i in "ABCDEFGHIJK"])
plt.figure(figsize = (10,7))
sn.heatmap(df_cm, annot=True)
#plt.matshow(df_cm)


# #################visualizing confusion matrix

# import some data to play with

# In[ ]:


iris = datasets.load_iris()
X = iris.data
y = iris.target
class_names = iris.target_names


# Split the data into a training set and a test set

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


# Run classifier, using a model that is too regularized (C too low) to see<br>
# the impact on the results

# In[ ]:


classifier = svm.SVC(kernel='linear', C=0.01).fit(X_train, y_train)


# In[ ]:


np.set_printoptions(precision=2)


# Plot non-normalized confusion matrix

# In[ ]:


titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(classifier, X_test, y_test,
                                 display_labels=class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)


# In[ ]:


plt.show()
'''

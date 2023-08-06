import numpy as np
import os
import pickle
from pathlib import Path
import requests
import tarfile 

def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')
 
        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                print('\r[{}{}]'.format('█' * done, '.' * (50-done)), end='')
            print('\ndone')



def download_and_read(dataset_name):
  if(dataset_name=='MNIST'):
    Path("./MNIST").mkdir(parents=True, exist_ok=True)
    download('https://pjreddie.com/media/files/mnist_train.csv', './MNIST/train.csv')
    download('https://pjreddie.com/media/files/mnist_test.csv', './MNIST/test.csv')
    return ReadFile("./MNIST")
  elif(dataset_name=='CIFAR'):
    Path("./CIFAR").mkdir(parents=True, exist_ok=True)
    download('https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz', './CIFAR/cifar10.tar.gz')
    path=os.path.abspath('./CIFAR/cifar10.tar.gz')
    file = tarfile.open(path)  
    file.extractall(path[:-15]) 
    file.close() 
    return ReadFile("./CIFAR/cifar-10-batches-py")


def ReadFile(path):
    print("Loading data...")
    path=path.replace("\\","/")
    path=path.replace('"','') 
    filenames = os.listdir(path)
    Features_Train = []
    Label_Train=[]
    if filenames[0][-4:]==".csv":               #MNIST dataset
        
        with open(path+"/train.csv", 'r', encoding='utf-8-sig') as f: 
            FullMatrix_Train = np.genfromtxt(f, dtype=float, delimiter=',')
        with open(path+"/test.csv", 'r', encoding='utf-8-sig') as f: 
                FullMatrix_Test = np.genfromtxt(f, dtype=float, delimiter=',')
                
        #  Shuffling data  
        np.random.shuffle(FullMatrix_Train)
        np.random.shuffle(FullMatrix_Test)
    
        Label_Train= FullMatrix_Train[:,0]  
        Temp= FullMatrix_Train[:,1:]
        Features_Train=Temp.transpose()
        
       
    
        Label_Test= FullMatrix_Test[:,0]
        Temp1= FullMatrix_Test[:,1:]
        Features_Test=Temp1.transpose()
        
        Features_Train = Features_Train.T.reshape(-1,28,28,1).transpose(0,3,1,2)
        Features_Test = Features_Test.T.reshape(-1,28,28,1).transpose(0,3,1,2)
        
        
        
        
      
    else :                                      #CIFAR dataset
        for file in filenames:
            if '_batch' in file:
                with open(path+'/'+file, 'rb') as fo:
                    dict = pickle.load(fo, encoding='bytes')
                    if'test' in file:
                        Label_Test=dict[b'labels']
                        Features_Test=dict[b'data']
                    else:
                       Label_Train.append(dict[b'labels'])
                       Features_Train.append(dict[b'data'])
                

        Label_Train=np.array(Label_Train)
        Features_Train=np.array(Features_Train)
        
        
        Label_Test=np.array(Label_Test)
        Features_Test=np.array(Features_Test)  
        Label_Train=Label_Train.reshape((-1,1))
        Features_Train=Features_Train.reshape((-1,3072))
        Features_Train=Features_Train.transpose()
        Features_Test=Features_Test.transpose()
        Features_Train = Features_Train.T.reshape(-1,3,32,32)
        Features_Test = Features_Test.T.reshape(-1,3,32,32)



    # Normalization
    Features_Train=Features_Train/255
    Features_Test=Features_Test/255
    
    print('data loaded')
    
    
    return Label_Train,Features_Train,Label_Test,Features_Test
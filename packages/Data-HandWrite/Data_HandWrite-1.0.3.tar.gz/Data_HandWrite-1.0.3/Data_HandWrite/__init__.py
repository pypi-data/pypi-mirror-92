import os
from PIL import Image
import numpy as np
import bz2#bz2file pypi
import zipfile
import requests
#data
#https://drive.google.com/file/d/1ZzSeuq-9ICZuFpPKM4H_gU8OGwpqKBAs/view?usp=sharing

#paint.exr
#https://drive.google.com/file/d/1EPrPilZ4XK80Cq4n9-ynO0yxZfxYTIhP/view?usp=sharing

def _save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
def _download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = _get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    _save_response_content(response, destination)

def dowloadPaintToolKit():
    _download_file_from_google_drive('1EPrPilZ4XK80Cq4n9-ynO0yxZfxYTIhP','paint.exe')
def dowloadPaintToolKitAndExecute():
    dowloadPaintToolKit()
    os.system('paint.exe')
def downloadData(folder=''):
    '''
    download train set and test set to 'folder'
    source==>
    https://drive.google.com/file/d/1ZzSeuq-9ICZuFpPKM4H_gU8OGwpqKBAs/view?usp=sharing
    '''
    #vedio==> https://drive.google.com/file/d/1076Ftdz8hxZkly-7QxYUR6kRJHSft-7s/view?usp=sharing
    #images==> https://drive.google.com/file/d/1zmpZY5D5vNwcxhNmTgBprisevixexA4I/view
    file_id = '1ZzSeuq-9ICZuFpPKM4H_gU8OGwpqKBAs'
    destination = '1.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination, mode='r') as myzip:
        for file in myzip.namelist():
            print("extract "+file)
            myzip.extract(file,folder)
    os.remove(destination)
    
def LoadImgFromFile(filename):
    '''
    return flatten image data whitch can predict directly
    '''
    x = np.asarray(Image.open(filename))
    x = x.flatten()/255
    return np.array([x])
    
def LoadDataFromWeb():
    '''
    combine downloadData() and LoadData()
    make data loading more easier
    '''
    downloadData()
    X_train,Y_train = LoadData('train')
    X_test,Y_test = LoadData('test')
    return X_train,Y_train,X_test,Y_test


def LoadData(sourceFolder):
    X = []
    Y = []
    for f in os.listdir(sourceFolder):
        try:
            y=f.split('_')[0]
            Y.append(int(y))
            x = np.asarray(Image.open(sourceFolder+'/'+f))
            X.append(x.flatten()/255) #將圖像陣列展開成 1 維
        except:pass
    X = np.array(X)
    Y = np.array(Y)
    return X,Y
                
def pickSample(X,Y,maxSize):
    dic={}
    newX = []
    newY = []
    for i in range(len(Y)):
        if  Y[i] in dic:
            if dic[Y[i]]<maxSize:
                dic[Y[i]]+=1
                newX.append(X[i])
                newY.append(Y[i])
        else:dic[Y[i]] = 0    
    return np.array(newX),np.array(newY)




    
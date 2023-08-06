import __init__
import numpy as np
#__init__.dowloadPaintToolKitAndExecute()
#X_train,Y_train,X_test,Y_test = __init__.LoadDataFromWeb()
#X_train,Y_train = __init__.pickSample(X_train,Y_train,60)

#__init__.downloadData()
X_train,Y_train = __init__.LoadData('train')
X_test,Y_test = __init__.LoadData('test')

#x = np.array([X_test[0]])
#x=np.reshape(X_test[0],(1,-1))# same effect as upper one
#print(np.shape(x))
#print(np.shape(x))
#print(np.shape(X_test))

from sklearn.svm import SVC
model = SVC(decision_function_shape='ovo',gamma=0.004,probability=True)
model.fit(X_train,Y_train)
result = model.predict(X_test)
print(model.score(X_test,Y_test))

for i in range(len(result)):
    print(Y_test[i],'==>',result[i])

x = __init__.LoadImgFromFile('test/1_100_0000.jpg')
result = model.predict_log_proba(x)
print(result)
result = model.predict(x)
print(result)
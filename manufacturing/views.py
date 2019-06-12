from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Manufacturing
from .serializers import ManufacturingSerializer

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras import backend as K
import numpy as np
import pickle
import os
import tensorflow as tf

from sklearn import svm, preprocessing, neighbors
from numpy import genfromtxt
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
import math
from sklearn.model_selection import RandomizedSearchCV
from keras import backend as K

@api_view(['GET'])
def training_oil_quality(request):

    try:
        # Convolutional Neural Network

        # Part 1 - Building the CNN

        # Initialising the CNN
        classifier = Sequential()

        # Step 1 - Convolution
        classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

        # Step 2 - Pooling
        classifier.add(MaxPooling2D(pool_size = (2, 2)))

        # Adding a second convolutional layer
        classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))

        # Adding a third convolutional layer
        classifier.add(Conv2D(128, (3, 3), activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))

        # Step 3 - Flattening
        classifier.add(Flatten())

        # Step 4 - Full connection
        classifier.add(Dense(units = 128, activation = 'relu'))
        classifier.add(Dense(units = 32, activation = 'relu'))

        classifier.add(Dense(units = 1, activation = 'sigmoid'))

        classifier.add(Dropout(rate=0.2))
        # Compiling the CNN
        classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

        # Part 2 - Fitting the CNN to the images

        train_datagen = ImageDataGenerator(rescale = 1./255,
                                        shear_range = 0.2,
                                        zoom_range = 0.2,
                                        horizontal_flip = True)

        test_datagen = ImageDataGenerator(rescale = 1./255)

        training_set = train_datagen.flow_from_directory('./manufacturing/dataset/training_oil_dataset',
                                                        target_size = (64, 64),
                                                        batch_size = 32,
                                                        class_mode = 'binary')

        test_set = test_datagen.flow_from_directory('./manufacturing/dataset/test_oil_dataset',
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'binary')

        classifier.fit_generator(training_set,
                                steps_per_epoch = 200,
                                epochs = 10,
                                validation_data = test_set,
                                validation_steps = 50)

        # ========= SALVANDO MODELO ===============
        filename = 'training_oil_savemodel.sav'
        file = open(filename, 'wb')
        pickle.dump(classifier, file)

        file.close()


        return Response(status=200)

    except Exception as e :
        print("error>>>>>")
        printe(e)
        return Response(status=400)

@api_view(['POST'])
def predict_oil_quality(request):
    try:
        K.clear_session()

        train_datagen = ImageDataGenerator(rescale = 1./255,
                                        shear_range = 0.2,
                                        zoom_range = 0.2,
                                        horizontal_flip = True)

        test_datagen = ImageDataGenerator(rescale = 1./255)

        training_set = train_datagen.flow_from_directory('./manufacturing/dataset/training_oil_dataset',
                                                        target_size = (64, 64),
                                                        batch_size = 32,
                                                        class_mode = 'binary')

        test_set = test_datagen.flow_from_directory('./manufacturing/dataset/test_oil_dataset',
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'binary')

        filename = 'training_oil_savemodel.sav'

        file = open(filename, 'rb')
        loaded_model = pickle.load(file)

        loss, metric = loaded_model.evaluate_generator(generator=test_set, steps=80)
        print("Acurácia:" + str(metric))

        # Comente essa linha para testes com o script 'predictImage.sh'
        # request_image = request.FILES['photo']

        # Descomente essa linha para testes com o script 'predictImage.sh'
        request_image = request.data['photo']

        test_image = image.load_img(request_image, target_size=(64, 64, 3))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)

        result = loaded_model.predict(test_image)
        # K.clear_session()

        print(training_set.class_indices)
        prediction = '?'

        if result[0][0] == 0:
            prediction = "BAD"
        elif result[0][0] == 1:
            prediction = "GOOD"
        elif result[0][0] == 2:
            prediction = "MEDIUM"
        else:
            prediction = "NO OIL"

        print("first single prediction is: ", prediction)

        file.close()

        K.clear_session()

        return Response(data=prediction, status=200)
    except Exception as e:
        print(e)
        return Response(status=400)

def random_search(request):
    try:
        train = genfromtxt('ml-prove/train.csv', delimiter=',')
        test = genfromtxt('ml-prove/test.csv', delimiter=',')
        validation = genfromtxt('ml-prove/validation.csv', delimiter=',')

        # Separando targets e features:

        validation_X = validation[:,0:-6]
        validation_y = validation[:,-6:]

        X_train = train[:,0:-6]
        y_train_1 = train[:,-6:-5]
        y_train_2 = train[:,-5:-4]
        y_train_3 = train[:,-4:-3]
        y_train_4 = train[:,-3:-2]
        y_train_5 = train[:,-2:-1]
        y_train_6 = train[:,-1:]

        X_test = test[:,0:-6]
        y_test_1 = test[:,-6:-5]
        y_test_2 = test[:,-5:-4]
        y_test_3 = test[:,-4:-3]
        y_test_4 = test[:,-3:-2]
        y_test_5 = test[:,-2:-1]
        y_test_6 = test[:,-1:]


        #-----------------RandomForestClassifier-----------------#

        # quantidade de combinações de hyperparametros = 4320 * 6

        params = {
            'bootstrap': [True, False],
            'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
            'max_features': ['auto', 'sqrt'],
            'min_samples_leaf': [1, 2, 4],
            'min_samples_split': [2, 5, 10],
            'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
        }

        clf = RandomForestClassifier()

        rfc = RandomizedSearchCV(
            estimator = clf,
            param_distributions = params,
            n_iter = 100,
            cv = 3,
            verbose=2,
            random_state=42,
            n_jobs = -1
        )

        dict_params = []
        accuracy_list = []
        time = []


        #--------------H1------------------#

        rfc.fit(X_train, y_train_1.ravel())

        dict_params.append(rfc.best_params_)

        score = rfc.score(X_test, y_test_1)

        accuracy = score
        accuracy_list.append(score)
        time.append(rfc.refit_time_)

        #--------------H2-----------------#

        rfc.fit(X_train, y_train_2.ravel())

        dict_params.append(rfc.best_params_)

        score = rfc.score(X_test, y_test_2)

        accuracy += score
        accuracy_list.append(score)
        time.append(rfc.refit_time_)

        #--------------H3-----------------#

        rfc.fit(X_train, y_train_3.ravel())

        dict_params.append(rfc.best_params_)

        score = rfc.score(X_test, y_test_3)

        accuracy += score
        accuracy_list.append(score)
        time.append(rfc.refit_time_)

        #--------------H4-----------------#

        rfc.fit(X_train, y_train_4.ravel())

        dict_params.append(rfc.best_params_)

        score = rfc.score(X_test, y_test_4)

        accuracy += score
        accuracy_list.append(score)
        time.append(rfc.refit_time_)

        #--------------H5-----------------#

        rfc.fit(X_train, y_train_5.ravel())

        dict_params.append(rfc.best_params_)

        score = rfc.score(X_test, y_test_5)

        accuracy += score
        accuracy_list.append(score)
        time.append(rfc.refit_time_)

        #-----------------H0-----------------#

        rfc.fit(X_train, y_train_6.ravel())

        dict_params.append(rfc.best_params_)

        score = rfc.score(X_test, y_test_6)

        accuracy += score
        accuracy_list.append(score)
        time.append(rfc.refit_time_)

        print("--------")
        print(accuracy/6.0)
        print("--------")
        print(dict_params)
        print("--------")
        print(accuracy_list)
        print("--------")
        print(time)
        print("--------")
        return Response(status=200)
    except Exception as e:
        return Response(status=400)



class ManufacturingCreateList(APIView):

    def get(self, request, format=None):
        fabrications = Manufacturing.objects.all()
        serializer = ManufacturingSerializer(fabrications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ManufacturingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

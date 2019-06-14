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
from sklearn.ensemble import AdaBoostClassifier
import math
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from keras import backend as K
import pandas as pd

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
        classifier.add(Conv2D(128, (3, 3), activation = 'tanh'))
        classifier.add(MaxPooling2D(pool_size = (2, 2)))

        # Step 3 - Flattening
        classifier.add(Flatten())

        # Step 4 - Full connection
        classifier.add(Dense(units = 128, activation = 'relu'))
        classifier.add(Dense(units = 32, activation = 'relu'))

        classifier.add(Dense(units = 3, activation = 'sigmoid'))

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
                                                        class_mode = 'categorical')

        test_set = test_datagen.flow_from_directory('./manufacturing/dataset/test_oil_dataset',
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'categorical')

        classifier.fit_generator(training_set,
                                steps_per_epoch = 100,
                                epochs = 10,
                                validation_data = test_set,
                                validation_steps = 10)

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
                                                        class_mode = 'categorical')

        test_set = test_datagen.flow_from_directory('./manufacturing/dataset/test_oil_dataset',
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'categorical')

        filename = 'training_oil_savemodel.sav'

        file = open(filename, 'rb')
        loaded_model = pickle.load(file)

        loss, metric = loaded_model.evaluate_generator(generator=test_set, steps=80)
        print("Acurácia:" + str(metric))

        # Comente essa linha para testes com o script 'predictImage.sh'
        request_image = request.FILES['photo']

        # Descomente essa linha para testes com o script 'predictImage.sh'
        # request_image = request.data['photo']

        test_image = image.load_img(request_image, target_size=(64, 64, 3))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)

        result = loaded_model.predict(test_image)

        print(training_set.class_indices)
        prediction = '?'

        max_value = result[0]
        max_indice = 0

        # for i in range(len(result)):
        #     if result[i] > max:
        #         max_value = result[i]
        #         max_indice = 0

        if max_indice == 0:
            prediction = "BAD"
        elif max_indice == 1:
            prediction = "GOOD"
        else: 
            prediction = "NO OIL"
 

        print("first single prediction is: ", prediction)

        file.close()

        K.clear_session()

        return Response(data=prediction, status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


@api_view(['GET'])
def training_ph(request):
    try:
        fabrications = Manufacturing.objects.all()
        serializer = ManufacturingSerializer(fabrications, many=True)

        manufacturing_list = pd.DataFrame(serializer.data)

        del manufacturing_list['id']
        del manufacturing_list['oil_image']
        del manufacturing_list['expected_ph']
        del manufacturing_list['end_of_manufacture']
        del manufacturing_list['start_of_manufacture']


        oil_quality_list = [ 2 if x == 'GOOD' else 1 if x ==  'MEDIUM' else 0 for x in manufacturing_list['oil_quality']]

        manufacturing_list['oil_quality'] = oil_quality_list

        y = manufacturing_list['actual_ph']

        del manufacturing_list['actual_ph']

        X = manufacturing_list

        gsc = GridSearchCV(
            estimator=RandomForestRegressor(),
            param_grid={
                'max_depth': range(3,7),
                'n_estimators': (10, 50, 100, 1000),
            },
            cv=5,
            scoring='neg_mean_squared_error',
            verbose=0,
            n_jobs=-1
        )

        grid_result = gsc.fit(X, y)
        best_params = grid_result.best_params_

        rfr = RandomForestRegressor(
            max_depth=best_params["max_depth"],
            n_estimators=best_params["n_estimators"],
            random_state=False,
            verbose=False
        )

        rfr.fit(X, y)

        filename = 'training_ph_savemodel.sav'
        file = open(filename, 'wb')
        pickle.dump(rfr, file)

        file.close()

        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


@api_view(['POST'])
def predict_ph(request):
    try:
        filename = 'training_ph_savemodel.sav'

        file = open(filename, 'rb')
        loaded_model = pickle.load(file)

        result = loaded_model.predict([request.data])

        return Response(status=200)
    except Exception as e:
        print(e)
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

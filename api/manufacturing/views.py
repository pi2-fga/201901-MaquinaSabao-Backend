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
import numpy as np
import pickle

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
                                steps_per_epoch = len(Manufacturing.objects.all()),
                                epochs = 10,
                                validation_data = test_set,
                                validation_steps = 1)

        # ========= SALVANDO MODELO ===============
        filename = './training_oil_savemodel.sav'
        pickle.dump(classifier, open(filename, 'wb'))

        return Response(status=200)
    
    except Exception as e :
        return Response(status=400)

def predict(request):
    pass

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

from django.shortcuts import render
import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from .apps import ApiConfig
from sklearn.impute import SimpleImputer


# Create your views here.
class PremiumPrediction(APIView):
    def post(self, request):
        data = request.data
        
        # Load the trained model
        model = ApiConfig.model

        # Preprocess the input data
        sex_map = {'female': 0, 'male': 1}
        smoker_map = {'yes': 1, 'no': 0}
        region_map = {'southwest': 1, 'southeast': 2, 'northwest': 3, 'northeast': 4}

        sex = data.get('sex')
        smoker = data.get('smoker')
        region = data.get('region')

        sex_encoded = sex_map.get(sex.lower())
        smoker_encoded = smoker_map.get(smoker.lower())
        region_encoded = region_map.get(region.lower())

        # Perform predictions
        age = int(data.get('age'))
        bmi = float(data.get('bmi'))
        children = int(data.get('children'))

        features = {
            'age': [age],
            'sex': [sex_encoded],
            'bmi': [bmi],
            'children': [children],
            'smoker': [smoker_encoded],
            'region': [region_encoded]
        }

        X = pd.DataFrame(features)

        # Create an instance of SimpleImputer to replace missing values with the mean
        imputer = SimpleImputer(strategy='mean')

        # Fit the imputer on your training data and transform the input data
        X = imputer.fit_transform(X)

        expenses = model.predict(X)

        # Prepare the expenses
        expenses_data = {'expenses': expenses.tolist()}

        return Response(expenses_data)

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler


app = Flask(__name__)

#load dataset
data = pd.read_csv('Laptop_price.csv')
data['RAM_Size'] = data['RAM_Size'].astype('O') # change data type of Ram size as object

num_cols = data.select_dtypes(include=['number']).columns.tolist()
cat_cols = ['Brand', 'RAM_Size']

cols = data.drop('Price', axis=1).columns

# take unique values for categoricl columns
brand_values = data['Brand'].unique()
ram_values = data['RAM_Size'].unique()

# load pkl file
model = joblib.load('laptop_price_rfr.pkl')
scaler = joblib.load('standard_scaler.pkl')
encoder = joblib.load('OneHotEncoder.pkl')



@app.route('/')
def home():
    return render_template('index.html', brand_values = brand_values, ram_values=ram_values)

@app.route('/predict', methods = ['POST'])
def predict():
    # get data from html form
    brand = request.form.get('brand')
    ram = request.form.get('ram')
    processor_speed = float(request.form.get('processor_speed'))
    storage = int(request.form.get('storage'))
    screen = float(request.form.get('screen'))
    weight = float(request.form.get('weight'))

    inputs = [brand, processor_speed, ram, storage, screen, weight] # list of input

    input_df = pd.DataFrame(input, columns= cols) # dataframe by using input data list
    # Extract features from the new data
    input_new = input_df[num_cols + cat_cols]

    input_scaled = scaler.transform(input_new[num_cols])
    input_encoded = encoder.transform(input_new[cat_cols]).toarray()
    
    input_preprocessed = np.concatenate([input_scaled, input_encoded], axis=1)

    # Make predictions using the pre-trained model
    prediction = model.predict(input_preprocessed) # predict the output

    return render_template('index.html', price = prediction[0], brand_values = brand_values, ram_values=ram_values, processor_speed = processor_speed,
                           storage = storage, screen = screen, weight= weight)




if __name__ == '__main__':
    app.run( debug=True)
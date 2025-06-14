import flask 
import pandas as pd 
import pickle
import pyttsx3 

model=pickle.load(open('RandomForest.pkl','rb'))

app = flask.Flask(__name__, template_folder='templates')


@app.route("/", methods=['GET', 'POST'])
def predict():
    if flask.request.method == 'GET':
        return flask.render_template('predict.html')

    if flask.request.method == 'POST':
        Nitrogen = flask.request.form['Nitrogen']
        Phosphorus = flask.request.form['Phosphorus']
        Potassium = flask.request.form['Potassium']
        Temperature = flask.request.form['Temperature']
        Humidity = flask.request.form['Humidity']
        Ph = flask.request.form['Ph']
        Rainfall = flask.request.form['Rainfall']

        #input_variables = pd.DataFrame([[Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]], columns=['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Ph', 'Rainfall'],
         #                              dtype='float',
          #                             index=['input'])
        input_variables = pd.DataFrame([[Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]],
                               columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'],
                               dtype='float')

        predictions = model.predict(input_variables)
        print(predictions)
        engine = pyttsx3.init(driverName='sapi5')   # Defining the speech rate, type of voice etc.
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-20)
        engine.setProperty('voice',voices[0].id)


        def speak(audio):  # Defining a speak function. We can call this function when we want to make our program to speak something.
            engine.say(audio) 
            engine.runAndWait()
        #speak("The best crop that you can grow is  " + predictions)
        speak("The best crop that you can grow is " + str(predictions[0]))

        #return flask.render_template('predict.html', original_input={'Nitrogen': Nitrogen, 'Phosphorus': Phosphorus, 'Potassium': Potassium, 'Temperature': Temperature, 'Humidity': Humidity, 'Ph': Ph, 'Rainfall': Rainfall},
                                     #result=predictions)
        return flask.render_template('predict.html', original_input={'Nitrogen': Nitrogen, 'Phosphorus': Phosphorus, 'Potassium': Potassium, 'Temperature': Temperature, 'Humidity': Humidity, 'Ph': Ph, 'Rainfall': Rainfall},
                                     result=predictions[0])


if __name__ == '__main__':
    app.run(debug=True)
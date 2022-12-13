from flask import Flask, render_template, request
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os

filepath = '/home/ubuntu/project-doan/GoogLeNet_tomatoclassification.h5'
model = load_model(filepath)
model.load_weights(filepath)

print(model)
def pred_tomato_dieas(tomato_plant):
  test_image = load_img(tomato_plant, target_size = (224, 224))  
  print("Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 
  test_image = np.expand_dims(test_image, axis = 0)
  
  result = model.predict(test_image) 
  print('Raw result = ', result)
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      return "Bac La", 'Tomato-Early-Blight.html'   
  elif pred==1:
      return "Hoan toan manh khoe", 'Tomato-Healthy.html'   
  elif pred==2:
      return "Khuon la", 'Tomato-Leaf-Mold.html'   
  elif pred==3:
      return "Moc suong", 'Tomato-Late-blight.html'
  elif pred==4:
      return "Ve nhen", 'Tomato-Two-spotted-spider-mite.html'  
  elif pred==5:
      return "Vi rut kham ca chua", 'Tomato-Tomato-mosaic-virus.html' 
  elif pred==6:
      return "Vi rut xoan vang la", 'Tomato-Tomato-Yellow-Leaf-Curl-Virus.html'  
  elif pred==7:
      return "Dom la Septoria", 'Tomato-Septoria-leaf-spot.html'  
  elif pred==8:
      return "Dom trang", 'Tomato-Target-Spot.html' 
  elif pred==9:
      return "Dom la", 'Tomato-Bacteria-Spot.html' 


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')

@app.route("/cd", methods=['GET','POST'])
def cd():
        return render_template('cd.html')

@app.route("/book", methods=['GET', 'POST'])
def book():
        return render_template('book.html')

@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] 
        filename = file.filename        
        
        file_path = os.path.join('/home/ubuntu/project-doan/static/upload/', filename)
        file.save(file_path)

        pred, output_page = pred_tomato_dieas(tomato_plant=file_path)     
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 
    # app.run(debug=True)
    

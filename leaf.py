from flask import Flask, render_template, request
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os

filepath = 'D:/Plant-Leaf-Disease-Prediction/GoogLeNet_tomatoclassification.h5'
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
      return "Bạc lá", 'Tomato-Early_Blight.html'   
  elif pred==1:
      return "Hoàn toàn mạnh khỏe", 'Tomato-Healthy.html'   
  elif pred==2:
      return "Khuôn lá", 'Tomato - Leaf_Mold.html'   
  elif pred==3:
      return "Mốc sương", 'Tomato - Late_blight.html'
  elif pred==4:
      return "Ve nhện", 'Tomato - Two-spotted_spider_mite.html'  
  elif pred==5:
      return "Vi rút khảm cà chua", 'Tomato - Tomato_mosaic_virus.html' 
  elif pred==6:
      return "Vi rút xoăn vàng lá", 'Tomato - Tomato_Yellow_Leaf_Curl_Virus.html'  
  elif pred==7:
      return "Đốm lá Septoria", 'Tomato - Septoria_leaf_spot.html'  
  elif pred==8:
      return "Đốm trắng", 'Tomato - Target_Spot.html' 
  elif pred==9:
      return "Đốm lá", 'Tomato-Bacteria Spot.html' 


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
        
        file_path = os.path.join('D:/Plant-Leaf-Disease-Prediction/static/upload/', filename)
        file.save(file_path)

        pred, output_page = pred_tomato_dieas(tomato_plant=file_path)     
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 
    # app.run(debug=True)
    

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__,static_url_path='/foodapp/',static_folder='static',template_folder='template')


@app.route('/foodapp')
def home():
    return render_template('index.html')

@app.route('/foodapp/predict',methods=['GET','POST'])
def predict():
    recipe=pd.read_csv('pre-processing/RAW_recipes.csv')
    df=pd.DataFrame(recipe)
    food=request.form['foodtype']
    mint=request.form['Mintime']
    maxt=request.form['Maxtime']
    mcal=request.form['mincal']
    macal=request.form['maxcal']
    mint=int(mint)
    maxt=int(maxt)
    mcal=int(mcal)
    macal=int(macal)
    nam=[]
    mins=[]
    calor=[]
    setp=[]
    des=[]
    ind=[]
    for i in df.index:
        if(df['food type'][i]==food and mint<df['minutes'][i]<maxt and mcal<df['cal'][i]<macal):
            nam.append(df['name'][i])
            mins.append(df['minutes'][i])
            calor.append(df['cal'][i])
            setp.append(df['steps'][i])
            des.append(df['description'][i])
            ind.append(df['ingredients'][i])
        
    if not nam:
        # If there are no matching recipes, handle it here (e.g., display a message)
        return render_template('no_result.html')

    list_of_tuples = list(zip(nam, mins,calor,setp,des,ind)) 
    df3 = pd.DataFrame(list_of_tuples, columns = ['Name', 'Minutes','Calories','Steps','Description','Ingridients']) 
    
    if df3.empty:
        # Handle the case where there are no matching recipes
        return render_template('no_result.html')
    
    return render_template('ouput.html',  tables=[df3.sample(n=10).to_html(classes='data')], titles=df3.columns.values)
    
if __name__ == "__main__":
    app.run(debug=False,port=5001)

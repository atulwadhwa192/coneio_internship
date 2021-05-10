from flask import Flask, redirect, url_for, request, send_file, render_template,Response

import glob

import os
import pandas as pd
# import numpy as np


import re

app = Flask(__name__)


@app.route("/")
def index():
   return render_template('new.html')

@app.route('/table',methods = ['POST', 'GET'])
def new():
    #print("entered 0")
    if request.method == 'POST':
        global df
        if request.files:
            file= request.files['csv']
            description = request.form['description']
            save_loc = r'//home//rohit//Desktop//Coneio//tagging_utility//'
            out_loc = r'//home//rohit//Desktop//Coneio//tagging_utility//outputs'
            # save_loc = r'C:\Users\\Administrator\Documents\update_description\static\file\uploads\\'
            # out_loc =  r'C:\Users\\Administrator\Documents\update_description\static\file\output\\'
            # file.save(save_loc+file.filename)
        fname= file.filename
        if fname[-3:]=='csv':
            df1 = pd.read_csv(file)
        elif fname[-4:]=='xlsx':
            df1 = pd.read_excel(file)
        else :
            return render_template("new.html")
        # df1 =  process1(df[["hsn","description"]])
        # df = df1[["hsn","updated_description"]]
        # df.columns= ["hsn","description"]
        # df= pd.read_excel(save_loc+file.filename)
        # t = [""]*df.shape[0]
        # print(t)
        df = pd.DataFrame()
        try:
            df['hsn'] = df1['hsn'].values
        except:
            df['hsn'] = df1['HSN_Code'].values
        
        try:
            df['description'] = df1['description'].values
        except:
            df['description'] = df1['Description'].values

        df["user_description"] = [description]*df.shape[0]
        # df['tags'] = t
        
        # df =  tagging(save_loc+file.filename, [description]).get_final_result()
        # df.to_excel(out_loc+'final.xlsx', index= False)
        # df1.to_excel(out_loc+'Quantity.xlsx', index=False)
        return render_template("table.html",df = df ) 
    else:
        return render_template("new.html")

@app.route('/labels',methods = ['POST', 'GET'])
def table():
    #print("entered 0")
    labels = []
    if request.method == 'POST':
        for i in range(df.shape[0]):
            if request.form.get(df.iloc[i][1]) == 'True':
                labels.append(1)
            else:
                labels.append(0)
        df['labels'] = labels
        return render_template('labels.html', df = df)
    else:
        return render_template("table.html",df = df )

# @app.route('/labels',methods = ['POST', 'GET'])
# def label():
#     #print("entered 0")
    
#     if request.method == 'POST':
        
#         return render_template('new.html')
#     else:
#         return render_template("label.html")


# Download API
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    x=filename
    out_loc =  out_loc =  r'C:\Users\dell\Downloads'
    file_path = out_loc + filename
    return Response(
       df.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       f"attachment; filename={x}.csv"})
    # return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == '__main__':
   
   app.run(debug = True)      
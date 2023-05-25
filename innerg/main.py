from flask import Flask, request
import pandas as pd
#from sql1111 import * 
import sqlite3
import json

app = Flask(__name__)



@app.route("/data")
def index():
    number=int(request.args.get('well'))
    df = pd.read_excel("20210309_2020_1.xls")
    new_dict=df.to_dict()
    sumb=0
    sumo=0
    sumg=0
    print(type(number))
    for sub in new_dict:
        for i in range(10626):
            if(number==new_dict[sub][i]):
                #sum=sum+int(new_dict['OIL'][i])
                print (sub)
                sumo=sumo+new_dict['OIL'][i]
                sumg=sumg+new_dict['GAS'][i]
                sumb=sumb+new_dict['BRINE'][i]
            
    print(sumg,sumo,sumb)
    well={ }
    conn=sqlite3.connect('innerg.db')
    c=conn.cursor()
    query="INSERT INTO Annual VALUES ({api},{oil},{gas},{brine})".format(api=number,oil=sumo,gas=sumg,brine=sumb)
    c.execute(query)
    conn.commit()
    query1="select oli from Annual where well={n}".format(n=number)
    res=c.execute(query1)
    res=res.fetchone()[0]
    well['oil']=res
    query1="select gas from Annual where well={n}".format(n=number)
    res=c.execute(query1)
    res=res.fetchone()[0]
    well['gas']=res
    query1="select brine from Annual where well={n}".format(n=number)
    res=c.execute(query1)
    res=res.fetchone()[0]
    
    well['brine']=res
    conn.close()
    res = json.dumps(well, sort_keys=True, indent=4)
    #response = str(well)
    return res
if __name__ == '__main__':
    app.run(debug=False, port=8080)
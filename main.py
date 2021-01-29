from flask import Flask, request, jsonify
import pyodbc as db
from requests import get

app = Flask(__name__)

try:
    strCnn = 'Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=northwind;Trusted_Connection=yes;'
    conn = db.connect(strCnn)
    cursor = conn.cursor()
except db.Error as err:
    sqlState = err.args[1]
    print (sqlState)
  
#GET - view all data
@app.route('/Shippers/', methods=['GET'])
def getAll():
    return getdata('Shippers')

#GET - view data for given CompanyName
@app.route('/Shippers/<CompanyName>/', methods=['GET'])
def get_(CompanyName):
    sql = "SELECT ShipperID, CompanyName, Phone FROM [dbo].[Shippers] "
    sql += "WHERE CompanyName = '" + CompanyName + "'"
    result = cursor.execute(sql)
    res = {'Shippers':[dict(zip([key[0] 
        for key in cursor.description], row)) for row in result]}
    return  jsonify(res)

#DELETE - delete entry by CompanyName
@app.route('/Shippers/<CompanyName>/', methods=['DELETE'])
def delete_(CompanyName):
    sql = "DELETE FROM [dbo].[Shippers] "
    sql += "WHERE CompanyName = '" + CompanyName + "'"
    cursor.execute(sql)
    return getdata('Shippers Updated')

#POST - Insert new CompanyName and Phone
@app.route('/Shippers/<CompanyName>/<Phone>/', methods=['POST'])
def post_(CompanyName, Phone):
    sql = "INSERT INTO [dbo].[Shippers] (CompanyName, Phone) "
    sql += "VALUES ('" + CompanyName + "','" + Phone + "')"
    cursor.execute(sql)
    return getdata('Shippers Updated')

#PUT - update CompanyName and Phone for given ShipperID
@app.route('/Shippers/<CompanyName>/<Phone>/<ShipperID>/', methods=['PUT'])
def put_(CompanyName, Phone, ShipperID):
    sql = "UPDATE [dbo].[Shippers] SET CompanyName = '" + CompanyName + "', "
    sql += "Phone = '" + Phone + "' WHERE ShipperID = '" + ShipperID + "'"
    cursor.execute(sql)
    return getdata('Shippers Updated')

def getdata(tag):
    sql = "SELECT ShipperID, CompanyName, Phone FROM [dbo].[Shippers]"  
    result = cursor.execute(sql)
    res = {tag:[dict(zip([key[0] 
        for key in cursor.description], row)) for row in result]}
    return jsonify(res)  


#Response Test
def ResponseTest():
    endPoint = ('http://127.0.0.1:8080/Shippers/')
    response = get(endPoint)
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
    else:
        print(response.json())


if __name__ == '__main__':
    #Debug mode on Port 8080
    app.run(debug=True, port='8080')





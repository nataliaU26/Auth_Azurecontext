from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS

app = Flask(__name__)
#CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}}, supports_credentials=True)
#Azure dataset
#Example Access credentials for login (username:2, password: pass123)
CORS(app, supports_credentials=True)
db_config = {
    'host': 'mentordb.mysql.database.azure.com',
    'user': 'mentordbuser',
    'password': 'm3nt0r2024%',
    'db': 'mentordb1',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'ssl': {'ca': 'DigiCertGlobalRootCA.crt.pem'}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    auth_id = data.get('user')
    Password = data.get('password')

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "SELECT id, email, Access_token, Access_type FROM users WHERE auth_id = %s AND Password = %s"
            cursor.execute(sql, (auth_id, Password))
            result = cursor.fetchone()
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "Unauthorized"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

"""
Local dataset

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}}, supports_credentials=True)

df = pd.read_csv('C:/Users/natal/Desktop/prueba2-server/Userdataset.csv', delimiter=';')

print(df.columns)
@app.route('/data', methods=['GET'])
def get_data():
    column = request.args.get('column')
    value = request.args.get('value')
    
    if column in df.columns and value:
        filtered_data = df[df[column] == value].to_dict(orient='records')
    else:
        filtered_data = df.to_dict(orient='records')
    
    return jsonify(filtered_data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    
   
    user_record = df[(df['iduser'] == user) & (df['Password'] == password)]

    if not user_record.empty:
        accessToken = user_record.iloc[0]['accessToken']
        userType = user_record.iloc[0]['userType']

      
        return jsonify({
            "user": user,  
            "password": password,  
            "accessToken": accessToken,
            "roles": [userType] 
        }), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True)"""
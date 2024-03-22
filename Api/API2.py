from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
import logging
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
#CORS(app, resources={r"/login": {"origins": "http://localhost:3001"}}, supports_credentials=True)
#http://127.0.0.1:8000/
CORS(app, supports_credentials=True) 

asgi_app = WsgiToAsgi(app)
db_config = {
    'host': 'mentordb.mysql.database.azure.com',
    'user': 'mentordbuser',
    'password': 'm3nt0r2024%',
    'db': 'mentordb1',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'ssl': {'ca': 'DigiCertGlobalRootCA.crt.pem'}
}

#Home display        
@app.route('/')
def home():
    return 'MentorIA statistics DEPLOY'

#Error Managment
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error interno,por favor intente más tarde: {str(e)}") 
    return jsonify(error="Ocurrió un error interno, por favor intente más tarde."), 500

#--------------------------------------- CONSULT DEFINITION -----------------------------------------------
def get_db_connection():
    return pymysql.connect(**db_config)

class BaseEndpoint_client:
    @staticmethod
    def verify_permission(user_id):
        _, type_id = rol_definition(user_id)
        if type_id == 3:
            return True
        else:
            return False
        
    @staticmethod  
    def execute_query(query, args=(), one=False):
        with get_db_connection().cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchone() if one else cursor.fetchall()

class BaseEndpoint_user:
    @staticmethod
    def verify_permission(user_id):
        _, type_id = rol_definition(user_id)
        if type_id == 2:
            return True
        else:
            return False
        
    @staticmethod
    def execute_query(query, args=(), one=False):
        with get_db_connection().cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchone() if one else cursor.fetchall()
        
class BaseEndpoint_Admin:
    @staticmethod
    def verify_permission(user_id):
        _, type_id = rol_definition(user_id)
        if type_id == 1:
            return True
        else:
            return False
        
    @staticmethod
    def execute_query(query, args=(), one=False):
        with get_db_connection().cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchone() if one else cursor.fetchall()
        
#---------------------------------------------- MAIN DATA OBTAIN -------------------------------------------------------------------------------------------------
def rol_definition(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
                SELECT company_id, type_id 
                FROM users 
                WHERE id = %s;
            """
            cursor.execute(query, (id,))
            user_info = cursor.fetchone()
            if user_info:
                return user_info['company_id'], user_info['type_id']
            else:
                return None, None
            
    except Exception as e:
        print(f"Error al obtener la información del usuario: {e}")
        return None, None
    finally:
        if 'connection' in locals():
            connection.close()
#----------------------------------------------------------------------------- GRAHPS
# Client dashboard
class ClientDashboard(BaseEndpoint_client):
        @staticmethod
        @app.route('/messages_user_by_day/<int:id>', methods=['GET'])
        def messages_user_by_day(id):
            if not ClientDashboard.verify_permission(id):
                return jsonify({"message": "Usuario no autorizado"}), 403
            company_id, _ = rol_definition(id)
            if not company_id:
                return jsonify({"message": "Campos incompletos"}), 404
            query = """
                SELECT 
                u.id AS user_id,
                u.name AS username,
                DATE(m.timestamp) AS date,
                COUNT(m.id) AS message_count,
                COUNT(m.sessionid) AS Conversaciones
                FROM messages m
                INNER JOIN users u ON m.user_id = u.id
                WHERE u.company_id = %s
                GROUP BY user_id, date
                ORDER BY date ASC, username ASC"""
            result = ClientDashboard.execute_query(query, (company_id,))
            return jsonify(result) if result else jsonify({"message": "No data found"}), 404

        @staticmethod
        @app.route('/total_users_by_company/<int:id>', methods=['GET'])
        def total_users_by_company(id): 
                if not ClientDashboard.verify_permission(id):
                    return jsonify({"message": "Usuario no autorizado"}), 403
                company_id, _ = rol_definition(id)
                if not company_id:
                    return jsonify({"message": "Campos incompletos"}), 404
                query = """
                    SELECT
                    c.id, 
                    COUNT(u.id) AS total_users
                    FROM
                    `users` u
                    JOIN
                    `companies` c ON u.company_id = c.id
                    WHERE
                    c.id = %s
                    GROUP BY
                    c.companyname;"""
                result = ClientDashboard.execute_query(query, (company_id,))
                return jsonify(result) if result else jsonify({"message": "No data found"}), 404
        
        @staticmethod
        @app.route('/daily_conversations_by_company/<int:id>', methods=['GET'])
        def get_daily_conversations_by_company_id(id):
                if not ClientDashboard.verify_permission(id):
                    return jsonify({"message": "Usuario no autorizado"}), 403
                company_id, _ = rol_definition(id)
                if not company_id:
                    return jsonify({"message": "Campos incompletos"}), 404
                query = """
                    SELECT 
                        u.company_id, 
                        DATE(m.timestamp) AS date, 
                        COUNT(DISTINCT m.sessionid) AS total_conversations
                        FROM 
                        messages m
                        JOIN 
                        users u ON m.user_id = u.id
                        WHERE 
                        u.company_id = %s
                        GROUP BY 
                        u.company_id, date
                        ORDER BY 
                        date ASC;"""
                result = ClientDashboard.execute_query(query, (company_id,))
                return jsonify(result) if result else jsonify({"message": "No data found"}), 404
        
        @staticmethod
        @app.route('/conversations_by_month_company/<int:id>', methods=['GET'])
        def get_conversations_by_month_company_id(id):
                if not ClientDashboard.verify_permission(id):
                    return jsonify({"message": "Usuario no autorizado"}), 403
                company_id, _ = rol_definition(id)
                if not company_id:
                    return jsonify({"message": "Campos incompletos"}), 404
                query = """
                    SELECT 
                    u.company_id, 
                    YEAR(m.timestamp) AS year, 
                    MONTH(m.timestamp) AS month, 
                    COUNT(DISTINCT m.sessionid) AS total_conversations
                    FROM 
                    messages m
                    JOIN 
                    users u ON m.user_id = u.id
                    WHERE
                    u.id = %s
                    GROUP BY 
                    u.company_id, year, month
                    ORDER BY 
                    u.company_id, year, month;"""
                result = ClientDashboard.execute_query(query, (company_id,))
                return jsonify(result) if result else jsonify({"message": "No data found"}), 404
        
        @staticmethod
        @app.route('/Total_conversations_by_company/<int:id>', methods=['GET'])
        def get_Total_conversations_by_company(id):
                if not ClientDashboard.verify_permission(id):
                    return jsonify({"message": "Usuario no autorizado"}), 403
                company_id, _ = rol_definition(id)
                if not company_id:
                    return jsonify({"message": "Campos incompletos"}), 404
                query = """
                    SELECT 
                    u.company_id, 
                    COUNT(DISTINCT m.sessionid) AS total_conversations
                    FROM 
                    messages m
                    JOIN 
                    users u ON m.user_id = u.id
                    WHERE
                    u.id = %s
                    GROUP BY 
                    u.company_id
                    ORDER BY 
                    u.company_id;"""
                result = ClientDashboard.execute_query(query, (company_id,))
                return jsonify(result) if result else jsonify({"message": "No data found"}), 404
#Admin rol           
class AdminDashboard(BaseEndpoint_Admin):    
        @staticmethod
        @app.route('/total_users_for_company/<int:id>', methods=['GET'])
        def total_users_for_company(id):
            if not AdminDashboard.verify_permission(id):
                return jsonify({"message": "Usuario no autorizado"}), 403
            company_id, _ = rol_definition(id)
            if not company_id:
                return jsonify({"message": "Campos incompletos"}), 404
            query = """
                SELECT 
                c.companyname AS NombreCompania,
                u.company_id, 
                COUNT(DISTINCT u.id) AS TotalUsuarios
                FROM 
                users u
                LEFT JOIN 
                messages m ON u.id = m.user_id
                INNER JOIN 
                companies c ON u.company_id = c.id
                GROUP BY 
                u.company_id, c.companyname ;"""
            result = AdminDashboard.execute_query(query)
            return jsonify(result) if result else jsonify({"message": "No data found"}), 404  
        
        @staticmethod
        @app.route('/total_clients/<int:id>', methods=['GET'])
        def total_clients(id):
            if not AdminDashboard.verify_permission(id):
                return jsonify({"message": "Usuario no autorizado"}), 403
            company_id, _ = rol_definition(id)
            if not company_id:
                return jsonify({"message": "Campos incompletos"}), 404
            query = """
              SELECT COUNT(DISTINCT id) AS TotalClientes
              FROM `companies`
            """
            result = AdminDashboard.execute_query(query)
            return jsonify(result) if result else jsonify({"message": "No data found"}), 404 
        
        @staticmethod
        @app.route('/total_Messages/<int:id>', methods=['GET'])
        def total_Messages(id):
            if not AdminDashboard.verify_permission(id):
                return jsonify({"message": "Usuario no autorizado"}), 403
            company_id, _ = rol_definition(id)
            if not company_id:
                return jsonify({"message": "Campos incompletos"}), 404
            query = """
             SELECT COUNT(DISTINCT id) AS TotalMessages
             FROM `messages`  
            """
            result = AdminDashboard.execute_query(query)
            return jsonify(result) if result else jsonify({"message": "No data found"}), 404 
        
        @staticmethod
        @app.route('/total_Conversations/<int:id>', methods=['GET'])
        def total_Conversations(id):
            if not AdminDashboard.verify_permission(id):
                return jsonify({"message": "Usuario no autorizado"}), 403
            company_id, _ = rol_definition(id)
            if not company_id:
                return jsonify({"message": "Campos incompletos"}), 404
            query = """
             SELECT COUNT(DISTINCT sessionid) AS TotalConversations
             FROM `messages`
            """
            result = AdminDashboard.execute_query(query)
            return jsonify(result) if result else jsonify({"message": "No data found"}), 404 
        
        @staticmethod
        @app.route('/total_info_Companies/<int:id>', methods=['GET'])
        def total_info_Companies(id):
            if not AdminDashboard.verify_permission(id):
                return jsonify({"message": "Usuario no autorizado"}), 403
            company_id, _ = rol_definition(id)
            if not company_id:
                return jsonify({"message": "Campos incompletos"}), 404
            query = """
                SELECT 
                c.companyname AS Nombre,
                u.company_id, 
                COUNT(DISTINCT u.id) AS TotalUsuarios,
                COUNT(DISTINCT m.id) AS TotalMensajes,
                COUNT(DISTINCT m.sessionid) AS TotalConversaciones
                FROM 
                users u
                LEFT JOIN 
                messages m ON u.id = m.user_id
                INNER JOIN 
                companies c ON u.company_id = c.id
                GROUP BY 
                u.company_id, c.companyname ;
            """
            result = AdminDashboard.execute_query(query)
            return jsonify(result) if result else jsonify({"message": "No data found"}), 404 


#General user information                                                      
@app.route('/userGeneralInfo/<int:id>', methods=['GET'])
def userGeneralInfo(id):
    company_id, type_id = rol_definition(id)
    if company_id is not None and type_id is not None:
        return jsonify({"company_id": company_id, "type_id": type_id}), 200
    else:
        return jsonify({"message": "Usuario no encontrado o no autorizado"}), 404    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host='127.0.0.1', port=8000)

"""if __name__ == '__main__':
    app.run(debug=True)"""

""""""
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

#LOGIN 

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    auth_id = data.get('user')
    Password = data.get('password')

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "SELECT id, type_id, email, Access_token, Access_type FROM users WHERE auth_id = %s AND Password = %s"
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

#-----------------------------------------------TABLEROS CLIENTES -------------------------------------------------------------------------------------------------
#filtro por comapañia y tipo de usuario 
def get_user_company_id_if_admin(id):
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
            
            if user_info and user_info['type_id'] == 3:
                return user_info['company_id']
            else:
                return None
            
    except Exception as e:
        print(f"Error al obtener la información del usuario: {e}")
        return None
    finally:
        connection.close()
#Mensajes diarios de usuarios de compañia
def get_messages_by_company_id(company_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
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
                ORDER BY date ASC, username ASC;
            """
            cursor.execute(query, (company_id,))
            result = cursor.fetchall() # Changed from fetchone to fetchall to handle multiple results
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No messages found for this company"}), 404
        
    except Exception as e:
        print(f"Error al obtener los mensajes: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
#Obtiene el total de mensajes de usuarios por dia
@app.route('/messagesuserbyday/<int:id>', methods=['GET'])
def messagesuserbyday(id):
    company_id = get_user_company_id_if_admin(id)
    if company_id is None:
        return jsonify({"message": "User not found or not client"}), 404
    return get_messages_by_company_id(company_id)

 #Hace la consulta para el conteo de los usuarios por compañia
def get_total_users_compañia(company_id):  
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            count_sql = """
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
                    c.companyname;

            """
            cursor.execute(count_sql, (company_id,))
            result = cursor.fetchall()  
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found for this company"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
#   Hace la consulta de las conversaciones por dia 
def get_daily_conversations_by_company_id(company_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Ajusta esta consulta para agrupar las conversaciones por día
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
                    date ASC;
            """
            cursor.execute(query, (company_id,))
            result = cursor.fetchall()
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No daily conversations found for this company"}), 404
                
    except Exception as e:
        print(f"Error obtaining daily conversations: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()

@app.route('/dailyconversations/<int:id>', methods=['GET'])
def daily_conversations(id):
    company_id = get_user_company_id_if_admin(id)
    if company_id is None:
        return jsonify({"message": "User not found or not client"}), 404
    return get_daily_conversations_by_company_id(company_id)
#Hace la consulra del total de usuarios por compañia
@app.route('/total_users_by_company/<int:id>', methods=['GET'])
def total_users_compañia(id):
    company_id = get_user_company_id_if_admin(id)
    if company_id is None:
        return jsonify({"message": "Unauthorized or not an client"}), 404
    return get_total_users_compañia(company_id)

#Traer las conversaciones totales de los users de la company por mes
def get_conversations_by_month_company_id(company_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
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
                u.company_id, year, month;
            """
            cursor.execute(query, (company_id,))
            result = cursor.fetchall()
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No conversations found for this company in any month"}), 404
                
    except Exception as e:
        print(f"Error obtaining monthly conversations: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
        
        
 #reconoce el id del usuario y su typeid       
@app.route('/monthly_conversations/<int:id>', methods=['GET'])
def monthly_conversations(id):
    company_id = get_user_company_id_if_admin(id)
    if company_id is None:
        return jsonify({"message": "User not found or not admin"}), 404
    return get_conversations_by_month_company_id(company_id)       

#Traer las conversaciones totales de los users de la company
def get_conversations_by_companyid(company_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
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
                u.company_id;
            """
            cursor.execute(query, (company_id,))
            result = cursor.fetchall()
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No conversations found for this company in any month"}), 404
                
    except Exception as e:
        print(f"Error obtaining monthly conversations: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
        
  #reconoce el id del usuario y su typeid para mostrar las coversaciones totales         
        
@app.route('/total_conveationsrs/<int:id>', methods=['GET'])
def total_conversations(id):
    company_id = get_user_company_id_if_admin(id)
    if company_id is None:
        return jsonify({"message": "User not found or not client"}), 404
    return get_conversations_by_companyid(company_id) 

#------------------------------------------------------------------------------TABLERO SUPERUSERS/BS --------------------------------------------------------------

#Consulta si es un superusuario 
def get_user_if_admin(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = "SELECT type_id FROM users WHERE id = %s;"
            cursor.execute(query, (id,))
            user_info = cursor.fetchone()
            return user_info is not None and user_info['type_id'] == 3
    except Exception as e:
        print(f"Error al verificar si el usuario es administrador: {e}")
        return False
    finally:
        connection.close()

#Consulta del total de usuarios de cada cliente
def get_totalusers_companiest():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
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
                        u.company_id, c.companyname ;

            """
            cursor.execute(query)  # Corregido: se elimina el parámetro innecesario
            result = cursor.fetchall()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found"}), 404
    except Exception as e:
        print(f"Error al obtener el total de usuarios por compañía: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()


#Envia la consulta del total de usuarios de cada cliente si es superusuario
@app.route('/totalusers_companiest/<int:id>', methods=['GET'])
def totalusers_companiest(id):
    if not get_user_if_admin(id):
        return jsonify({"message": "User not found or not admin"}), 403  # Cambiado para reflejar un error de autorización más preciso
    return get_totalusers_companiest()  # Corregido: No necesita pasar un argumento

#Consulta del total de clientes
def get_totalclients():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
              SELECT COUNT(DISTINCT id) AS TotalClientes
              FROM `companies`
            """
            cursor.execute(query)  # Corregido: se elimina el parámetro innecesario
            result = cursor.fetchall()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found"}), 404
    except Exception as e:
        print(f"Error al obtener el total de usuarios por compañía: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()   
        
#Envia la consulta del total de clientes a si es superusuario      
@app.route('/totalclients/<int:id>', methods=['GET'])
def totalclients(id):
    if not get_user_if_admin(id):
        return jsonify({"message": "User not found or not admin"}), 403  
    return get_totalclients() 
    
        
#Consulta del total de mensajes

def get_totalMessages():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
             SELECT COUNT(DISTINCT id) AS TotalMessages
             FROM `messages`  
            """
            cursor.execute(query)  # Corregido: se elimina el parámetro innecesario
            result = cursor.fetchall()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found"}), 404
    except Exception as e:
        print(f"Error al obtener el total de usuarios por compañía: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()   
        
#Envia la consulta del total de mensajes a si es superusuario         
@app.route('/totalMessages/<int:id>', methods=['GET'])
def totalMessages(id):
    if not get_user_if_admin(id):
        return jsonify({"message": "User not found or not admin"}), 403  
    return get_totalMessages() 
        


#Consulta del total de conversaciones
def get_totalConversations():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
             SELECT COUNT(DISTINCT sessionid) AS TotalConversations
             FROM `messages`
            """
            cursor.execute(query)  # Corregido: se elimina el parámetro innecesario
            result = cursor.fetchall()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found"}), 404
    except Exception as e:
        print(f"Error al obtener el total de usuarios por compañía: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()   
        
#Envia la consulta del total de conversaciones a si es superusuario          
@app.route('/totalConversations/<int:id>', methods=['GET'])
def totalConversations(id):
    if not get_user_if_admin(id):
        return jsonify({"message": "User not found or not admin"}), 403  
    return get_totalConversations() 
        

#Consulta de toda la informacion de los clientes (mensajes, conversaciones, usuarios )
def get_totalinfo_companies():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
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
            cursor.execute(query)  # Corregido: se elimina el parámetro innecesario
            result = cursor.fetchall()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found"}), 404
    except Exception as e:
        print(f"Error al obtener el total de usuarios por compañía: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()   
        
#Envia la consulta del total de informacion de los clientes si es superusuario             
@app.route('/totalinfo_companies/<int:id>', methods=['GET'])
def totalinfo_companies(id):
    if not get_user_if_admin(id):
        return jsonify({"message": "User not found or not admin"}), 403  
    return get_totalinfo_companies() 

#cuenta cuantos la cantidad de ususarios con los typesid
def get_user_typesid():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
             SELECT usertype, COUNT(u.id) AS cantidad 
                FROM users u
                join usertypes on u.type_id = usertypes.id
                GROUP BY usertype;
            """
            cursor.execute(query)  # Corregido: se elimina el parámetro innecesario
            result = cursor.fetchall()

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No users found"}), 404
    except Exception as e:
        print(f"Error al obtener el total de usuarios por compañía: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()   
        
#Envia la consulta del total de informacion de los clientes si es superusuario             
@app.route('/user_typesid/<int:id>', methods=['GET'])
def user_typesid(id):
    if not get_user_if_admin(id):
        return jsonify({"message": "User not found or not admin"}), 403  
    return get_user_typesid() 



#-----------------------------------------------------TABLERO USERS --------------------------------------------------------------

# No es necesario verificar el tipo de usuario aquí, ya que todos los usuarios pueden ver su propia información.

#Consulta del total de mensajes del usuario individual
def get_total_messages_user(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    COUNT(id) AS TotalMensajes
                FROM messages
                WHERE user_id = %s;
            """
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result and result['TotalMensajes'] is not None:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No messages found for this user"}), 404
    except Exception as e:
        print(f"Error al obtener los mensajes del usuario: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
#Envia el total de mensajes del usuario individual
@app.route('/total_messages_user/<int:user_id>', methods=['GET'])
def total_messages_user(id):

    return get_total_messages_user(id)   


#Consulta del total de conversaciones del usuario individual
def get_total_conversations_user(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    COUNT(DISTINCT sessionid) AS TotalConversaciones
                FROM messages
                WHERE user_id = %s;
            """
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result and result['TotalConversaciones'] is not None:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No conversations found for this user"}), 404
    except Exception as e:
        print(f"Error al obtener las conversaciones del usuario: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
#Envia el total de conversaciones del usuario individual
@app.route('/total_conversations_user/<int:id>', methods=['GET'])
def total_conversations_user(id):
    return get_total_conversations_user(id) 
#Consulta del total de mesajes y conversaciones diarios del usuario individual
def get_daily_messages_conversations_user(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    DATE(timestamp) AS Fecha,
                    COUNT(id) AS MensajesPorDia,
                    COUNT(DISTINCT sessionid) AS ConversacionesPorDia
                FROM messages
                WHERE user_id = %s
                GROUP BY Fecha
                ORDER BY Fecha ASC;
            """
            cursor.execute(query, (id,))
            result = cursor.fetchall()
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No daily messages or conversations found for this user"}), 404
    except Exception as e:
        print(f"Error al obtener los mensajes y conversaciones diarios del usuario: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
#Envia el total de mesajes y conversaciones diarios
@app.route('/daily_messages_conversations_user/<int:id>', methods=['GET'])
def daily_messages_conversations_user(id):
    return get_daily_messages_conversations_user(id)

#consulta de comportamiento de bot y el user
def get_behavior_chat_user(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
               SELECT 
                    CASE 
                        WHEN type = 'bot_response' THEN 'Respuestas del Chat'
                        WHEN type = 'user_message' THEN 'Solicitudes de Usuario'
                    END AS type,
                    COUNT(*) AS cantidad
                FROM 
                    messages
                WHERE 
                    type IN ('bot_response', 'user_message')
                    AND user_id =%s
                GROUP BY 
                    type;
            """
            cursor.execute(query, (id,))
            result = cursor.fetchall()
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No daily messages or conversations found for this user"}), 404
    except Exception as e:
        print(f"Error al obtener los mensajes y conversaciones diarios del usuario: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
        
#Envvia comportamiento de bot y el user
@app.route('/behavior_chat_user/<int:id>', methods=['GET'])
def behavior_chat_user(id):
    return get_behavior_chat_user(id)

if __name__ == '__main__':
    app.run(debug=True)
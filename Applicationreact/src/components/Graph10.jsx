import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { ResponsiveContainer } from 'recharts';
//SUPER USUARIO
//TOTAL CONVERSACIONES 
const Graph9 = () => {
  const [data, setData] = useState([]);//variable de datos y funcion de actualizacion 

  useEffect(() => {
    // solicitud al API
    fetch('https://flaskapimentor.azurewebsites.net/Total_conversations_by_company/1')
      .then(response => response.json()) // Convierte la respuesta a JSON
      .then(data => { // Maneja los datos JSON
        console.log(data)
        // Aquí, `data` ya es el objeto JavaScript resultante de la respuesta JSON, no necesitas `response.data`
        const formattedData = data.map(item => ({
          value: item.total_conversations
        }));
  
        setData(formattedData);
      })
      .catch((error) => {
        console.error('Error al obtener datos: ', error);
      });
  }, []);

  // Colores para el gráfico


  return (
    <ResponsiveContainer width="100%" height="100%">
    <div className='GraphTotalConversationsByCompany'>
      
      {data.length > 0 ? (
        <div className='numbmesages'>
          <ul>
            {data.map((item, index) => (
              <li key={index}>{`${item.value}`}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Cargando datos...</p>
      )}
      <div className='rectangulo'>
        <h3>Conversaciones En Total</h3>
      </div>
    </div>
  </ResponsiveContainer>
  );
};

export default Graph9;

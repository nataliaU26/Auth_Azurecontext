import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Label, Legend, ResponsiveContainer } from 'recharts';
//USUARIO
// GRAFICO mENSAJES Y CONVERSACIONES POR DIA
const Graph5 = () => {
    const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Asegúrate de sustituir la URL con la ruta correcta de tu API y proporcionar cualquier parámetro o cabecera necesaria para la autenticación
        const response = await axios.get('http://localhost:5000/daily_messages_conversations_user/1'); // Sustituye 'USER_ID' por el ID real del usuario administrador
        setData(response.data);
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    };

    fetchData();
  }, []);

  // Ajusta el aspecto del gráfico para que se parezca al mockup
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 } }  barCategoryGap="5%" barGap={2}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="Fecha">
            <Label value="" offset={-10} position="insideBottom" />
        </XAxis>
        <YAxis  />
        <Tooltip />
        <Legend />
        <Bar dataKey="MensajesPorDia" fill="#424AB5" name="TotalUsuarios" minPointSize={10} />
        <Bar dataKey="ConversacionesPorDia" fill="#FFB0E7" name="TotalMensajes"  />

      </BarChart>
    </ResponsiveContainer>
  );
};

export default Graph5;

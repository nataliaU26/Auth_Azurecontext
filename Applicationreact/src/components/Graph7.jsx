import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
//SUPER USUARIO
// GRAFICO DE CANTIDAD D TIPOS DE USUARIOS 
const Graph7 = () => {
  const [data, setData] = useState([]);//variable de datos y funcion de actualizacion 

  useEffect(() => {
    // solicitud al API
    Axios.get('http://localhost:5000/user_typesid/1') //envia funcion del api
    //respuestas de errores 
      .then((response) => {
        //accede a la info y crea el objeto
        const formattedData = response.data.map(item => ({
          name: `${item.usertype}`,
          value: item.cantidad
        }));
        setData(formattedData);
      })
      .catch((error) => {
        console.error('Error al obtener datos: ', error);
      });
  }, []);

  // Colores para el gráfico
  const COLORS = ['#FFB0E7', '#E6E8EC', '#424AB5', '#2B306E','#12142E','#FF7ED8','#FC16B6','#989FF0','#293197'];


  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={150}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default Graph7;

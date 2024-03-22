import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
//SUPER USUARIO
// GRAFICO DE CANTIDAD DE USUARIOS POR COMPAÑIA
const Graph3 = () => {
  const [data, setData] = useState([]);//variable de datos y funcion de actualizacion 

  useEffect(() => {
    // solicitud al API
    Axios.get('http://localhost:5000/totalusers_companiest/1') //envia funcion del api
    //respuestas de errores 
      .then((response) => {
        //accede a la info y crea el objeto
        const formattedData = response.data.map(item => ({
          name: `${item.NombreCompania}`,
          value: item.TotalUsuarios
        }));
        setData(formattedData);
      })
      .catch((error) => {
        console.error('Error al obtener datos: ', error);
      });
  }, []);

  // Colores para el gráfico
  const COLORS = [ '#424AB5', '#2B306E','#E6E8EC','#12142E','#FF7ED8','#FC16B6','#989FF0','#293197','#FFB0E7'];
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

export default Graph3;



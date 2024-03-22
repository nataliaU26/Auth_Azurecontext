
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';
//CLIENTE
//GRAFICO DE MENSAJES/CONVERSACIONES DE USUARIOS POR DIA 
const Graph1 = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  useEffect(() => {
    fetch('https://flaskapimentor.azurewebsites.net/messages_user_by_day/1')
      .then(response => response.json())
      .then(data => {
        // console.log(data);
        setData(data);
      })
      .catch(error => console.error('Error:', error));
  }, []); 


  useEffect(() => {
    // Filtra los datos basado en las fechas seleccionadas
    const filtered = data.filter(d => {
      const date = new Date(d.date); // Asume que 'd.date' es una propiedad de tus objetos de datos
      return (!startDate || date >= new Date(startDate)) && (!endDate || date <= new Date(endDate));
    });
    setFilteredData(filtered);
  }, [data, startDate, endDate]);
  if (!data) return <div>Loading...</div>;


  const chartWidth = data.length * 50;
  
  // Ajusta el aspecto del gráfico para que se parezca al mockup
  return (

    <div className='Graph1' >
    <div className='titulo'>
    <h2>Mensajes y conversaciones por dia</h2>

    </div>

    <div  className='filtrodate'>
        <input
        type="date"
        value={startDate}
        onChange={e => setStartDate(e.target.value)}
        placeholder="dd/mm/aaaa" 
      />
      <input
        type="date"
        value={endDate}
        onChange={e => setEndDate(e.target.value)}
        placeholder="dd/mm/aaaa" 
      />
      </div>
      <div className={'containerBar'} >

      <ResponsiveContainer  width={chartWidth}  >
      
      <BarChart   data={data} >
        <CartesianGrid  strokeDasharray="3 3" />
        <XAxis dataKey="username"   />
        <YAxis/>
        <Tooltip />
        
        <Legend />
        <Bar  dataKey="message_count" fill="#424AB5" name="Mensajes" />
        <Bar dataKey="message_count" fill="#FFB0E7" name="Conversaciones" />
    
       
      </BarChart>
      </ResponsiveContainer>

      </div>
 
    </div>
  );
};

export default Graph1;
// import React, { useState, useEffect } from 'react';
// import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
// import axios from 'axios';
// //CLIENTE
// //GRAFICO DE MENSAJES/CONVERSACIONES DE USUARIOS POR DIA 
// const Graph1 = () => {
//   const [data, setData] = useState([]);

//   useEffect(() => {
//     fetch('https://flaskapimentor.azurewebsites.net/messages_user_by_day/1')
//       .then(response => response.json())
//       .then(data => {
//         // console.log(data);
//         setData(data);
//       })
//       .catch(error => console.error('Error:', error));
//   }, []); 
//   if (!data) return <div>Loading...</div>;


//   const chartWidth = data.length * 50;
//   // Ajusta el aspecto del gráfico para que se parezca al mockup
//   return (
//     <div style={{ marginTop: '2%', width: '100%', height: '97%', overflowX: 'scroll' }}>
//     <ResponsiveContainer paddingTop = '5%' width={chartWidth} height="87%">
//     <h2>Mensajes y conversaciones por dia</h2>
//       <BarChart width={500} data={data} margin={{ top: 40, right: 30, left: 20, bottom: 10 }}>
//         <CartesianGrid strokeDasharray="3 3" />
//         <XAxis dataKey="username" />
//         <YAxis />
//         <Tooltip />
//         <Legend />
//         <Bar dataKey="message_count" fill="#424AB5" name="Mensajes" />
//         <Bar dataKey="message_count" fill="#FFB0E7" name="Conversaciones" />
//       </BarChart>
//     </ResponsiveContainer>
//     </div>
//   );
// };

// export default Graph1;

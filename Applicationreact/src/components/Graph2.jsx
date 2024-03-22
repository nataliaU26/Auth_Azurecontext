import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';




const Graph2 = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  // Initializing startDate and endDate with empty strings
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const COLORS = ['#FFB0E7', '#939496', '#424AB5', '#2B306E','#12142E','#FF7ED8','#FC16B6','#989FF0','#293197'];
  const monthNames = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];


  useEffect(() => {
    fetch('https://flaskapimentor.azurewebsites.net/conversations_by_month_company/1')
      .then(response => response.json())
      .then(data => {
        const formattedData = data.map(item => ({
          name: `${monthNames[item.month - 1]}-${item.year}`,
          value: item.total_conversations,
          date: new Date(item.year, item.month - 1)
        }));
        setData(formattedData);
        // Filtrando los datos inmediatamente después de establecerlos
        filterData(formattedData, startDate, endDate);
      })
      .catch((error) => {
        console.error('Error al obtener datos: ', error);
      });
  }, []);




  useEffect(() => {
    // Filtra los datos basado en las fechas seleccionadas
    const filtered = data.filter(d => {
      const date = new Date(d.date); // Asume que 'd.date' es una propiedad de tus objetos de datos
      return (!startDate || date >= new Date(startDate)) && (!endDate || date <= new Date(endDate));
    });
    setFilteredData(filtered);
  }, [data, startDate, endDate]); 


  const filterData = (data, startDate, endDate) => {
    // Asegurándose de que startDate y endDate estén definidos
    if (!startDate || !endDate) return;

    const start = startDate;
    const end = endDate;
    const filtered = data.filter(item => {
      const itemDate = item.date;
      return itemDate >= start && itemDate <= end;
    });
    setFilteredData(filtered);
  };


  return (

<div className='Graph2'>
<div className='titulo'> 
      <h2>Conversaciones por compañía al mes</h2>
      </div>
      <div className='fechapastel'>
        <input     type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          placeholder="dd/mm/aaaa"/>
        <input  
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          placeholder="dd/mm/aaaa" />
      </div>

<ResponsiveContainer  className='GraphPie' >
      {filteredData.length > 0 ? (
  
      <PieChart className='pastel' >


        <Pie 
          
          data={filteredData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
          outerRadius={'75%'}
          fill="#8884d8"
          dataKey="value"
         
        >
          {filteredData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}

        </Pie>
        <Tooltip />
         <Legend  layout='vertical' align='right' verticalAlign='middle'  /> 
     
      </PieChart>
    
      ):(
        <p>No existen datos...</p>
      )}
    </ResponsiveContainer>



    </div>




  );
};

export default Graph2;



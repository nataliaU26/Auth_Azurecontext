import React, { useState, useEffect } from 'react';
import Axios from 'axios';
import { ResponsiveContainer } from 'recharts';
//Cliente
//Total usuarios de la compañia
const Graph8 = () => {
  
  return (
    <ResponsiveContainer width="100%" height="100%">
    <div className='GraphTotalActiveUsers'>
      <div className='titulo'> 
       <h2>Bienvenido</h2>
       </div>
      
      <div className='circulo'>
       <div className='svg'>
          <img src="public\User.png" alt="" />
          </div>
      </div>
      <div className='rectangulo'>
        <h2>USER NAME</h2>
        <h3>USER ID</h3>
      </div>
    </div>
  </ResponsiveContainer>
  );
};

export default Graph8;

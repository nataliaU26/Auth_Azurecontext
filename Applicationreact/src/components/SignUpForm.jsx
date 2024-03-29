
//import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthProvider'
import axios from '../api/axios';
import { useRef, useState, useEffect, useContext } from 'react';

const SignUpForm = () =>{  
    const {setAuth} = useContext(AuthContext);

    const userRef= useRef();
    const errRef= useRef();
    const navigate = useNavigate();

    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [errMsg, setErrMsg] = useState('');


    useEffect(() =>{
      userRef.current.focus();
  },[])

  useEffect(() =>{
      setErrMsg('');
  },[user,password] )

    const handleSubmit = async(e)=> {
         e.preventDefault();
         try{
          //console.log(user,password);
          //ajustar con el URL login
          const response = await axios.post('http://127.0.0.1:5000/login',
          JSON.stringify({user,password}),
            {
              headers:{'Content-Type':'application/json' },
              withCredentials: true
              
            }
          );
          console.log(JSON.stringify(response?.data));
          //console.log(JSON.stringify(response));

          const Access_token = response?.data?.Access_token;
          const Access_type = response?.data?.Access_type;
          setAuth({ user,password,Access_type,Access_token});
          setUser('');
          setPassword('');
          navigate('/hi');

         }catch (err){
          if(!err?.response){
            setErrMsg("No server response");
          }else if( err.response?.status === 7){
            setErrMsg("Data missing");
          }else if( err.response?.status === 8){
            setErrMsg("Unauthorized");
          }else{
            setErrMsg("login failed");
          }
          errRef.current.focus();
         }
         
    }
    return (
      <div className="signup-form-container">
      <div className="container">
          <div className="header">
            <div className="text1">Mentor-IA | Monitor</div>
            <div className="text2">Login</div>
            <div className="underline"></div>
          </div>

            <p ref={errRef} className={errMsg ? "errmsg":"offscreen"} 
            aria-live="assertive"> {errMsg} </p>

          <form onSubmit={handleSubmit}>
              <div className="input">
                <div className="inputs">
                  <input
                        type="text"
                        id="username"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(e) => setUser(e.target.value)}
                        value={user}
                        required
                      />
                  <label htmlFor="username" className={user ? 'filled' : ''}>Username</label>
                </div>
                <div className="inputs">
                  <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                  <label htmlFor="password" className={password ? 'filled' : ''}>Password</label>
                </div>
                
              </div>
              <div className="actions">
          <button className='submit-button'>Continue</button>
        </div>
              </form>
      </div>
      
    </div> 
      );
}
export default SignUpForm;

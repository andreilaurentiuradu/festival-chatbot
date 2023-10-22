import { useState, useRef, useEffect } from "react";
import Coordinates from "./Coordinates";
import Chatbox from "./Chatbox";
import "./animatie.css";

function Home() {
  
 
 
  const [activeButton, setActiveButton] = useState('chatbot'); // Starea pentru butonul activ


  return (
    <div className="lg:w-1/3 md:w-1/2 w-3/4 p-4  lg:ml-5  border rounded-lg shadow-lg chat_color mb-24 lg:mb-1 ">
      <div className="flex justify-end items-center mb-3">
      <button
          className={`mb-2 bg-gray-200 border border-vlack-100 text-black p-2 rounded-l-3xl ${activeButton === 'inputCoordinates' ? '' : 'active-button'}`}
          onClick={() => setActiveButton('chatbot')}
        >
          ChatBot
        </button>
        <button
          className={`mb-2 bg-gray-200 border border-black-100 text-black p-2 rounded-r-3xl ${activeButton === 'chatbot' ? '' : 'active-button'}`}
          onClick={() => setActiveButton('inputCoordinates')}
        >
          InputCoordinates
        </button>
        
        </div>
      

      {/* Conținut pentru ChatBot */}
      {activeButton === 'chatbot' && 
        <Chatbox/>
      }

      {/* Conținut pentru InputCoordinates */}
      {activeButton === 'inputCoordinates' && 
        <Coordinates/>
      }

      
    </div>
  );
}

export default Home;

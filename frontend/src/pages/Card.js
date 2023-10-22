import React from "react";

function Card3({ ...props}) {
    return (
      <div className={`rounded-lg p-6 shadow-sm justify-center items-center `}>
        <div className=" rounded-lg justify-center items-center flex">
            
        <a href={props.value}>
            <img
            className="w-1/2 cursor-pointer transition duration-200 ease-in-out transform hover:scale-110 rounded-lg h-1/2 mx-auto "
            src="https://cdn-icons-png.flaticon.com/512/2875/2875387.png"
            alt="Image Alt Text"
            />
        </a>

          
        </div>
        <h3 className="pt-5 pl-3 text-[14px] font-normal text-gray-600 block">
          Distance: {props.distance} Duration: {props.duration} 
        </h3>
        <p className="font-normal text-base text-justify px-3 text-gray-500 cursor-pointer text-lg duration-300 transition hover:text-[#FA5252] mt-2">
          {props.instructions}
        </p>
      </div>
    );
  }
  
  function Card3Presentation(props) {
    return (
       
      <div className=" ">
        <Card3
          className="bg-[#fcf4ff]"
          instructions={props.instructions}
          distance={props.distance}
          value={props.value}
          duration={props.duration}
        />
        
      </div>
    );
  }
  
  export default Card3Presentation;
  
import React, { useState, useContext } from "react";
import Swal from 'sweetalert2';
import { coordinatesRequest } from "../common/services/coordinates";
import Card3Presentation from "./Card";
import "./animatie.css"

const googleMapsApiKey = 'AIzaSyAD1KCCoKf_NpcFpJ1Q0Y5AINHeMRgExpo';

function Coordinates() {
  const [x, setX] = useState("");
  const [y, setY] = useState("");
  const [question, setQuestion] = useState("");
  const [hasBeenSearched, setHasBeenSearched] = useState(false);
  const [mapsLink, setMapsLink] = useState("");
  const [distance, setDistance] = useState("");
  const [instructions, setInstructions] = useState("");
  const [destination, setDestination] = useState("");
  const [duration, setDuration] = useState("");

  const handleClick = async () => {
    try {
      // Create an object with the values of x, y, and question
      const values = { x, y, location: question };
      console.log(values);
      // You can then use 'values' to send the request
      // For example, you can send it to a function like 'coordinatesRequest'
      const response = await coordinatesRequest(values);

      // Update the UI or perform other actions based on the response
      // ...
      // console.log(response.data["maps_link"]);
      setMapsLink(response.data["maps_link"]);
      setDistance(response.data["distance"]);
      setInstructions(response.data["instructions"]);
      setDestination(response.data["destination"]);
      setDuration(response.data["duration"]);
      setHasBeenSearched(true);
     
      console.log(response.data["duration"]);

      // Show a success message using Swal or other notification library
      Swal.fire({
        title: 'Message sent successfully',
        icon: 'success',
        timer: 2500,
        showConfirmButton: false,
      });
    } catch (e) {
      // Handle any errors that occur during the server request
      console.error(e);

      // Show an error message using Swal or other notification library
      Swal.fire({
        title: 'Message could not be sent',
        icon: 'error',
        timer: 5000,
        showConfirmButton: false,
      });
    }
  };

  return (
    <div className="lg:h-96 md:h-3/4 sm:h-3/4 h-3/4  flex p-2 lg:flex-row flex-col bg-white rounded-xl justify-center items-center">
      {/* Left Column for X and Y Coordinates */}
      <div className="    p-2 border border-gray-300 flex flex-col justify-center items-center rounded-lg">
        <form>
          <div className="mb-4 p-2">
            <label htmlFor="x" className="block text-gray-700 text-sm font-bold mb-2">
              X Coordinate:
            </label>
            <input
              type="text"
              id="x"
              name="x"
              className="p-2 border rounded-lg"
              placeholder="Enter X coordinate"
              value={x}
              onChange={(e) => setX(e.target.value)}
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="y" className="block text-gray-700 text-sm font-bold mb-2">
              Y Coordinate:
            </label>
            <input
              type="text"
              id="y"
              name="y"
              className="p-2 border rounded-lg"
              placeholder="Enter Y coordinate"
              value={y}
              onChange={(e) => setY(e.target.value)}
            />
          </div>
        </form>
      </div>
      
      {/* Right Column for Question and Submit */}

      {!hasBeenSearched ? (<div className="lg:w-1/2  p-2 flex flex-col justify-center items-center">
        <div className="mb-4 text-center">
          <label htmlFor="question" className="block text-gray-700 text-md font-bold mb-2 justify-center">
            Where do you want to go?
          </label>
          <input
            type="text"
            id="question"
            name="question"
            className="p-2 border rounded-lg w-full"
            placeholder="Enter your destination"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
        </div>
        <button className="bg_color text-white p-2 rounded-lg w-1/2" onClick={handleClick}>
          Submit
        </button>
     
        
      </div>) : (<div className="p-4 my-2 lg:w-1/2  lg:p-2 lg:flex lg:flex-col items-center justify-center">
            
          
            <Card3Presentation value={mapsLink} distance={distance} instructions={instructions} duration={duration}/>

          
        
        </div>)}
      
      
    </div>
  );
}

export default Coordinates;

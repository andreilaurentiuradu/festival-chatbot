import React, { useState, useRef, useEffect } from "react";
import { chatRequest } from "../common/services/chattext";
import Swal from 'sweetalert2';
import "./animatie.css";
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getDatabase, ref, set } from "firebase/database";



function Chatbox() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", isUser: false },
  ]);

  const [input, setInput] = useState('');
  const messageContainerRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    // Create a new message object for the user's input
    const newMessage = { text: input, isUser: true };
    setMessages([...messages, newMessage]);
    setInput('');
    try {
      // Send the message to the server and await the response
      setIsLoading(true);
      const response = await chatRequest({ message: input });
      setIsLoading(false);

      // Update the UI with the user's message and the server's response
      setMessages([...messages, newMessage, { text: response.data, isUser: false }]);

    } catch (e) {
      // Handle any errors that occur during the server request
      console.error(e);

      // Show an error message using Swal or other notification library
      
    }
  };

  useEffect(() => {
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div>
      <div
        ref={messageContainerRef}
        className="h-96 border border-black-500 p-2 rounded-lg overflow-y-auto white_new"
      >
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 ${message.isUser ? 'text-right' : 'text-left'}`}
          >
            
            <div
              className={`py-2 px-4  d-flex row rounded-lg inline-block ${
                message.isUser ? 'message_color text-white' : 'response_color text-black'
              }`}
            >
             
              {message.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flicker-animation">
            <div key="31431" className="mb-2 text-left">
              
              <span
                className="py-2 px-4 rounded-lg inline-block response_color"
              >
                <div className=" ">...</div>
              </span>
            </div>
          </div>
        )}
      </div>
      <div className="mt-2 flex">
        <input
          type="text"
          className="flex-1 p-2 rounded-l-lg border border-gray-300 white_new"
          placeholder="Type a message..."
          value={input}
          onChange={handleInputChange}
          style={{ "::placeholder": { color: "white" } }}
        />
        <button
          className="bg_color text-white p-2 rounded-r-lg"
          onClick={handleSendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbox;

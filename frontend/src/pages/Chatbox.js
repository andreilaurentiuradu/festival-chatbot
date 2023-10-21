import React, { useState, useRef, useEffect } from "react";
import { chatRequest } from "../common/services/chattext";
import Swal from 'sweetalert2';

function Chatbox() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", isUser: false },
  ]);

  const [input, setInput] = useState('');
  const messageContainerRef = useRef(null);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSendMessage = async () => {
    if (input.trim() === '') return;
  
    // Create a new message object for the user's input
    const newMessage = { text: input, isUser: true };
    console.log(newMessage);
  
    try {
      // Send the message to the server and await the response
      const response = await chatRequest({ message: input });
  
      // Update the UI with the user's message and the server's response
      setMessages([...messages, newMessage, { text: response, isUser: false }]);
      setInput('');
  
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
  

  useEffect(() => {
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div>
      {/* ... codul pentru ChatBot */}
      <div
        ref={messageContainerRef}
        className="h-96 border border-gray-300 p-2 rounded-lg overflow-y-auto"
      >
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 ${message.isUser ? 'text-right' : 'text-left'}`}
          >
            <span
              className={`py-2 px-4 rounded-lg inline-block ${
                message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-300'
              }`}
            >
              {message.text}
            </span>
          </div>
        ))}
      </div>
      <div className="mt-2 flex">
        <input
          type="text"
          className="flex-1 p-2 rounded-l-lg border border-grey-300 bg-transparent"
          placeholder="Type a message..."
          value={input}
          onChange={handleInputChange}
          style={{ "::placeholder": { color: "white" } }}
        />

        <button
          className="bg-blue-500 text-white p-2 rounded-r-lg"
          onClick={handleSendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbox;

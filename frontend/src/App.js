import "./App.css";

import Home from "./pages/Home";

function App() {
  return (
    <div >
      <div className="color_bg ">
     
        <div className="flex lg:flex-row flex-col justify-around items-center lg:h-screen  ">
          
          <div className="flex flex-col justify-around items-center w-5/6 lg:w-2/5 mt-24 " >
          
            <h2 className="sm:mb-10 md-6 sm:text-7xl text-4xl ">CHAT BOT</h2>
            <div className="mt-10 "><h1 className="sm:mb-7 mb-10 lg:mb-0  leading-7 sm:text-l text-sm">Introducing the cutting-edge chatbot, freshly launched to redefine conversational AI with unprecedented sophistication</h1></div>
            
          </div>  
          
          <Home />
        </div>
        
      </div>
    </div>
  );
}

export default App;

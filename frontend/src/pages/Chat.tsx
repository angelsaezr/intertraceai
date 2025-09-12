import { useState, useEffect, useRef } from "react";

const App = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<string[]>([]);
  const socketRef = useRef<WebSocket | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    // Create a new WebSocket connection
    socketRef.current = new WebSocket("ws://localhost:8000/chat");

    // Handle WebSocket open event
    socketRef.current.onmessage = (event) => {
      setMessages((prev) => [...prev, `🤖: ${event.data}`]);
    };

    return () => {
      if (
        socketRef.current &&
        socketRef.current.readyState === WebSocket.OPEN
      ) {
        socketRef.current.close();
      }
    };
  }, []);

  // Send message function
  const sendMessage = () => {
    if (socketRef.current && input.trim()) {
      socketRef.current.send(input);
      setMessages((prev) => [...prev, `🧑: ${input}`]);
      setInput("");
    }
  };

  return (
    <div className="p-5">
      <div className="h-72 overflow-y-scroll border border-gray-400 mb-2.5 rounded">
        {messages.map((msg, idx) => (
          <div key={idx}>{msg}</div>
        ))}
      </div>
      <div className="flex">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          className="w-4/5 border border-gray-300 rounded px-2 py-1 focus:outline-none"
        />
        <button
          onClick={sendMessage}
          className="w-[18%] ml-[2%] bg-blue-500 text-white rounded px-2 py-1 hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default App;

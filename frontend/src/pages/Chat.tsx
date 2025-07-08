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
    <div style={{ padding: 20 }}>
      <div
        style={{
          height: 300,
          overflowY: "scroll",
          border: "1px solid gray",
          marginBottom: 10,
        }}
      >
        {messages.map((msg, idx) => (
          <div key={idx}>{msg}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage} style={{ width: "18%", marginLeft: "2%" }}>
        Send
      </button>
    </div>
  );
};

export default App;

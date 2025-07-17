
import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import axios from "axios";

const App = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleSubmit = async () => {
    const res = await axios.post("http://localhost:8000/ask", { question });
    setAnswer(res.data.answer);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>USCIS Chatbot</h1>
      <textarea
        rows="3"
        style={{ width: "100%", padding: "1rem" }}
        placeholder="Ask a USCIS question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <br />
      <button onClick={handleSubmit} style={{ marginTop: "1rem" }}>
        Ask
      </button>
      <div style={{ marginTop: "2rem", whiteSpace: "pre-wrap" }}>{answer}</div>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App />);

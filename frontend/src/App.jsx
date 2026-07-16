import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [model, setModel] = useState("gemini");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/chat",
        {
          question,
          model,
        }
      );

      setAnswer(response.data.answer);
      setSources(response.data.sources);
    } catch (error) {
      console.error(error);
      setAnswer("Something went wrong.");
      setSources([]);
    }

    setLoading(false);
  };

  return (
    <div className="container">

      <div className="card">

        <h1>RAG Chatbot</h1>

        <div className="models">

          <button
            className={model === "gemini" ? "active" : ""}
            onClick={() => setModel("gemini")}
          >
            Gemini
          </button>

          <button
            className={model === "qwen" ? "active" : ""}
            onClick={() => setModel("qwen")}
          >
            Qwen
          </button>

        </div>

        <textarea
          rows="5"
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          className="askButton"
          onClick={askQuestion}
          disabled={loading}
        >
          {loading ? "Thinking..." : "Ask"}
        </button>

        {answer && (
          <>
            <h2>Answer</h2>

            <div className="answer">
              {answer}
            </div>

            <h3>Sources</h3>

            <ul>
              {sources.map((source) => (
                <li key={source}>{source}</li>
              ))}
            </ul>
          </>
        )}

      </div>

    </div>
  );
}

export default App;
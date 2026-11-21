import { useState } from "react";
import { sendChatMessage } from "./services/api";
import {
  Bot,
  Send,
  User,
  FileText,
  LoaderCircle,
  ShieldCheck
} from "lucide-react";

function Assistant() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    const userQuestion = question.trim();

    if (!userQuestion || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", text: userQuestion }
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await sendChatMessage(userQuestion);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: response.answer,
          sources: response.sources || []
        }
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: "Unable to connect to the Safety Assistant. Please check whether the backend is running.",
          sources: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="content assistant-page">

      <div className="welcome">
        <div>
          <p className="eyebrow">AI-POWERED SAFETY KNOWLEDGE</p>
          <h2>Safety Assistant<span>.</span></h2>
          <p className="welcome-text">
            Ask questions about workplace safety documents.
            Get answers grounded in your uploaded safety manuals.
          </p>
        </div>
      </div>

      <div className="panel assistant-panel">

        <div className="assistant-header">
          <div className="assistant-avatar">
            <Bot size={23} />
          </div>

          <div>
            <h3>SENTINEL AI Assistant</h3>
            <p>
              <ShieldCheck size={13} />
              Document-grounded safety assistance
            </p>
          </div>

          <span className="assistant-status">LOCAL AI</span>
        </div>

        <div className="chat-messages">

          {messages.length === 0 && (
            <div className="chat-welcome">
              <Bot size={38} />
              <h3>How can I help you?</h3>
              <p>
                Ask me about safety procedures, protective equipment,
                workplace hazards, and emergency guidelines.
              </p>
              <span>
                Example: What protective equipment should workers wear?
              </span>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              className={`chat-message ${message.role}`}
              key={index}
            >
              <div className="message-avatar">
                {message.role === "user"
                  ? <User size={17} />
                  : <Bot size={17} />}
              </div>

              <div className="message-content">
                <strong>
                  {message.role === "user" ? "You" : "Safety Assistant"}
                </strong>

                <p>{message.text}</p>

                {message.sources?.length > 0 && (
                  <div className="message-sources">
                    <strong>
                      <FileText size={14} /> Sources
                    </strong>

                    {message.sources.map((source, sourceIndex) => (
                      <span key={sourceIndex}>
                        {source.source}
                        {source.page
                          ? ` — Page ${source.page}`
                          : ""}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-loading">
              <LoaderCircle size={17} />
              Searching safety documents and generating an answer...
            </div>
          )}

        </div>

        <div className="chat-input-area">
          <input
            type="text"
            placeholder="Ask a workplace safety question..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") handleSend();
            }}
            disabled={loading}
          />

          <button
            className="send-button"
            onClick={handleSend}
            disabled={!question.trim() || loading}
          >
            <Send size={18} />
            Send
          </button>
        </div>

        <p className="assistant-disclaimer">
          AI-generated responses must be verified against official safety
          procedures. Do not rely on this assistant alone during emergencies.
        </p>

      </div>
    </div>
  );
}

export default Assistant;
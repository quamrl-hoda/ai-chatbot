import { useState, useRef, useEffect } from "react";

const API_URL = "http://localhost:8000";

// ── Icons (inline SVG) ────────────────────────────────────────────────────────
const PlusIcon = () => (
  <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
    <path d="M12 5v14M5 12h14" strokeLinecap="round"/>
  </svg>
);
const SendIcon = () => (
  <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
    <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);
const ChatIcon = () => (
  <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);
const BotIcon = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 64 64" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
    {/* Antenna */}
    <rect x="30" y="2" width="4" height="10" rx="2"/>
    <circle cx="32" cy="2" r="3"/>
    {/* Head */}
    <rect x="10" y="12" width="44" height="34" rx="8"/>
    {/* Eyes */}
    <rect x="18" y="22" width="10" height="10" rx="3" fill="#10a37f"/>
    <rect x="36" y="22" width="10" height="10" rx="3" fill="#10a37f"/>
    {/* Mouth */}
    <rect x="20" y="36" width="24" height="5" rx="2.5" fill="#10a37f"/>
    {/* Neck */}
    <rect x="26" y="46" width="12" height="6" rx="2"/>
    {/* Body shoulders */}
    <rect x="14" y="52" width="36" height="6" rx="4"/>
  </svg>
);

// ── Helpers ────────────────────────────────────────────────────────────────────
function makeId() { return Math.random().toString(36).slice(2, 9); }
function makeTitle(text) { return text.length > 38 ? text.slice(0, 38) + "…" : text; }

// ── Typing dots ───────────────────────────────────────────────────────────────
function TypingDots() {
  return (
    <span style={{ display: "inline-flex", gap: 4, alignItems: "center", padding: "4px 0" }}>
      {[0, 1, 2].map(i => (
        <span key={i} style={{
          width: 7, height: 7, borderRadius: "50%",
          background: "#aaa",
          display: "inline-block",
          animation: "dotBounce 1.2s infinite",
          animationDelay: `${i * 0.2}s`,
        }} />
      ))}
    </span>
  );
}

// ── Message ───────────────────────────────────────────────────────────────────
function Message({ role, content, isTyping }) {
  const isUser = role === "user";
  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      padding: "6px 0",
      animation: "fadeUp 0.2s ease",
    }}>
      {!isUser && (
        <div style={{
          width: 32, height: 32, borderRadius: "50%",
          background: "linear-gradient(135deg, #10a37f, #1a7f64)",
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "#fff", flexShrink: 0, marginRight: 12, marginTop: 2,
        }}>
          <BotIcon />
        </div>
      )}
      <div style={{
        maxWidth: "72%",
        padding: isUser ? "10px 16px" : "10px 16px",
        borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
        background: isUser
          ? "linear-gradient(135deg, #10a37f, #0d8f6e)"
          : "#2f2f2f",
        color: isUser ? "#fff" : "#ececec",
        fontSize: 14.5,
        lineHeight: 1.65,
        whiteSpace: "pre-wrap",
        wordBreak: "break-word",
        boxShadow: isUser
          ? "0 2px 12px rgba(16,163,127,0.25)"
          : "0 1px 4px rgba(0,0,0,0.3)",
      }}>
        {isTyping ? <TypingDots /> : content}
      </div>
      {isUser && (
        <div style={{
          width: 32, height: 32, borderRadius: "50%",
          background: "#3d3d3d",
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "#ccc", flexShrink: 0, marginLeft: 12, marginTop: 2,
          fontSize: 13, fontWeight: 600,
        }}>
          U
        </div>
      )}
    </div>
  );
}

// ── Welcome screen ────────────────────────────────────────────────────────────
function WelcomeScreen({ onPrompt }) {
  const suggestions = [
    "Explain quantum computing simply",
    "Write a Python function to sort a list",
    "What's the difference between AI and ML?",
    "Give me 5 business ideas for 2025",
  ];
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", flex: 1, gap: 32, padding: "40px 20px" }}>
      <div style={{ textAlign: "center" }}>
        <div style={{
          width: 60, height: 60, borderRadius: "50%",
          background: "linear-gradient(135deg, #10a37f, #1a7f64)",
          display: "flex", alignItems: "center", justifyContent: "center",
          margin: "0 auto 16px",
          boxShadow: "0 4px 24px rgba(16,163,127,0.35)",
        }}>
          <BotIcon size={28} />
        </div>
        <h1 style={{ color: "#ececec", fontSize: 26, fontWeight: 600, marginBottom: 6 }}>
          How can I help you today?
        </h1>
        <p style={{ color: "#888", fontSize: 14 }}>Powered by LangGraph + GPT-4o-mini</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, width: "100%", maxWidth: 560 }}>
        {suggestions.map((s, i) => (
          <button key={i} onClick={() => onPrompt(s)} style={{
            background: "#2a2a2a",
            border: "1px solid #3d3d3d",
            borderRadius: 12,
            padding: "12px 16px",
            color: "#ccc",
            fontSize: 13,
            textAlign: "left",
            cursor: "pointer",
            transition: "all 0.18s ease",
            lineHeight: 1.5,
          }}
            onMouseEnter={e => { e.currentTarget.style.background = "#333"; e.currentTarget.style.borderColor = "#555"; }}
            onMouseLeave={e => { e.currentTarget.style.background = "#2a2a2a"; e.currentTarget.style.borderColor = "#3d3d3d"; }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

// ── App ────────────────────────────────────────────────────────────────────────
export default function App() {
  const [conversations, setConversations] = useState([]);   // [{id, title, messages, history}]
  const [activeId, setActiveId] = useState(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [statusText, setStatusText] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const textareaRef = useRef(null);

  const activeConv = conversations.find(c => c.id === activeId) || null;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations, loading]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 160) + "px";
    }
  }, [input]);

  function newChat() {
    setActiveId(null);
    setInput("");
    inputRef.current?.focus();
  }

  function switchConv(id) {
    setActiveId(id);
  }

  function updateConv(id, updater) {
    setConversations(prev => prev.map(c => c.id === id ? { ...c, ...updater(c) } : c));
  }

  async function sendMessage(overrideText) {
    const text = (overrideText ?? input).trim();
    if (!text || loading) return;
    setInput("");

    let convId = activeId;

    // Create new conversation if none active
    if (!convId) {
      convId = makeId();
      const newConv = {
        id: convId,
        title: makeTitle(text),
        messages: [],
        history: [],
      };
      setConversations(prev => [newConv, ...prev]);
      setActiveId(convId);
    }

    // Add user message
    const userMsg = { role: "user", content: text };
    updateConv(convId, c => ({ messages: [...c.messages, userMsg] }));

    setLoading(true);
    setStatusText("▶ llm_node — Calling GPT-4o-mini…");

    let reply = "Sorry, something went wrong.";
    try {
      const currentConv = conversations.find(c => c.id === convId);
      const history = currentConv?.history ?? [];
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: text, thread_id: convId, history }),
      });
      const data = await res.json();
      reply = data.response;
    } catch (e) {
      reply = `⚠️ Cannot reach backend at ${API_URL}.\nMake sure FastAPI is running:\n  python -m uvicorn backend.main:app --reload --port 8000`;
    }

    const aiMsg = { role: "ai", content: reply };
    updateConv(convId, c => ({
      messages: [...c.messages, userMsg, aiMsg],
      history: [...c.history, { role: "user", content: text }, { role: "assistant", content: reply }],
    }));

    setStatusText("");
    setLoading(false);
    inputRef.current?.focus();
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  // Get fresh messages (after state updates)
  const displayMessages = activeConv
    ? activeConv.messages.filter(m =>
        !activeConv.messages.slice(activeConv.messages.lastIndexOf(m) + 1).some(x => x.role === m.role)
        || true
      )
    : [];

  // Actually get messages from activeConv fresh each render
  const msgs = activeConv?.messages ?? [];

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html, body, #root {
          height: 100%; width: 100%;
          font-family: 'Inter', -apple-system, sans-serif;
          background: #212121;
          color: #ececec;
        }
        #root { display: flex; }
        textarea { resize: none; font-family: inherit; }
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes dotBounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #444; border-radius: 99px; }
        button { cursor: pointer; border: none; outline: none; }
        input, textarea { outline: none; }
      `}</style>

      {/* ── Sidebar ── */}
      {sidebarOpen && (
        <aside style={{
          width: 260,
          background: "#171717",
          display: "flex",
          flexDirection: "column",
          borderRight: "1px solid #2a2a2a",
          flexShrink: 0,
        }}>
          {/* New Chat button */}
          <div style={{ padding: "12px 10px 8px" }}>
            <button
              onClick={newChat}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "10px 14px",
                borderRadius: 10,
                background: "transparent",
                color: "#ececec",
                fontSize: 13.5,
                fontWeight: 500,
                transition: "background 0.15s",
                border: "1px solid #3d3d3d",
              }}
              onMouseEnter={e => e.currentTarget.style.background = "#2a2a2a"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}
            >
              <PlusIcon />
              New chat
            </button>
          </div>

          {/* Conversation list */}
          <div style={{ flex: 1, overflowY: "auto", padding: "4px 8px" }}>
            {conversations.length === 0 && (
              <p style={{ color: "#555", fontSize: 12, padding: "12px 8px" }}>No conversations yet</p>
            )}
            {conversations.map(conv => (
              <button
                key={conv.id}
                onClick={() => switchConv(conv.id)}
                style={{
                  width: "100%",
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  padding: "9px 10px",
                  borderRadius: 8,
                  background: activeId === conv.id ? "#2a2a2a" : "transparent",
                  color: activeId === conv.id ? "#ececec" : "#aaa",
                  fontSize: 13,
                  textAlign: "left",
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  textOverflow: "ellipsis",
                  transition: "all 0.15s",
                  marginBottom: 2,
                }}
                onMouseEnter={e => { if (activeId !== conv.id) e.currentTarget.style.background = "#222"; }}
                onMouseLeave={e => { if (activeId !== conv.id) e.currentTarget.style.background = "transparent"; }}
              >
                <span style={{ flexShrink: 0, opacity: 0.6 }}><ChatIcon /></span>
                <span style={{ overflow: "hidden", textOverflow: "ellipsis" }}>{conv.title}</span>
              </button>
            ))}
          </div>

          {/* Sidebar footer */}
          <div style={{
            padding: "12px 14px",
            borderTop: "1px solid #2a2a2a",
            display: "flex", alignItems: "center", gap: 10,
          }}>
            <div style={{
              width: 30, height: 30, borderRadius: "50%",
              background: "linear-gradient(135deg, #10a37f, #1a7f64)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 11, fontWeight: 700, color: "#fff",
            }}>U</div>
            <span style={{ fontSize: 13, color: "#aaa" }}>User</span>
          </div>
        </aside>
      )}

      {/* ── Main area ── */}
      <main style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", position: "relative" }}>

        {/* Top bar */}
        <div style={{
          padding: "12px 20px",
          display: "flex",
          alignItems: "center",
          gap: 12,
          borderBottom: "1px solid #2a2a2a",
          background: "#212121",
          flexShrink: 0,
        }}>
          <button
            onClick={() => setSidebarOpen(o => !o)}
            style={{
              background: "transparent",
              color: "#888",
              padding: 6,
              borderRadius: 6,
              fontSize: 18,
              lineHeight: 1,
              transition: "color 0.15s",
            }}
            onMouseEnter={e => e.currentTarget.style.color = "#fff"}
            onMouseLeave={e => e.currentTarget.style.color = "#888"}
          >
            ☰
          </button>
          <span style={{ fontSize: 14, fontWeight: 500, color: "#ccc" }}>
            {activeConv ? activeConv.title : "LangGraph Chatbot"}
          </span>
          <span style={{
            marginLeft: "auto",
            fontSize: 11,
            color: "#555",
            background: "#2a2a2a",
            border: "1px solid #3a3a3a",
            borderRadius: 6,
            padding: "3px 8px",
            fontFamily: "monospace",
          }}>gpt-4o-mini</span>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: "24px 0" }}>
          <div style={{ maxWidth: 720, margin: "0 auto", padding: "0 20px" }}>
            {!activeConv ? (
              <WelcomeScreen onPrompt={(text) => { setInput(text); setTimeout(() => sendMessage(text), 0); }} />
            ) : (
              <>
                {msgs.map((m, i) => (
                  <Message key={i} role={m.role} content={m.content} />
                ))}
                {loading && <Message role="ai" content="" isTyping />}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Status bar */}
        {statusText && (
          <div style={{
            textAlign: "center",
            fontSize: 11,
            color: "#10a37f",
            fontFamily: "monospace",
            padding: "4px",
            background: "#212121",
          }}>
            {statusText}
          </div>
        )}

        {/* Input area */}
        <div style={{
          padding: "12px 20px 20px",
          background: "#212121",
          flexShrink: 0,
        }}>
          <div style={{
            maxWidth: 720,
            margin: "0 auto",
            background: "#2f2f2f",
            border: "1px solid #444",
            borderRadius: 16,
            display: "flex",
            alignItems: "flex-end",
            gap: 10,
            padding: "12px 14px",
            boxShadow: "0 2px 16px rgba(0,0,0,0.3)",
            transition: "border-color 0.2s",
          }}>
            <textarea
              ref={el => { inputRef.current = el; textareaRef.current = el; }}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message LangGraph Chatbot…"
              disabled={loading}
              rows={1}
              style={{
                flex: 1,
                background: "transparent",
                border: "none",
                color: "#ececec",
                fontSize: 14.5,
                lineHeight: 1.6,
                maxHeight: 160,
                overflowY: "auto",
              }}
            />
            <button
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
              style={{
                width: 36, height: 36,
                borderRadius: 10,
                background: input.trim() && !loading
                  ? "linear-gradient(135deg, #10a37f, #0d8f6e)"
                  : "#444",
                color: input.trim() && !loading ? "#fff" : "#666",
                display: "flex", alignItems: "center", justifyContent: "center",
                flexShrink: 0,
                transition: "all 0.15s",
                boxShadow: input.trim() && !loading ? "0 2px 8px rgba(16,163,127,0.35)" : "none",
              }}
            >
              <SendIcon />
            </button>
          </div>
          <p style={{ textAlign: "center", fontSize: 11, color: "#555", marginTop: 10 }}>
            Press <kbd style={{ background: "#333", padding: "1px 5px", borderRadius: 4, fontSize: 10 }}>Enter</kbd> to send,&nbsp;
            <kbd style={{ background: "#333", padding: "1px 5px", borderRadius: 4, fontSize: 10 }}>Shift+Enter</kbd> for new line
          </p>
        </div>
      </main>
    </>
  );
}

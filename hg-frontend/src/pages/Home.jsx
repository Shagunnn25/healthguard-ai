export default function Home({ setPage }) {
  const ACCENT  = "#00d2ff";
  const ACCENT2 = "#0055ff";
  const BORDER  = "rgba(0,210,255,0.12)";

  const cards = [
    { icon: "💬", title: "AI Chat",        desc: "Ask health questions, get instant AI-powered answers.", page: "chat" },
    { icon: "🧬", title: "Lab Analyzer",   desc: "Upload or describe lab results for detailed interpretation.", page: "lab" },
    { icon: "🩺", title: "Disease Check",  desc: "Enter symptoms and get a differential diagnosis overview.", page: "disease" },
    { icon: "📄", title: "OCR Reports",    desc: "Scan and extract text from medical documents instantly.", page: "ocr" },
  ];

  return (
    <div style={{
      minHeight: "100vh", width: "100vw",
      background: "#020617",
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center",
      fontFamily: "'DM Sans', sans-serif",
      padding: "40px 20px",
    }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 48 }}>
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 12,
          marginBottom: 20,
        }}>
          <div style={{
            width: 52, height: 52, borderRadius: 14,
            background: `linear-gradient(135deg, ${ACCENT2}, ${ACCENT})`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: "Syne, sans-serif", fontWeight: 800, fontSize: 18,
            color: "#fff", boxShadow: `0 0 24px rgba(0,210,255,0.45)`,
          }}>HG</div>
          <div style={{ textAlign: "left" }}>
            <div style={{ fontFamily: "Syne, sans-serif", fontWeight: 800, fontSize: "1.4rem", color: "#f1f5f9" }}>
              HealthGuard AI
            </div>
            <div style={{ fontSize: "0.72rem", color: ACCENT, letterSpacing: "0.1em" }}>
              MEDICAL INTELLIGENCE PLATFORM
            </div>
          </div>
        </div>

        <h1 style={{
          fontFamily: "Syne, sans-serif", fontWeight: 800,
          fontSize: "clamp(1.8rem, 4vw, 3rem)",
          background: `linear-gradient(90deg, #fff, ${ACCENT})`,
          WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          marginBottom: 12, lineHeight: 1.2,
        }}>
          Your AI Health Assistant
        </h1>
        <p style={{ color: "rgba(148,163,184,0.7)", fontSize: "1rem", maxWidth: 480, margin: "0 auto" }}>
          Powered by advanced medical AI. Ask questions, analyze results, and understand your health.
        </p>
      </div>

      {/* Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: 16, maxWidth: 860, width: "100%", marginBottom: 40,
      }}>
        {cards.map(c => (
          <button key={c.page} onClick={() => setPage?.(c.page)} style={{
            background: "rgba(255,255,255,0.03)",
            border: `1px solid ${BORDER}`,
            borderRadius: 16, padding: "24px 20px",
            textAlign: "left", cursor: "pointer",
            backdropFilter: "blur(12px)",
            transition: "all 0.2s ease",
          }}
            onMouseEnter={e => {
              e.currentTarget.style.background = "rgba(0,210,255,0.06)";
              e.currentTarget.style.borderColor = "rgba(0,210,255,0.35)";
              e.currentTarget.style.transform = "translateY(-3px)";
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = "rgba(255,255,255,0.03)";
              e.currentTarget.style.borderColor = BORDER;
              e.currentTarget.style.transform = "translateY(0)";
            }}
          >
            <div style={{ fontSize: 28, marginBottom: 12 }}>{c.icon}</div>
            <div style={{ fontFamily: "Syne, sans-serif", fontWeight: 700, fontSize: "1rem", color: "#f1f5f9", marginBottom: 6 }}>
              {c.title}
            </div>
            <div style={{ fontSize: "0.82rem", color: "rgba(148,163,184,0.6)", lineHeight: 1.5 }}>
              {c.desc}
            </div>
          </button>
        ))}
      </div>

      {/* CTA */}
      <button onClick={() => setPage?.("chat")} style={{
        padding: "13px 32px",
        background: `linear-gradient(135deg, ${ACCENT2}, ${ACCENT})`,
        border: "none", borderRadius: 12,
        color: "#fff", fontFamily: "Syne, sans-serif",
        fontWeight: 700, fontSize: "0.95rem",
        cursor: "pointer", letterSpacing: "0.03em",
        boxShadow: `0 0 24px rgba(0,210,255,0.35)`,
        transition: "transform 0.15s, box-shadow 0.15s",
      }}
        onMouseEnter={e => { e.currentTarget.style.transform = "scale(1.04)"; e.currentTarget.style.boxShadow = "0 0 36px rgba(0,210,255,0.55)"; }}
        onMouseLeave={e => { e.currentTarget.style.transform = "scale(1)"; e.currentTarget.style.boxShadow = "0 0 24px rgba(0,210,255,0.35)"; }}
      >
        Start Chatting →
      </button>

      <p style={{ marginTop: 20, fontSize: "0.72rem", color: "rgba(100,116,139,0.5)" }}>
        Not a substitute for professional medical advice.
      </p>
    </div>
  );
}
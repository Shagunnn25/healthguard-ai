import { DotLottieReact } from "@lottiefiles/dotlottie-react";

export default function Dashboard({ setPage }) {
  const cards = [
    { title: "Disease", icon: "🧠", page: "disease" },
    { title: "Lab", icon: "🧪", page: "lab" },
    { title: "OCR", icon: "📄", page: "ocr" },
    { title: "Q&A", icon: "❓", page: "qa" },
    { title: "AI Chat", icon: "💬", page: "chat" },
  ];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#020617",
      color: "white",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden"
    }}>

      {/* 🔥 BACKGROUND ANIMATION */}
      <div style={{
        position: "absolute",
        inset: 0,
        opacity: 0.08,
        pointerEvents: "none",  // 🔥 VERY IMPORTANT
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}>
        <DotLottieReact
          src="https://lottie.host/15051b44-1c40-43a2-89fd-bee01bae6007/MZbYBzGSWQ.lottie"
          autoplay
          loop
          style={{ width: 500 }}
        />
      </div>

      {/* CONTENT */}
      <div style={{ position: "relative", zIndex: 2 }}>

        <h1 style={{
          fontSize: "2.5rem",
          marginBottom: "40px",
          textAlign: "center",
          background: "linear-gradient(90deg, #00c6ff, #ffd700)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent"
        }}>
          Health Dashboard
        </h1>

        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 200px))",
          gap: "25px",
          justifyContent: "center"
        }}>
          {cards.map((card) => (
            <div
              key={card.title}
              onClick={() => setPage(card.page)}
              style={{
                height: "160px",
                width: "200px",
                borderRadius: "18px",
                cursor: "pointer",

                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",

                background: "rgba(255,255,255,0.05)",
                backdropFilter: "blur(20px)",
                border: "1px solid rgba(255,255,255,0.1)",

                transition: "all 0.3s ease"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "scale(1.08)";
                e.currentTarget.style.boxShadow =
                  "0 0 25px rgba(0,200,255,0.6), 0 0 40px rgba(255,215,0,0.3)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "scale(1)";
                e.currentTarget.style.boxShadow = "none";
              }}
            >
              <div style={{ fontSize: "2rem" }}>{card.icon}</div>
              <h3 style={{ marginTop: "10px" }}>{card.title}</h3>
            </div>
          ))}
        </div>

        <div style={{ textAlign: "center" }}>
          <button
            onClick={() => setPage("home")}
            style={{
              marginTop: "40px",
              padding: "10px 20px",
              borderRadius: "10px",
              border: "none",
              cursor: "pointer",
              background: "#1e293b",
              color: "white"
            }}
          >
            Back Home
          </button>
        </div>

      </div>
    </div>
  );
}
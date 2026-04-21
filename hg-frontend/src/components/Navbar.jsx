export default function Navbar({ setPage }) {
  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      padding: "15px 20px",
      display: "flex",
      justifyContent: "space-between",
      background: "#111",
      color: "white"
    }}>
      <h3>HealthGuard AI</h3>
      <button>Dashboard</button>
    </div>
  );
}
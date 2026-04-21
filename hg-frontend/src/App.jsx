import { useState } from "react";
import Chat from "./pages/Chat";
import Home from "./pages/Home";

function App() {
  const [page, setPage] = useState("chat");

  return (
    <>
      {page === "chat" && <Chat setPage={setPage} />}
      {page === "home" && <Home setPage={setPage} />}
    </>
  );
}

export default App;
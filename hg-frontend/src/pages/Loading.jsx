import { useEffect } from "react";
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export default function Loading({ setPage }) {

  useEffect(() => {
    const timer = setTimeout(() => {
      setPage("dashboard");
    }, 2500); // 2.5 sec animation

    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{
      height:"100vh",
      display:"flex",
      justifyContent:"center",
      alignItems:"center",
      background:"#020617"
    }}>

      <DotLottieReact
        src="https://lottie.host/0cd6e0b6-c757-441e-87f8-ce95d7a19428/Z8nTxruVou.lottie"
        autoplay
        loop
        style={{ width:300 }}
      />

    </div>
  );
}
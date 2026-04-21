import React from "react";
import { DotLottieReact } from "@lottiefiles/dotlottie-react";

export default function BackgroundAnimation({ src }) {
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: 0.15,
        zIndex: 0,
        pointerEvents: "none",
      }}
    >
      <DotLottieReact src={src} loop autoplay />
    </div>
  );
}
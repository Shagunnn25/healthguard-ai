import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export default function Lab({ setPage }) {
  return (
    <div style={container}>

      <DotLottieReact
        src="https://lottie.host/ce742026-b89b-4d25-bbaa-0bd9b724260e/pWiZzQBUSm.lottie"
        autoplay loop
        style={bg}
      />

      <div style={content}>
        <Back setPage={setPage} />

        <h1>🧪 Lab Analyzer</h1>

        <input placeholder="Enter lab values..." style={input} />

        <button style={btn}>Analyze</button>
      </div>
    </div>
  );
}
export default function QA({ setPage }) {
  return (
    <div style={container}>
      <div style={content}>
        <Back setPage={setPage} />

        <h1>❓ Medical Q&A</h1>

        <input placeholder="Ask anything..." style={input} />

        <button style={btn}>Ask</button>
      </div>
    </div>
  );
}
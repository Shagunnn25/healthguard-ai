export default function Card({ title, onClick }) {
  return (
    <div className="card glass" onClick={onClick}>
      <h2>{title}</h2>
    </div>
  );
}
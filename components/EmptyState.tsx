export default function EmptyState() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 24px",
        gap: "16px",
        textAlign: "center",
      }}
    >
      <div
        style={{
          width: "64px",
          height: "64px",
          borderRadius: "50%",
          background: "var(--bg-tertiary)",
          border: "1px solid var(--border)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "28px",
        }}
      >
        🎙️
      </div>
      <div>
        <p style={{ color: "var(--text-primary)", fontWeight: 500, marginBottom: "4px" }}>
          Sin evaluaciones aún
        </p>
        <p style={{ color: "var(--text-muted)", fontSize: "13px" }}>
          Sube un audio de venta para comenzar la evaluación IA
        </p>
      </div>
    </div>
  );
}

"use client";

type Status = "processing" | "completed" | "error";

const config: Record<Status, { label: string; color: string; pulse: boolean }> = {
  processing: { label: "Procesando", color: "#FFB800", pulse: true },
  completed: { label: "Completado", color: "#22FF44", pulse: false },
  error: { label: "Error", color: "#FF4444", pulse: false },
};

export default function StatusBadge({ status }: { status: Status }) {
  const { label, color, pulse } = config[status] ?? config.error;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "6px",
        padding: "2px 10px",
        borderRadius: "999px",
        border: `1px solid ${color}33`,
        background: `${color}11`,
        color,
        fontSize: "11px",
        fontWeight: 500,
        letterSpacing: "0.04em",
        textTransform: "uppercase",
      }}
    >
      <span
        style={{
          width: "6px",
          height: "6px",
          borderRadius: "50%",
          backgroundColor: color,
          animation: pulse ? "pulse-green 1.4s ease-in-out infinite" : undefined,
        }}
      />
      {label}
    </span>
  );
}

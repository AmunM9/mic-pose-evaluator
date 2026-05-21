"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import ScoreBar from "@/components/ScoreBar";
import StatusBadge from "@/components/StatusBadge";
import { deleteEvaluation, getEvaluation } from "@/lib/api";
import { formatDateLong } from "@/lib/format";
import { EvaluationDetail } from "@/types";

function scoreColor(score: number | null): string {
  if (score === null) return "var(--text-muted)";
  if (score >= 8) return "#22FF44";
  if (score >= 5) return "#FFB800";
  return "#FF4444";
}

export default function EvaluationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [evaluation, setEvaluation] = useState<EvaluationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    getEvaluation(Number(id))
      .then(setEvaluation)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    setDeleting(true);
    try {
      await deleteEvaluation(Number(id));
      router.push("/");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al eliminar");
      setDeleting(false);
    }
  }

  if (loading) {
    return (
      <div style={{ padding: "40px 24px", color: "var(--text-muted)", textAlign: "center" }}>
        Cargando evaluación...
      </div>
    );
  }

  if (error || !evaluation) {
    return (
      <div style={{ padding: "40px 24px", textAlign: "center" }}>
        <p style={{ color: "#FF4444", marginBottom: "16px" }}>{error ?? "No encontrada"}</p>
        <Link href="/" style={{ color: "var(--accent-primary)" }}>
          ← Volver al inicio
        </Link>
      </div>
    );
  }

  const scoreCol = scoreColor(evaluation.overall_score);

  return (
    <div style={{ minHeight: "100vh", padding: "0 24px 60px", maxWidth: "900px", margin: "0 auto" }}>
      {/* Header */}
      <header style={{ borderBottom: "1px solid var(--border)", padding: "20px 0", marginBottom: "32px" }}>
        <Link
          href="/"
          style={{
            color: "var(--text-secondary)",
            fontSize: "13px",
            display: "inline-flex",
            alignItems: "center",
            gap: "6px",
          }}
        >
          ← Evaluaciones
        </Link>
      </header>

      {/* Title row */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: "16px",
          marginBottom: "32px",
          flexWrap: "wrap",
        }}
      >
        <div>
          <h1 style={{ fontSize: "20px", fontWeight: 600, marginBottom: "8px" }}>
            {evaluation.filename}
          </h1>
          <div style={{ display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
            <StatusBadge status={evaluation.status} />
            <span style={{ color: "var(--text-muted)", fontSize: "12px" }}>
              {formatDateLong(evaluation.created_at)}
            </span>
          </div>
        </div>

        {/* Overall score */}
        {evaluation.overall_score !== null && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              background: "var(--bg-secondary)",
              border: `1px solid ${scoreCol}33`,
              borderRadius: "12px",
              padding: "16px 24px",
              boxShadow: `0 0 24px ${scoreCol}18`,
            }}
          >
            <span
              style={{
                fontSize: "40px",
                fontWeight: 700,
                color: scoreCol,
                lineHeight: 1,
                fontFamily: '"JetBrains Mono", monospace',
              }}
            >
              {evaluation.overall_score.toFixed(1)}
            </span>
            <span style={{ color: "var(--text-muted)", fontSize: "11px", marginTop: "4px" }}>
              / 10 promedio
            </span>
          </div>
        )}
      </div>

      {/* Transcript */}
      {evaluation.transcript && (
        <section style={{ marginBottom: "32px" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              marginBottom: "12px",
            }}
          >
            <h2
              style={{
                fontSize: "12px",
                fontWeight: 500,
                color: "var(--text-secondary)",
                textTransform: "uppercase",
                letterSpacing: "0.08em",
              }}
            >
              Transcripción
            </h2>
            {evaluation.speaker_count > 1 && (
              <span
                style={{
                  fontSize: "11px",
                  color: "var(--text-muted)",
                  background: "var(--bg-tertiary)",
                  border: "1px solid var(--border)",
                  borderRadius: "4px",
                  padding: "1px 7px",
                }}
              >
                {evaluation.speaker_count} speakers
              </span>
            )}
          </div>
          <div
            style={{
              background: "var(--bg-secondary)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              padding: "20px",
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: "13px",
              lineHeight: "1.9",
              maxHeight: "320px",
              overflowY: "auto",
              display: "flex",
              flexDirection: "column",
              gap: "2px",
            }}
          >
            {evaluation.transcript.split("\n").map((line, i) => {
              const isVendedor = line.startsWith("VENDEDOR:");
              const isCliente = line.startsWith("CLIENTE:");
              const colonIdx = line.indexOf(":");
              const label = colonIdx !== -1 ? line.slice(0, colonIdx + 1) : null;
              const text = colonIdx !== -1 ? line.slice(colonIdx + 1) : line;

              return (
                <div key={i} style={{ display: "flex", gap: "8px", wordBreak: "break-word" }}>
                  {label && (
                    <span
                      style={{
                        color: isVendedor ? "#22FF44" : isCliente ? "#888888" : "var(--text-muted)",
                        fontWeight: 600,
                        flexShrink: 0,
                        minWidth: "90px",
                      }}
                    >
                      {label}
                    </span>
                  )}
                  <span style={{ color: isVendedor ? "var(--text-primary)" : "var(--text-secondary)" }}>
                    {text}
                  </span>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Rubric results */}
      {evaluation.rubric_results.length > 0 && (
        <section style={{ marginBottom: "40px" }}>
          <h2
            style={{
              fontSize: "12px",
              fontWeight: 500,
              color: "var(--text-secondary)",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: "16px",
            }}
          >
            Evaluación por criterio
          </h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
              gap: "12px",
            }}
          >
            {evaluation.rubric_results.map((r) => (
              <div
                key={r.id}
                style={{
                  background: "var(--bg-secondary)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  padding: "16px",
                }}
              >
                <p style={{ fontWeight: 500, marginBottom: "10px", fontSize: "14px" }}>
                  {r.criterion.name}
                </p>
                <ScoreBar score={r.score} maxScore={r.criterion.max_score} />
                <p
                  style={{
                    color: "var(--text-muted)",
                    fontSize: "12px",
                    marginTop: "10px",
                    lineHeight: "1.6",
                  }}
                >
                  {r.feedback}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Error message */}
      {evaluation.error_message && (
        <div
          style={{
            background: "rgba(255,68,68,0.08)",
            border: "1px solid rgba(255,68,68,0.3)",
            borderRadius: "8px",
            padding: "16px",
            marginBottom: "32px",
            color: "#FF4444",
            fontSize: "13px",
          }}
        >
          Error: {evaluation.error_message}
        </div>
      )}

      {/* Delete */}
      <div style={{ borderTop: "1px solid var(--border)", paddingTop: "24px" }}>
        {!confirmDelete ? (
          <button
            onClick={() => setConfirmDelete(true)}
            style={{
              background: "transparent",
              border: "1px solid rgba(255,68,68,0.4)",
              color: "#FF4444",
              borderRadius: "6px",
              padding: "8px 16px",
              cursor: "pointer",
              fontSize: "13px",
            }}
          >
            Eliminar evaluación
          </button>
        ) : (
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <span style={{ color: "var(--text-secondary)", fontSize: "13px" }}>
              ¿Confirmar eliminación?
            </span>
            <button
              onClick={handleDelete}
              disabled={deleting}
              style={{
                background: "rgba(255,68,68,0.15)",
                border: "1px solid rgba(255,68,68,0.5)",
                color: "#FF4444",
                borderRadius: "6px",
                padding: "6px 14px",
                cursor: deleting ? "not-allowed" : "pointer",
                fontSize: "13px",
              }}
            >
              {deleting ? "Eliminando..." : "Sí, eliminar"}
            </button>
            <button
              onClick={() => setConfirmDelete(false)}
              style={{
                background: "transparent",
                border: "1px solid var(--border)",
                color: "var(--text-secondary)",
                borderRadius: "6px",
                padding: "6px 14px",
                cursor: "pointer",
                fontSize: "13px",
              }}
            >
              Cancelar
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

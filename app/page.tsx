"use client";

import { useEffect, useState } from "react";
import AudioUpload from "@/components/AudioUpload";
import EvaluationCard from "@/components/EvaluationCard";
import EmptyState from "@/components/EmptyState";
import { getEvaluations } from "@/lib/api";
import { EvaluationDetail, EvaluationListItem } from "@/types";

export default function HomePage() {
  const [evaluations, setEvaluations] = useState<EvaluationListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEvaluations()
      .then(setEvaluations)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  function handleNewEvaluation(evaluation: EvaluationDetail) {
    setEvaluations((prev) => [evaluation, ...prev]);
  }

  return (
    <div style={{ minHeight: "100vh", padding: "0 24px 48px" }}>
      {/* Header */}
      <header
        style={{
          borderBottom: "1px solid var(--border)",
          padding: "20px 0",
          marginBottom: "40px",
          display: "flex",
          alignItems: "center",
          gap: "12px",
        }}
      >
        <span style={{ fontSize: "20px" }}>🎙️</span>
        <h1
          style={{
            fontSize: "18px",
            fontWeight: 600,
            color: "var(--text-primary)",
            letterSpacing: "-0.02em",
          }}
        >
          Evaluador Comercial
        </h1>
        <span
          style={{
            background: "rgba(34,255,68,0.12)",
            border: "1px solid var(--border-accent)",
            color: "var(--accent-primary)",
            fontSize: "10px",
            fontWeight: 600,
            padding: "2px 8px",
            borderRadius: "4px",
            letterSpacing: "0.06em",
            textTransform: "uppercase",
          }}
        >
          AI
        </span>
        <span style={{ color: "var(--text-muted)", fontSize: "13px", marginLeft: "4px" }}>
          Mic&amp;Pose
        </span>
      </header>

      {/* Main grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "clamp(300px, 40%, 480px) 1fr",
          gap: "40px",
          maxWidth: "1200px",
          margin: "0 auto",
        }}
      >
        {/* Left: Upload */}
        <div>
          <h2
            style={{
              fontSize: "13px",
              fontWeight: 500,
              color: "var(--text-secondary)",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: "16px",
            }}
          >
            Subir audio
          </h2>
          <AudioUpload onSuccess={handleNewEvaluation} />

          <div
            style={{
              marginTop: "24px",
              background: "var(--bg-secondary)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              padding: "16px",
            }}
          >
            <p
              style={{
                color: "var(--text-secondary)",
                fontSize: "12px",
                lineHeight: "1.7",
              }}
            >
              Sube una grabación de una conversación de venta. El sistema la transcribirá con
              Whisper y evaluará 5 criterios comerciales usando GPT-4o-mini.
            </p>
          </div>
        </div>

        {/* Right: List */}
        <div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              marginBottom: "16px",
            }}
          >
            <h2
              style={{
                fontSize: "13px",
                fontWeight: 500,
                color: "var(--text-secondary)",
                textTransform: "uppercase",
                letterSpacing: "0.08em",
              }}
            >
              Evaluaciones
            </h2>
            {evaluations.length > 0 && (
              <span
                style={{
                  background: "var(--bg-tertiary)",
                  color: "var(--text-muted)",
                  fontSize: "11px",
                  padding: "2px 8px",
                  borderRadius: "4px",
                }}
              >
                {evaluations.length}
              </span>
            )}
          </div>

          {loading ? (
            <p style={{ color: "var(--text-muted)", fontSize: "13px" }}>Cargando...</p>
          ) : evaluations.length === 0 ? (
            <div
              style={{
                background: "var(--bg-secondary)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
              }}
            >
              <EmptyState />
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
              {evaluations.map((ev) => (
                <EvaluationCard key={ev.id} evaluation={ev} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Responsive */}
      <style>{`
        @media (max-width: 768px) {
          div[style*="grid-template-columns"] {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </div>
  );
}

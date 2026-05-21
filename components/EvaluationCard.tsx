"use client";

import Link from "next/link";
import { formatDate } from "@/lib/format";
import { EvaluationListItem } from "@/types";
import StatusBadge from "./StatusBadge";

function scoreColor(score: number | null): string {
  if (score === null) return "var(--text-muted)";
  if (score >= 8) return "#22FF44";
  if (score >= 5) return "#FFB800";
  return "#FF4444";
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function EvaluationCard({ evaluation }: { evaluation: EvaluationListItem }) {
  const color = scoreColor(evaluation.overall_score);

  return (
    <Link href={`/evaluations/${evaluation.id}`} style={{ textDecoration: "none" }}>
      <div
        style={{
          background: "var(--bg-secondary)",
          border: "1px solid var(--border)",
          borderRadius: "8px",
          padding: "16px",
          cursor: "pointer",
          transition: "border-color 0.2s, box-shadow 0.2s",
          display: "flex",
          alignItems: "center",
          gap: "16px",
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(34,255,68,0.2)";
          (e.currentTarget as HTMLDivElement).style.boxShadow = "0 0 20px rgba(34,255,68,0.08)";
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLDivElement).style.borderColor = "var(--border)";
          (e.currentTarget as HTMLDivElement).style.boxShadow = "none";
        }}
      >
        {/* Score circle */}
        <div
          style={{
            width: "48px",
            height: "48px",
            borderRadius: "50%",
            border: `2px solid ${color}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            background: `${color}11`,
          }}
        >
          <span
            style={{
              fontSize: "14px",
              fontWeight: 700,
              color,
              fontFamily: '"JetBrains Mono", monospace',
            }}
          >
            {evaluation.overall_score !== null ? evaluation.overall_score.toFixed(1) : "—"}
          </span>
        </div>

        {/* Info */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <p
            style={{
              color: "var(--text-primary)",
              fontWeight: 500,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              marginBottom: "4px",
            }}
          >
            {evaluation.filename}
          </p>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            <span style={{ color: "var(--text-muted)", fontSize: "12px" }}>
              {formatBytes(evaluation.file_size_bytes)}
            </span>
            <span style={{ color: "var(--text-muted)", fontSize: "12px" }}>·</span>
            <span style={{ color: "var(--text-muted)", fontSize: "12px" }}>
              {formatDate(evaluation.created_at)}
            </span>
          </div>
        </div>

        <StatusBadge status={evaluation.status} />
      </div>
    </Link>
  );
}

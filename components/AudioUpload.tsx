"use client";

import { useRef, useState } from "react";
import { uploadAudio } from "@/lib/api";
import { EvaluationDetail } from "@/types";

const ACCEPTED = ".mp3,.wav,.m4a,.webm";

interface AudioUploadProps {
  onSuccess: (evaluation: EvaluationDetail) => void;
}

export default function AudioUpload({ onSuccess }: AudioUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleUpload(file: File) {
    setSelectedFile(file);
    setError(null);
    setLoading(true);
    try {
      const result = await uploadAudio(file);
      onSuccess(result);
      setSelectedFile(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
  }

  function onDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleUpload(file);
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Zona drag & drop */}
      <div
        onClick={() => !loading && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        style={{
          border: `2px dashed ${isDragging ? "var(--accent-primary)" : "var(--border)"}`,
          borderRadius: "12px",
          padding: "40px 24px",
          textAlign: "center",
          cursor: loading ? "not-allowed" : "pointer",
          background: isDragging ? "rgba(34,255,68,0.04)" : "var(--bg-secondary)",
          transition: "border-color 0.2s, background 0.2s",
          boxShadow: isDragging ? "var(--glow)" : undefined,
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          style={{ display: "none" }}
          onChange={onFileChange}
          disabled={loading}
        />

        {loading ? (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "12px" }}>
            <div
              style={{
                width: "32px",
                height: "32px",
                border: "2px solid var(--border)",
                borderTopColor: "var(--accent-primary)",
                borderRadius: "50%",
                animation: "spin 0.8s linear infinite",
              }}
            />
            <p style={{ color: "var(--accent-primary)", fontWeight: 500 }}>
              Transcribiendo audio...
            </p>
            <p style={{ color: "var(--text-muted)", fontSize: "12px" }}>
              {selectedFile?.name}
            </p>
          </div>
        ) : (
          <>
            <div style={{ fontSize: "32px", marginBottom: "12px" }}>🎙️</div>
            <p style={{ color: "var(--text-primary)", fontWeight: 500, marginBottom: "6px" }}>
              Arrastra tu audio aquí
            </p>
            <p style={{ color: "var(--text-muted)", fontSize: "12px", marginBottom: "12px" }}>
              o haz clic para seleccionar
            </p>
            <p style={{ color: "var(--text-muted)", fontSize: "11px" }}>
              MP3, WAV, M4A, WEBM · Máx. 25 MB
            </p>
          </>
        )}
      </div>

      {/* Error */}
      {error && (
        <div
          style={{
            background: "rgba(255,68,68,0.08)",
            border: "1px solid rgba(255,68,68,0.3)",
            borderRadius: "8px",
            padding: "12px 16px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: "12px",
          }}
        >
          <p style={{ color: "#FF4444", fontSize: "13px" }}>{error}</p>
          <button
            onClick={() => { setError(null); setSelectedFile(null); }}
            style={{
              background: "transparent",
              border: "1px solid rgba(255,68,68,0.4)",
              color: "#FF4444",
              borderRadius: "4px",
              padding: "4px 10px",
              cursor: "pointer",
              fontSize: "12px",
              whiteSpace: "nowrap",
            }}
          >
            Reintentar
          </button>
        </div>
      )}

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}

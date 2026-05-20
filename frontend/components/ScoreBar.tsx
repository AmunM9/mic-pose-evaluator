"use client";

import { useEffect, useState } from "react";

function scoreColor(score: number): string {
  if (score >= 8) return "#22FF44";
  if (score >= 5) return "#FFB800";
  return "#FF4444";
}

interface ScoreBarProps {
  score: number;
  maxScore?: number;
}

export default function ScoreBar({ score, maxScore = 10 }: ScoreBarProps) {
  const [width, setWidth] = useState(0);
  const percent = Math.round((score / maxScore) * 100);
  const color = scoreColor(score);

  // Animar al montar: parte de 0% y llega al valor real
  useEffect(() => {
    const timer = setTimeout(() => setWidth(percent), 50);
    return () => clearTimeout(timer);
  }, [percent]);

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
      <div
        style={{
          flex: 1,
          height: "6px",
          borderRadius: "3px",
          background: "var(--bg-tertiary)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${width}%`,
            background: color,
            borderRadius: "3px",
            transition: "width 0.7s cubic-bezier(0.4, 0, 0.2, 1)",
            boxShadow: width > 0 ? `0 0 8px ${color}66` : undefined,
          }}
        />
      </div>
      <span
        style={{
          minWidth: "32px",
          textAlign: "right",
          fontSize: "13px",
          fontWeight: 600,
          color,
          fontFamily: '"JetBrains Mono", monospace',
        }}
      >
        {score.toFixed(1)}
      </span>
    </div>
  );
}

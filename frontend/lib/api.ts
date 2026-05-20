import { EvaluationDetail, EvaluationListItem } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function uploadAudio(file: File): Promise<EvaluationDetail> {
  const form = new FormData();
  form.append("file", file);
  return request<EvaluationDetail>("/api/v1/evaluations/upload", {
    method: "POST",
    body: form,
  });
}

export async function getEvaluations(): Promise<EvaluationListItem[]> {
  return request<EvaluationListItem[]>("/api/v1/evaluations");
}

export async function getEvaluation(id: number): Promise<EvaluationDetail> {
  return request<EvaluationDetail>(`/api/v1/evaluations/${id}`);
}

export async function deleteEvaluation(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/evaluations/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
}

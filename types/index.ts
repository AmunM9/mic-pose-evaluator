export interface RubricCriterion {
  id: number;
  name: string;
  description: string;
  max_score: number;
}

export interface RubricResult {
  id: number;
  criterion_id: number;
  score: number;
  feedback: string;
  criterion: RubricCriterion;
}

export interface EvaluationListItem {
  id: number;
  filename: string;
  file_size_bytes: number;
  overall_score: number | null;
  status: "processing" | "completed" | "error";
  created_at: string;
}

export interface EvaluationDetail extends EvaluationListItem {
  transcript: string | null;
  speaker_count: number;
  error_message: string | null;
  updated_at: string;
  rubric_results: RubricResult[];
}

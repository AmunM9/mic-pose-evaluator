// La API devuelve datetimes sin sufijo de timezone (ej: "2026-05-21T20:44:00").
// Sin el Z, JS los interpreta como hora local en vez de UTC, lo que da un offset
// de 5 horas en Colombia. Forzamos UTC antes de parsear.
function toUTC(iso: string): Date {
  if (iso.endsWith("Z") || iso.includes("+") || iso.match(/-\d{2}:\d{2}$/)) {
    return new Date(iso);
  }
  return new Date(iso + "Z");
}

export function formatDate(iso: string): string {
  return toUTC(iso).toLocaleString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatDateLong(iso: string): string {
  return toUTC(iso).toLocaleString(undefined, {
    day: "2-digit",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

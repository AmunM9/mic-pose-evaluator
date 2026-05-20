# Mic&Pose Evaluator

Microservicio prototipo que transcribe y evalúa conversaciones de venta usando IA.  
Prueba técnica para el rol de **Lead Developer Full-Stack** en Mic&Pose.

## Cómo correr localmente

### Prerrequisitos
- Docker + Docker Compose instalados
- Una API key de OpenAI (`sk-...`)

### Setup (3 pasos)

```bash
# 1. Copiar variables de entorno
cp backend/.env.example backend/.env
# 2. Editar backend/.env y poner tu OPENAI_API_KEY=sk-...
# 3. Levantar todo
OPENAI_API_KEY=sk-... docker compose up --build
```

Abrir [http://localhost:3000](http://localhost:3000)

La API Swagger está en [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Arquitectura

```
Usuario
  │
  ▼
Next.js (puerto 3000)
  │  fetch /api/v1/evaluations/upload
  ▼
FastAPI (puerto 8000)
  ├── gpt-4o-transcribe-diarize  ──→  transcripción + diarización por speaker
  ├── GPT-4o-mini (OpenAI)  ──→  evaluación por 5 criterios
  └── PostgreSQL            ──→  persistencia
```

**Flujo de una evaluación:**
1. Usuario sube audio `.mp3/.wav/.m4a/.webm` desde el browser
2. FastAPI lo recibe, valida extensión y tamaño (máx. 25 MB)
3. Se guarda en `/tmp/uploads/` con nombre UUID (evita colisiones)
4. Se llama a `gpt-4o-transcribe-diarize` → devuelve transcripción con etiquetas VENDEDOR/CLIENTE
5. Se llama a `gpt-4o-mini` con prompt estructurado → devuelve 5 scores + feedback en JSON
6. Se persiste en PostgreSQL (`evaluations` + `rubric_results`)
7. El frontend refresca la lista automáticamente

---

## Decisiones de arquitectura

| Decisión | Alternativa considerada | Por qué esta | Trade-off aceptado |
|---|---|---|---|
| **gpt-4o-mini** para evaluación | gpt-4o | Costo ~$0.00015/1K tokens vs $0.005 de gpt-4o. Para ~300 palabras de transcript = <$0.001/eval | Menor capacidad de razonamiento en casos ambiguos |
| **gpt-4o-transcribe-diarize** para transcripción | whisper-1 | Diarización nativa (detecta hasta 4 speakers) sin librerías externas ni GPU. Mismo precio estimado que whisper-1 (~$0.006/min). Lanzado por OpenAI en octubre 2025. Elimina la necesidad de pyannote.audio + infraestructura de GPU para separar voces | La respuesta `diarized_json` no está soportada en el cliente OpenAI < 1.58 — requiere versión actualizada |
| **SQLAlchemy 2.0 async** | ORM síncrono / queries raw | FastAPI corre en asyncio — un ORM síncrono bloquearía el event loop. asyncpg permite N requests simultáneos con pool de conexiones | Mayor complejidad que queries raw |
| **ECS Fargate** (Terraform) | EC2 con Auto Scaling | Sin gestión de nodos, pago por segundo, escala a 0 fuera de horario. Para early-stage reduce overhead operacional | 20-30% más caro que EC2 Reserved a escala |
| **CloudFront + S3** para frontend | Vercel / EC2 | CDN con 400+ edge locations en LATAM, SSL gratis, cache de assets estáticos, ~$0.01/GB vs $0.085/GB en EC2 | Proceso de deploy más manual que Vercel |
| **Procesamiento síncrono** | Celery + Redis | Simplicidad: cero infraestructura adicional para v1. Un request = un ciclo completo | No escala bien si hay muchos uploads simultáneos |

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0 async |
| Base de datos | PostgreSQL 16 |
| Migraciones | Alembic |
| Transcripción | OpenAI gpt-4o-transcribe-diarize (con diarización) |
| Evaluación | OpenAI GPT-4o-mini |
| Frontend | Next.js 14, TypeScript, CSS custom (sin Tailwind) |
| Infra local | Docker Compose |
| IaC | Terraform (código, no aplicado) |
| CI | GitHub Actions |

---

## Qué dejé fuera para v1 (intencionalmente)

- **Autenticación real** — el schema `users` existe pero sin JWT/OAuth
- **Cola asíncrona** — el procesamiento es síncrono en el request (Celery/RQ para v2)
- **Storage de audios en S3** — se guardan en `/tmp` local (no persisten entre reinicios)
- **Rate limiting** — no hay límite de uploads por IP
- **Tests E2E** — solo unit + integration tests contra DB en memoria

## Qué priorizaría para v2

1. **Cola asíncrona**: Celery + Redis + WebSocket para notificar cuando termine la evaluación
2. **S3 para audios**: presigned URLs, sin pasar el audio por el servidor
3. **Auth con JWT**: registro, login, evaluaciones por usuario
4. **Observabilidad**: Sentry para errores, structured logs con `correlation_id`, métricas por vendedor
5. **Dashboard de métricas**: evolución de scores por criterio en el tiempo

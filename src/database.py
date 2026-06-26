from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

DATABASE_URL_ENV = "DATABASE_URL"


def get_database_backend(db_path: Path) -> dict[str, str | bool]:
    database_url = os.getenv(DATABASE_URL_ENV, "").strip()
    if database_url:
        return {
            "engine": "PostgreSQL",
            "location": "Render PostgreSQL",
            "persistent": True,
            "detail": DATABASE_URL_ENV,
        }
    return {
        "engine": "SQLite",
        "location": str(db_path),
        "persistent": False,
        "detail": "archivo local",
    }


def init_database(db_path: Path) -> None:
    if _database_url():
        _init_postgres()
        return

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_predictions (
                prediction_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                consultor TEXT,
                model_name TEXT,
                model_version TEXT,
                model_file TEXT,
                features_json TEXT NOT NULL,
                prediction REAL,
                actual_value REAL,
                error REAL,
                record_status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                prediction_id TEXT,
                detail TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_prediction_record(db_path: Path, row: dict, feature_columns: Iterable[str]) -> None:
    init_database(db_path)
    features = {feature: row.get(feature) for feature in feature_columns}
    actual_value = _nullable_float(row.get("actual_value"))
    prediction = _nullable_float(row.get("prediction"))
    error = _nullable_float(row.get("error"))

    if _database_url():
        with _connect_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO app_predictions (
                        prediction_id, timestamp, consultor, model_name, model_version, model_file,
                        features_json, prediction, actual_value, error, record_status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT(prediction_id) DO UPDATE SET
                        timestamp = EXCLUDED.timestamp,
                        consultor = EXCLUDED.consultor,
                        model_name = EXCLUDED.model_name,
                        model_version = EXCLUDED.model_version,
                        model_file = EXCLUDED.model_file,
                        features_json = EXCLUDED.features_json,
                        prediction = EXCLUDED.prediction,
                        actual_value = EXCLUDED.actual_value,
                        error = EXCLUDED.error,
                        record_status = EXCLUDED.record_status,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        row.get("prediction_id"),
                        row.get("timestamp"),
                        row.get("consultor"),
                        row.get("model_name"),
                        row.get("model_version"),
                        row.get("model_file"),
                        json.dumps(features, ensure_ascii=False),
                        prediction,
                        actual_value,
                        error,
                        row.get("record_status"),
                    ),
                )
                cur.execute(
                    """
                    INSERT INTO app_events (event_type, prediction_id, detail)
                    VALUES ('prediction_saved', %s, %s)
                    """,
                    (row.get("prediction_id"), "Prediccion guardada desde Streamlit"),
                )
            conn.commit()
        return

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO app_predictions (
                prediction_id, timestamp, consultor, model_name, model_version, model_file,
                features_json, prediction, actual_value, error, record_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(prediction_id) DO UPDATE SET
                timestamp = excluded.timestamp,
                consultor = excluded.consultor,
                model_name = excluded.model_name,
                model_version = excluded.model_version,
                model_file = excluded.model_file,
                features_json = excluded.features_json,
                prediction = excluded.prediction,
                actual_value = excluded.actual_value,
                error = excluded.error,
                record_status = excluded.record_status,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                row.get("prediction_id"),
                row.get("timestamp"),
                row.get("consultor"),
                row.get("model_name"),
                row.get("model_version"),
                row.get("model_file"),
                json.dumps(features, ensure_ascii=False),
                prediction,
                actual_value,
                error,
                row.get("record_status"),
            ),
        )
        conn.execute(
            """
            INSERT INTO app_events (event_type, prediction_id, detail)
            VALUES ('prediction_saved', ?, ?)
            """,
            (row.get("prediction_id"), "Prediccion guardada desde Streamlit"),
        )


def update_actual_value(db_path: Path, prediction_id: str, actual_value: float, prediction: float | None) -> None:
    init_database(db_path)
    error = abs(float(actual_value) - float(prediction)) if prediction is not None else None
    if _database_url():
        with _connect_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE app_predictions
                    SET actual_value = %s,
                        error = %s,
                        record_status = 'validated_for_retraining',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE prediction_id = %s
                    """,
                    (float(actual_value), error, prediction_id),
                )
                cur.execute(
                    """
                    INSERT INTO app_events (event_type, prediction_id, detail)
                    VALUES ('actual_value_updated', %s, %s)
                    """,
                    (prediction_id, "Valor real actualizado"),
                )
            conn.commit()
        return

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE app_predictions
            SET actual_value = ?,
                error = ?,
                record_status = 'validated_for_retraining',
                updated_at = CURRENT_TIMESTAMP
            WHERE prediction_id = ?
            """,
            (float(actual_value), error, prediction_id),
        )
        conn.execute(
            """
            INSERT INTO app_events (event_type, prediction_id, detail)
            VALUES ('actual_value_updated', ?, ?)
            """,
            (prediction_id, "Valor real actualizado"),
        )


def delete_prediction_record(db_path: Path, prediction_id: str) -> None:
    init_database(db_path)
    if _database_url():
        with _connect_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM app_predictions WHERE prediction_id = %s", (prediction_id,))
                cur.execute(
                    """
                    INSERT INTO app_events (event_type, prediction_id, detail)
                    VALUES ('prediction_deleted', %s, %s)
                    """,
                    (prediction_id, "Prediccion eliminada desde la app"),
                )
            conn.commit()
        return

    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM app_predictions WHERE prediction_id = ?", (prediction_id,))
        conn.execute(
            """
            INSERT INTO app_events (event_type, prediction_id, detail)
            VALUES ('prediction_deleted', ?, ?)
            """,
            (prediction_id, "Prediccion eliminada desde la app"),
        )


def get_database_summary(db_path: Path) -> dict[str, int | str | bool]:
    init_database(db_path)
    backend = get_database_backend(db_path)
    if _database_url():
        with _connect_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM app_predictions")
                total = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM app_predictions WHERE actual_value IS NOT NULL")
                validated = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM app_events")
                events = cur.fetchone()[0]
        return {
            "path": backend["location"],
            "engine": backend["engine"],
            "persistent": backend["persistent"],
            "exists": True,
            "total_predictions": int(total),
            "validated_predictions": int(validated),
            "pending_predictions": int(total - validated),
            "events": int(events),
        }

    with sqlite3.connect(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM app_predictions").fetchone()[0]
        validated = conn.execute(
            "SELECT COUNT(*) FROM app_predictions WHERE actual_value IS NOT NULL"
        ).fetchone()[0]
        events = conn.execute("SELECT COUNT(*) FROM app_events").fetchone()[0]
    return {
        "path": str(db_path),
        "engine": backend["engine"],
        "persistent": backend["persistent"],
        "exists": db_path.exists(),
        "total_predictions": int(total),
        "validated_predictions": int(validated),
        "pending_predictions": int(total - validated),
        "events": int(events),
    }


def load_recent_predictions(db_path: Path, limit: int = 25) -> pd.DataFrame:
    init_database(db_path)
    if _database_url():
        with _connect_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        timestamp,
                        consultor,
                        model_name,
                        model_version,
                        prediction,
                        actual_value,
                        error,
                        record_status
                    FROM app_predictions
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                rows = cur.fetchall()
        return pd.DataFrame(
            rows,
            columns=[
                "timestamp",
                "consultor",
                "model_name",
                "model_version",
                "prediction",
                "actual_value",
                "error",
                "record_status",
            ],
        )

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(
            """
            SELECT
                timestamp,
                consultor,
                model_name,
                model_version,
                prediction,
                actual_value,
                error,
                record_status
            FROM app_predictions
            ORDER BY created_at DESC
            LIMIT ?
            """,
            conn,
            params=(limit,),
        )


def load_monitoring_records(db_path: Path) -> pd.DataFrame:
    init_database(db_path)
    columns = [
        "prediction_id",
        "timestamp",
        "consultor",
        "model_name",
        "model_version",
        "model_file",
        "prediction",
        "actual_value",
        "error",
        "record_status",
    ]

    if _database_url():
        with _connect_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        prediction_id,
                        timestamp,
                        consultor,
                        model_name,
                        model_version,
                        model_file,
                        prediction,
                        actual_value,
                        error,
                        record_status
                    FROM app_predictions
                    ORDER BY created_at ASC
                    """
                )
                rows = cur.fetchall()
        return pd.DataFrame(rows, columns=columns)

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(
            """
            SELECT
                prediction_id,
                timestamp,
                consultor,
                model_name,
                model_version,
                model_file,
                prediction,
                actual_value,
                error,
                record_status
            FROM app_predictions
            ORDER BY created_at ASC
            """,
            conn,
        )


def _nullable_float(value) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _database_url() -> str:
    return os.getenv(DATABASE_URL_ENV, "").strip()


def _connect_postgres():
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError(
            "DATABASE_URL esta configurada, pero falta instalar psycopg. "
            "Instala las dependencias de Docker o anade psycopg[binary]."
        ) from exc

    return psycopg.connect(_database_url())


def _init_postgres() -> None:
    with _connect_postgres() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS app_predictions (
                    prediction_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    consultor TEXT,
                    model_name TEXT,
                    model_version TEXT,
                    model_file TEXT,
                    features_json TEXT NOT NULL,
                    prediction DOUBLE PRECISION,
                    actual_value DOUBLE PRECISION,
                    error DOUBLE PRECISION,
                    record_status TEXT,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS app_events (
                    id BIGSERIAL PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    prediction_id TEXT,
                    detail TEXT,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()

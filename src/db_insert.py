import streamlit as st

def get_connection():
    return st.connection("postgresql", type="sql")

def insert_model_test_results(
    conn,
    *,
    dataset_name: str,
    dataset_version: str | None,
    target_column: str,
    model_name: str,
    model_path: str,
    rmse: float,
    mae: float,
    r2: float,
    best_pred,
    y_test,
    row_ids  # <-- IMPORTANTE: aquí pasamos los id reales de X_test
):
    # dataset
    conn.execute("""
        INSERT INTO dataset (name, version, target_column)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (dataset_name, dataset_version, target_column))

    dataset_rows = conn.query("""
        SELECT id
        FROM dataset
        WHERE name=%s
          AND ((version=%s) OR (version IS NULL AND %s IS NULL))
          AND target_column=%s
        LIMIT 1
    """, (dataset_name, dataset_version, dataset_version, target_column))
    dataset_id = int(dataset_rows[0]["id"])

    # run
    run_rows = conn.query("""
        INSERT INTO model_runs (dataset_id, model_name, model_path)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (dataset_id, model_name, str(model_path)))
    run_id = int(run_rows[0]["id"])

    # metrics
    conn.execute("""
        INSERT INTO metrics (model_run_id, split, rmse, mae, r2, overfitting_r2_pct, cumple_overfitting)
        VALUES (%s, 'test', %s, %s, %s, NULL, NULL)
    """, (run_id, float(rmse), float(mae), float(r2)))

    # predictions (loop simple para no romper)
    for row_id, y_true, y_hat in zip(row_ids, y_test, best_pred):
        conn.execute("""
            INSERT INTO predictions (model_run_id, row_id, y_true, y_pred)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (model_run_id, row_id) DO UPDATE
            SET y_true = EXCLUDED.y_true,
                y_pred = EXCLUDED.y_pred
        """, (run_id, int(row_id), float(y_true), float(y_hat)))

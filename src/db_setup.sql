CREATE TABLE IF NOT EXISTS dataset (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  version TEXT,
  target_column TEXT NOT NULL,
  UNIQUE (name, version, target_column)
);

CREATE TABLE IF NOT EXISTS model_runs (
  id SERIAL PRIMARY KEY,
  dataset_id INT NOT NULL REFERENCES dataset(id),
  model_name TEXT NOT NULL,
  model_path TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS metrics (
  id SERIAL PRIMARY KEY,
  model_run_id INT NOT NULL REFERENCES model_runs(id),
  split TEXT NOT NULL CHECK (split IN ('test')),
  rmse DOUBLE PRECISION NOT NULL,
  mae  DOUBLE PRECISION NOT NULL,
  r2   DOUBLE PRECISION NOT NULL,
  overfitting_r2_pct DOUBLE PRECISION,
  cumple_overfitting BOOLEAN
);

CREATE TABLE IF NOT EXISTS predictions (
  id SERIAL PRIMARY KEY,
  model_run_id INT NOT NULL REFERENCES model_runs(id),
  row_id INT NOT NULL,
  y_true DOUBLE PRECISION NOT NULL,
  y_pred DOUBLE PRECISION NOT NULL,
  UNIQUE (model_run_id, row_id)
);

from src.database import (
    delete_prediction_record,
    get_database_summary,
    load_monitoring_records,
    load_recent_predictions,
    save_prediction_record,
    update_actual_value,
)


def test_sqlite_prediction_lifecycle(tmp_path):
    db_path = tmp_path / "flood_app.sqlite"
    row = {
        "prediction_id": "pred_test_1",
        "timestamp": "2026-06-26T10:00:00",
        "consultor": "test",
        "model_name": "Linear Regression Baseline",
        "model_version": "baseline_v1",
        "model_file": "flood_baseline_model.joblib",
        "MonsoonIntensity": 5,
        "TopographyDrainage": 4,
        "prediction": 0.42,
        "actual_value": "",
        "error": "",
        "record_status": "pending_target",
    }

    save_prediction_record(db_path, row, ["MonsoonIntensity", "TopographyDrainage"])
    summary = get_database_summary(db_path)

    assert summary["exists"] is True
    assert summary["total_predictions"] == 1
    assert summary["pending_predictions"] == 1

    update_actual_value(db_path, "pred_test_1", actual_value=0.5, prediction=0.42)
    recent = load_recent_predictions(db_path)
    monitoring = load_monitoring_records(db_path)

    assert recent.loc[0, "actual_value"] == 0.5
    assert round(recent.loc[0, "error"], 2) == 0.08
    assert recent.loc[0, "record_status"] == "validated_for_retraining"
    assert monitoring.loc[0, "prediction_id"] == "pred_test_1"

    delete_prediction_record(db_path, "pred_test_1")
    summary_after_delete = get_database_summary(db_path)

    assert summary_after_delete["total_predictions"] == 0
    assert summary_after_delete["events"] == 3

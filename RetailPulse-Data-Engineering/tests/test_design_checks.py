"""Lightweight static checks for repository structure (run locally with pytest)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_notebooks_exist():
    required = [
        "00_setup_and_config.ipynb",
        "01_bronze_ingestion.ipynb",
        "02_silver_transformations.ipynb",
        "03_customer_scd_type2.ipynb",
        "04_gold_model.ipynb",
        "05_data_quality_and_audit.ipynb",
    ]
    for name in required:
        assert (ROOT / "notebooks" / name).exists()

def test_sql_files_exist():
    assert (ROOT / "sql" / "gold_business_queries.sql").exists()
    assert (ROOT / "sql" / "validation_queries.sql").exists()

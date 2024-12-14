import os
import tabula
from app.core.config import Config
from app.core.celery_app import celery


@celery.task(bind=True, queue="pdf_worker")
def process_pdf_task(self, pdf_path, task_id):
    """
    Celery task to process PDF and extract tables

    Args:
        pdf_path (str): Path to PDF file
        task_id (str): Unique task identifier
    """
    try:
        # Create task-specific folder
        task_folder = os.path.join(Config.UPLOAD_FOLDER, task_id)
        os.makedirs(task_folder, exist_ok=True)

        # Extract tables
        tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

        # Save tables as CSV
        for i, table in enumerate(tables):
            csv_path = os.path.join(task_folder, f"table_{i+1}.csv")
            table.to_csv(csv_path, index=False)

        return {"status": "completed", "task_id": task_id}

    except Exception as e:
        # Save error to file
        error_path = os.path.join(task_folder, "error.txt")
        with open(error_path, "w") as f:
            f.write(str(e))

        return {"status": "failed", "error": str(e)}

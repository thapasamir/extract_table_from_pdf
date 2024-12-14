import os
import uuid
import traceback
from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app.tasks import process_pdf_task

ns = Namespace("pdf", description="PDF Processing Operations")


upload_parser = reqparse.RequestParser()

upload_parser.add_argument(
    "file",
    type=FileStorage,
    location="files",
    required=True,
    help="PDF file to upload",
)


task_model = ns.model(
    "TaskResponse",
    {"task_id": fields.String(required=True, description="Unique Task Identifier")},
)


class PDFUploadResource(Resource):
    @ns.expect(upload_parser)
    @ns.marshal_with(task_model)
    def post(self):
        """Upload PDF and start processing"""
        try:
            args = upload_parser.parse_args()
            print("here", flush=True)

            # Check if file is provided
            uploaded_file = args.get("file")
            if not uploaded_file:
                ns.abort(400, "No file was uploaded. Please include a PDF file.")

            # Check file type
            if not uploaded_file.filename.lower().endswith(".pdf"):
                ns.abort(400, "Only PDF files are allowed.")

            # Generate unique task ID
            task_id = str(uuid.uuid4())
            upload_folder = current_app.config["UPLOAD_FOLDER"]

            # Ensure the upload folder exists
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save uploaded file
            file_path = os.path.join(upload_folder, f"{task_id}.pdf")
            uploaded_file.save(file_path)
            print("heretooo", flush=True)

            # Trigger async task
            process_pdf_task.delay(file_path, task_id)
            print("here not", flush=True)
            return {"task_id": task_id}, 201

        except Exception as e:
            # Capture and log the full stack trace
            error_trace = traceback.format_exc()
            current_app.logger.error(f"An error occurred: {e}\n{error_trace}")
            return {
                "message": "An internal server error occurred.",
                "details": str(e),
            }, 500


class PDFStatusResource(Resource):
    def get(self, task_id):
        """Check processing status of a PDF task"""
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        task_folder = os.path.join(upload_folder, task_id)

        # Check error file
        error_path = os.path.join(task_folder, "error.txt")
        if os.path.exists(error_path):
            with open(error_path, "r") as f:
                return {"status": "failed", "error": f.read()}, 400

        # Check CSV files
        try:
            csv_files = [f for f in os.listdir(task_folder) if f.endswith(".csv")]
        except FileNotFoundError as e:
            return (
                {
                    "status": "Not Found",
                    "error": "Task you requested doesn,t exists",
                },
            ), 400
        if csv_files:
            return {"status": "completed", "files": csv_files}, 200

        return {"status": "in-progress"}, 202


ns.add_resource(PDFUploadResource, "/upload")
ns.add_resource(PDFStatusResource, "/status/<string:task_id>")

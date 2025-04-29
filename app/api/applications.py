from flask import Blueprint, request, jsonify, current_app
from models.application import Application, PermitType, BuildingCategory, Document
from core.validators import validate_documents
from utils.file_handler import save_file
from db import db_session
from http import HTTPStatus

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/applications", methods=["POST"])
def submit_application():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST

        required_fields = ["applicant_id", "permit_type", "building_category", "location"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": "Missing required fields", "fields": missing_fields}), HTTPStatus.BAD_REQUEST

        applicant_id = data["applicant_id"]
        permit_type = data["permit_type"]
        building_category = data["building_category"]
        location = data["location"]
        uploaded_docs = data.get("documents", [])

        # Validate documents
        missing_docs = validate_documents(building_category, permit_type, uploaded_docs)
        if missing_docs:
            return jsonify({
                "error": "Missing required documents",
                "missing": missing_docs
            }), HTTPStatus.BAD_REQUEST

        # Create application
        try:
            app = Application(
                applicant_id=applicant_id,
                permit_type=PermitType(permit_type),
                building_category=BuildingCategory(building_category),
                location=location
            )
            db_session.add(app)
            db_session.flush()  # Get the ID without committing

            # Save documents
            for doc in uploaded_docs:
                document = Document(
                    application_id=app.id,
                    name=doc,
                    file_path=f"{current_app.config['UPLOAD_FOLDER']}/{doc}"
                )
                db_session.add(document)

            db_session.commit()
            return jsonify({
                "message": "Application submitted successfully",
                "application_id": app.id
            }), HTTPStatus.CREATED

        except ValueError as e:
            db_session.rollback()
            return jsonify({"error": f"Invalid enum value: {str(e)}"}), HTTPStatus.BAD_REQUEST
        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@applications_bp.route("/applications/<int:application_id>/documents", methods=["POST"])
def upload_document(application_id):
    try:
        # Validate application exists
        application = db_session.query(Application).get(application_id)
        if not application:
            return jsonify({"error": "Application not found"}), HTTPStatus.NOT_FOUND

        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), HTTPStatus.BAD_REQUEST

        file = request.files['file']
        doc_name = request.form.get("name")

        if not doc_name:
            return jsonify({"error": "Document name is required"}), HTTPStatus.BAD_REQUEST

        if file.filename == '':
            return jsonify({"error": "No selected file"}), HTTPStatus.BAD_REQUEST

        # Check for existing document
        existing_doc = db_session.query(Document).filter_by(
            application_id=application_id,
            name=doc_name
        ).first()
        if existing_doc:
            return jsonify({"error": "Document with this name already exists"}), HTTPStatus.CONFLICT

        file_path, error = save_file(file, current_app.config['UPLOAD_FOLDER'])
        if error:
            return jsonify({"error": error}), HTTPStatus.BAD_REQUEST

        try:
            doc = Document(
                application_id=application_id,
                name=doc_name,
                file_path=file_path
            )
            db_session.add(doc)
            db_session.commit()

            return jsonify({
                "message": "File uploaded successfully",
                "path": file_path
            }), HTTPStatus.CREATED

        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
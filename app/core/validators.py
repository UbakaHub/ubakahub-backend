REQUIRED_DOCS = {
    "category_2": {
        "new_building": ["application_form", "land_title"],
    },
    "category_3": {
        "new_building": [
            "application_form", "land_title", "architectural_drawings",
            "eia", "structural_design", "boq"
        ]
    },
    # Extend more combinations as needed
}

def validate_documents(category, permit_type, uploaded_docs):
    missing = []
    required = REQUIRED_DOCS.get(category, {}).get(permit_type, [])

    for doc_name in required:
        if doc_name not in uploaded_docs:
            missing.append(doc_name)

    return missing

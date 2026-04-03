from app.modules.gliner.schemas import ExtractionTemplate, ProcessingRules


USE_CASE_TEMPLATES: dict[str, ExtractionTemplate] = {
    "resume": ExtractionTemplate(
        key="resume",
        name="Resume Parsing",
        description="Extract common candidate details from resumes and CV text.",
        labels=[
            "name",
            "email",
            "phone",
            "location",
            "skills",
            "education",
            "experience",
            "organization",
            "designation",
        ],
        processing=ProcessingRules(
            value_normalizers={
                "email": "lower",
            }
        ),
    ),
    "invoice": ExtractionTemplate(
        key="invoice",
        name="Invoice and GST Extraction",
        description="Extract invoice fields including GST and total/tax details.",
        labels=[
            "invoice_number",
            "invoice_date",
            "due_date",
            "vendor_name",
            "buyer_name",
            "gst_number",
            "tax_amount",
            "total_amount",
            "currency",
        ],
    ),
    "seo": ExtractionTemplate(
        key="seo",
        name="SEO and Content Entities",
        description="Extract entities useful for SEO/content analysis from text.",
        labels=[
            "keyword",
            "topic",
            "brand",
            "product",
            "organization",
            "person",
            "location",
            "url",
        ],
        processing=ProcessingRules(
            value_normalizers={
                "url": "lower",
            }
        ),
    ),
    "ecommerce": ExtractionTemplate(
        key="ecommerce",
        name="Product and E-commerce Data",
        description="Extract product attributes from catalogs, listings, and descriptions.",
        labels=[
            "product_name",
            "brand",
            "category",
            "price",
            "currency",
            "sku",
            "color",
            "size",
            "material",
            "availability",
        ],
    ),
    "developer": ExtractionTemplate(
        key="developer",
        name="Developer Logs and API Data",
        description="Extract technical entities from logs, API docs, and diagnostic text.",
        labels=[
            "service_name",
            "api_endpoint",
            "http_method",
            "status_code",
            "error_code",
            "environment",
            "version",
            "timestamp",
        ],
        processing=ProcessingRules(
            value_normalizers={
                "api_endpoint": "lower",
                "http_method": "upper",
            }
        ),
    ),
}


def get_use_case_template(use_case: str) -> ExtractionTemplate | None:
    return USE_CASE_TEMPLATES.get(use_case.lower().strip())


def list_use_case_templates() -> list[ExtractionTemplate]:
    return list(USE_CASE_TEMPLATES.values())

from flask import request

from app.models.resource import Resource
from .. import bp


@bp.get("/api/get/all-pages/")
def api_get_all_pages():
    resource_id = request.args.get("id", None)
    if not resource_id:
        return {"status": "error", "message": "No valid resource_id", "pages": []}
    resource_ = Resource.get_by_id(resource_id)
    pages = resource_.rel_resource_pages
    clean_pages = []
    for page in pages:
        clean_pages.append({
            "resource_page_id": page.resource_page_id,
            "order": page.order,
            "markup": page.markup,
            "markdown": page.markdown,
            "markdown_og_filename": page.markdown_og_filename
        })
    return {"status": "success", "pages": clean_pages}

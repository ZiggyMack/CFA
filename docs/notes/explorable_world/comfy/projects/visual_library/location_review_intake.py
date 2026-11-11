"""Carry saved location-family direction through a local catalog rebuild."""
import importlib.util
from pathlib import Path


def apply_location_reviews(catalog, root, review, previous=None):
    previous = previous or {}
    if not any(key in source for source in (previous, review)
               for key in ("locationReviews", "locationReviewBackups")):
        return
    path = Path(root) / "apps/creative_studio/location_reviews.py"
    spec = importlib.util.spec_from_file_location("_cfa_location_review_intake", path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    catalog.update(helper.merge_state(previous, review))

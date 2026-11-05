"""Preserve validated questionnaire drafts and prepared replies on rebuild."""
import importlib.util
from pathlib import Path


def apply_collaborator_reviews(catalog, root, review, previous=None):
    sources = [previous or {}, review]
    if not any('collaboratorReviews' in source or 'collaboratorReviewBackups' in source for source in sources):
        return
    path = Path(root) / 'apps/creative_studio/collaborator_review.py'
    spec = importlib.util.spec_from_file_location('_cfa_collaborator_review_intake', path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    # Validate the complete union before replacing any previously saved records.
    prepared = {}
    if any('collaboratorReviews' in source for source in sources):
        prepared['collaboratorReviews'] = helper.merge(
            *(source.get('collaboratorReviews', {}) for source in sources))
    if any('collaboratorReviewBackups' in source for source in sources):
        prepared['collaboratorReviewBackups'] = helper.merge_backups(
            *(source.get('collaboratorReviewBackups', []) for source in sources))
    catalog.update(prepared)

"""Register the component from an importable module for Streamlit multipage apps."""
from pathlib import Path
from functools import lru_cache
import json
from urllib.parse import quote, unquote
from streamlit.components.v1 import declare_component


VIEWS = {'mission_control', 'casa_baldadoon', 'project_home', 'collaborators', 'all',
         'favorites', 'export_basket', 'review_queue', 'archive', 'shot_plans',
         'documents', 'intake', 'asset'}


@lru_cache(maxsize=8)
def route_config(snapshot: Path) -> dict:
    """Read project and view identities from the immutable published snapshot."""
    raw = (snapshot / 'catalog.js').read_text(encoding='utf-8')
    if not raw.lstrip().startswith('window.REVIEW_CATALOG=') and not raw.lstrip().startswith('window.REVIEW_CATALOG ='):
        raise ValueError('The dashboard route catalog is invalid.')
    catalog = json.loads(raw.split('=', 1)[1].strip().removesuffix(';'))
    return {'projects': [p['id'] for p in catalog.get('projects', [])],
            'views': sorted(VIEWS | {c[0] for c in catalog.get('categories', [])})}


def valid_route(value, config: dict) -> str | None:
    if not isinstance(value, str) or not value.startswith('#') or len(value) > 700:
        return None
    parts = [unquote(part) for part in value[1:].split('/')]
    if len(parts) not in (2, 3) or parts[0] not in config['projects'] or parts[1] not in config['views']:
        return None
    if any(not part or any(ord(char) < 32 or char in '/\\?#' for char in part) for part in parts):
        return None
    return '#' + '/'.join(quote(part, safe='') for part in parts)


def query_route(query, config: dict) -> str | None:
    project = query.get('project')
    if project not in config['projects']:
        return None
    view = query.get('view') or 'all'
    if not isinstance(view, str):
        return None
    # Native navigation uses display labels; the iframe uses canonical keys.
    # Baldadoon's earlier overview now lives inside All files.
    if view in {'Library', 'All files'} or (project == 'criminal_mind' and view == 'project_home'):
        view = 'all'
    parts = [project, view]
    if query.get('album'):
        parts.append(query['album'])
    if not all(isinstance(part, str) for part in parts):
        return None
    return valid_route('#' + '/'.join(quote(part, safe='') for part in parts), config)


def navigation_request(query, config: dict, previous: dict | None = None) -> dict:
    """Separate an outside navigation command from our own URL acknowledgements.

    A child route reported to the URL is already on screen. Reissuing it as a
    command on the next rerun can rewind a more recent click in the iframe.
    """
    current = query_route(query, config)
    if previous and current == previous.get('queryRoute'):
        return dict(previous)
    project = 'hon' if 'hon' in config['projects'] else config['projects'][0]
    return {'queryRoute': current, 'requestedRoute': current or f'#{project}/all',
            'requestID': (previous.get('requestID', 0) if previous else 0) + 1}


def route_query_update(value, initial_route: str | None, config: dict,
                       request_id: int | None = None) -> dict | None:
    """Ignore stale iframe results when a different direct link has just opened."""
    if not isinstance(value, dict) or value.get('requestedRoute') != initial_route:
        return None
    if request_id is not None and value.get('requestID') != request_id:
        return None
    route = valid_route(value.get('route'), config)
    if not route:
        return None
    parts = [unquote(part) for part in route[1:].split('/')]
    return {'project': parts[0], 'view': parts[1], 'album': parts[2] if len(parts) == 3 else None}


def render_dashboard(snapshot: Path, height: int = 850, initial_route: str | None = None,
                     request_id: int | None = None, report_navigation: bool = False):
    # Stable registration name and browser origin preserve localStorage reviews
    # when a new content-addressed snapshot replaces the previous deployment.
    component = declare_component("cfa_full_visual_library", path=str(snapshot))
    config = route_config(snapshot)
    return component(height=height, initialRoute=valid_route(initial_route, config),
                     requestID=request_id, reportNavigation=report_navigation, routeConfig=config,
                     key="cfa-full-visual-library", default=None)

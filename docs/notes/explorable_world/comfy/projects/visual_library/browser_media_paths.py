"""Short, byte-identical browser paths for sources beyond Windows MAX_PATH.

An NTFS hard link is a second name for the same file, not another media copy.
Original intake paths and hashes remain the provenance authority. Do not edit
the aliases: editing either name would edit the same underlying source bytes.
"""
import hashlib
import json
import os
from pathlib import Path

from grok500_catalog import io_path


class BrowserMediaPaths:
    def __init__(self, root, output):
        self.root = Path(root).resolve()
        self.output = Path(output).resolve()
        if not self.output.is_relative_to(self.root):
            raise ValueError('Browser aliases must stay inside the repository.')
        self.entries = {}

    def resolve(self, source):
        source = Path(source).absolute()
        if len(str(source)) < 260:
            return source
        if not source.is_relative_to(self.root):
            raise ValueError('Browser source must stay inside the repository.')
        relative = source.relative_to(self.root).as_posix()
        if relative in self.entries:
            return self.root / self.entries[relative]['browser_path']
        data = io_path(source).read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        alias = self.output / (sha + source.suffix.lower())
        if len(str(alias)) >= 260:
            raise ValueError('Browser alias itself exceeds MAX_PATH.')
        self.output.mkdir(parents=True, exist_ok=True)
        if not alias.exists():
            os.link(io_path(source), alias)
        if hashlib.sha256(alias.read_bytes()).hexdigest() != sha:
            raise ValueError('Browser alias differs from source: ' + relative)
        # A pre-existing exact-byte alias may have come from another duplicate
        # source. Keep that verified link; never create a second payload copy.
        self.entries[relative] = {
            'browser_path': alias.relative_to(self.root).as_posix(),
            'sha256': sha,
            'bytes': len(data),
            'source_path_characters': len(str(source)),
            'browser_path_characters': len(str(alias)),
            'same_file': os.path.samefile(io_path(source), alias),
        }
        return alias

    def write_manifest(self, destination):
        Path(destination).write_text(json.dumps({
            'schema_version': 1,
            'purpose': 'Full-resolution Windows browser aliases for long source paths.',
            'storage': 'hard_links_no_copied_media_payloads',
            'originals_changed': False,
            'warning': 'Read-only use. Aliases share source bytes; never edit them.',
            'by_source_path': self.entries,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

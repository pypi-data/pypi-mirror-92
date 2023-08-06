# ------------------------------------------------------------------------------
# This module creates and caches the parse-tree of Node instances.
# ------------------------------------------------------------------------------

from __future__ import annotations
from typing import Dict, List, Callable, Any, Union, Optional
from pathlib import Path

import os
import sys

from . import utils
from . import events
from . import filters
from . import renderers
from . import site


# Cached parse tree of Node instances.
_root = None


# Returns the site's root node. Parses the root directory and assembles the
# node tree on first call.
def root() -> Node:
    global _root
    if _root is None:
        if not os.path.isdir(site.src()):
            sys.exit("Error: cannot locate the site's source directory.")
        _root = Node()
        _parse_node_directory(_root, site.src())
    return _root


# Returns the node corresponding to the specified @root/ url if it exists,
# otherwise returns None.
def node(url: str) -> Optional[Node]:
    if url.startswith('@root/'):
        node = root()
        for slug in url.rstrip('/').split('/')[1:]:
            if (node := node.child(slug)) is None:
                break
        return node
    return None


# A Node instance represents a directory or text file (or both) in the
# site's source directory.
class Node():

    def __init__(self):
        # Stores the node's metadata (title, author, date, etc.).
        self.meta: Dict[str, Any] = {}

        # Stores a reference to the node's parent node.
        self.parent: Optional[Node] = None

        # Stores child nodes.
        self.children: List[Node] = []

        # Stores the path to the node's source directory/file.
        # (File path will overwrite directory path.)
        self.filepath: str = ''

        # Stores the node's filepath stem, i.e. basename minus extension.
        self.stem: str = ''

        # Stores the node's filepath extension, stripped of its leading dot.
        self.ext: str = ''

        # Stores the node's raw text content.
        self.text: str = ''

        # Internal cache for generated data.
        self.cache: Dict[str, Any] = {}

    # Identifying nodes by their @root/ url is useful for debugging.
    def __repr__(self) -> str:
        return f"<Node {self.url}>"

    # Allows dictionary-style read access to the node's metadata.
    def __getitem__(self, key: str) -> Any:
        return self.meta[key]

    # Allows dictionary-style write access to the node's metadata.
    def __setitem__(self, key: str, value: Any):
        self.meta[key] = value

    # Dictionary-style 'in' support for metadata.
    def __contains__(self, key: str) -> bool:
        return key in self.meta

    # Dictionary-style 'get' support for metadata.
    def get(self, key: str, default: Any = None) -> Any:
        return self.meta.get(key, default)

    # Dictionary-style 'get' with inheritance for metadata. This method walks
    # its way up the ancestor chain looking for a matching entry.
    def inherit(self, key: str, default: Any = None) -> Any:
        while self is not None:
            if key in self.meta:
                return self.meta[key]
            self = self.parent
        return default

    # Calls the specified function on the node and all its descendants.
    def walk(self, callback: Callable[['Node'], None]):
        for node in self.children:
            node.walk(callback)
        callback(self)

    # Returns the node's path, i.e. the list of slugs which determines the node's
    # output filepath and url. (Returns a disposable copy of the cached list.)
    @property
    def path(self) -> List[str]:
        if not 'path' in self.cache:
            self.cache['path'] = []
            current = self
            while current.parent is not None:
                self.cache['path'].append(current.slug)
                current = current.parent
            self.cache['path'].reverse()
        return self.cache['path'].copy()

    # Returns the node's url.
    @property
    def url(self) -> str:
        if not 'url' in self.cache:
            if self.parent:
                self.cache['url'] = '@root/' + '/'.join(self.path) + '//'
            else:
                self.cache['url'] = '@root/'
        return self.cache['url']

    # True if the node has child nodes.
    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    # Returns the node's filepath/url slug.
    @property
    def slug(self) -> str:
        if not 'slug' in self.cache:
            self.cache['slug'] = self.meta.get('slug') or utils.slugify(self.stem)
        return self.cache['slug']

    # Returns the child node with the specified slug if it exists, otherwise None.
    def child(self, slug: str) -> Optional[Node]:
        for child in self.children:
            if child.slug == slug:
                return child
        return None

    # Returns the node's rendered HTML content.
    @property
    def html(self) -> str:
        if not 'html' in self.cache:
            text = filters.apply('node_text', self.text, self)
            html = renderers.render(text, self.ext, self.filepath)
            self.cache['html'] = filters.apply('node_html', html, self)
        return self.cache['html']


# Parse a source directory.
#
# Args:
#   dirnode (Node): the Node instance for the directory.
#   dirpath (str/Path): path to the directory as a string or Path instance.
def _parse_node_directory(dirnode, dirpath):

    # Parse subdirectories.
    for path in (p for p in Path(dirpath).iterdir() if p.is_dir()):
        if filters.apply('load_node_dir', True, path):
            childnode = Node()
            childnode.stem = path.stem
            childnode.parent = dirnode
            childnode.filepath = str(path)
            dirnode.children.append(childnode)
            _parse_node_directory(childnode, path)

    # Parse files.
    for path in (p for p in Path(dirpath).iterdir() if p.is_file()):
        if path.stem.startswith('.') or path.stem.endswith('~'):
            continue
        if filters.apply('load_node_file', True, path):
            _parse_node_file(dirnode, path)


# Parse a source file.
#
# Args:
#   dirnode (Node): the Node instance for the directory containing the file.
#   filepath (Path): path to the file as a Path instance.
def _parse_node_file(dirnode, filepath):
    if filepath.stem == 'index':
        filenode = dirnode
    else:
        filenode = None
        for child in dirnode.children:
            if filepath.stem == child.stem:
                filenode = child
                break
        if filenode is None:
            filenode = Node()
            filenode.stem = filepath.stem
            filenode.parent = dirnode
            dirnode.children.append(filenode)
    text, meta = utils.loadfile(filepath)
    filenode.text = text
    filenode.meta.update(meta)
    filenode.filepath = str(filepath)
    filenode.ext = filepath.suffix.strip('.')

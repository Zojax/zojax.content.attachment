# This file is necessary to make this directory a package.
from BTrees import OOBTree

OOBTreeItems = type(OOBTree.OOBTree().keys())

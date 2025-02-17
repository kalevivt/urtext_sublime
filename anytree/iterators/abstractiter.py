
import sys
import os
parent_dir = os.path.dirname(__file__)
super_parent_dir = os.path.dirname(parent_dir)
vendor_dir = os.path.join(parent_dir, 'anytree')
sys.path.append(super_parent_dir)

import anytree_six as six 
    
class AbstractIter(six.Iterator):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Base class for all iterators.

        Iterate over tree starting at `node`.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.
        """
        self.node = node
        self.filter_ = filter_
        self.stop = stop
        self.maxlevel = maxlevel
        self.__iter = None

    def __init(self):
        node = self.node
        maxlevel = self.maxlevel
        filter_ = self.filter_ or AbstractIter.__default_filter
        stop = self.stop or AbstractIter.__default_stop
        children = [] if AbstractIter._abort_at_level(1, maxlevel) else AbstractIter._get_children([node], stop)
        return self._iter(children, filter_, stop, maxlevel)

    @staticmethod
    def __default_filter(node):
        return True

    @staticmethod
    def __default_stop(node):
        return False

    def __iter__(self):
        return self.__init()

    def __next__(self):
        if self.__iter is None:
            self.__iter = self.__init()
        return next(self.__iter)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def _abort_at_level(level, maxlevel):
        return maxlevel is not None and level > maxlevel

    @staticmethod
    def _get_children(children, stop):
        return [child for child in children if not stop(child)]

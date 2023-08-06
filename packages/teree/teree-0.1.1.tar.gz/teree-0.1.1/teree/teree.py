class Node:
    def __init__(self, name, some=None):
        self.name = str(name)
        self.nodes = self._build_nodes(some) if some else []

    @classmethod
    def _build_nodes(cls, some):
        if type(some) in [str, int]:
            return [cls(some)]
        if isinstance(some, list):
            return [cls(i, v) for i, v in enumerate(some)]
        if isinstance(some, dict):
            return [cls(i, v) for i, v in some.items()]
        return [cls(p, getattr(some, p)) for p in dir(some) if not p.startswith('_')]


class Teree():
    """Tree maker"""

    def __init__(self, some, ch=['―', '├', '|', '└']):
        """Init tree maker with any object"""
        self._tree = Node(type(some), some)
        self._ch = ch

    def tree(self) -> str:
        """Get tree as string"""
        return self._traverse(self._tree)

    def _traverse(self, root: Node, level=-1, last=False, sup=[]) -> str:
        """Produce tree by traversing nodes"""
        from functools import reduce
        d, b, p, e = self._ch
        nodes = root.nodes

        out = []
        padded_pipe = '{}  '.format(p)
        pre = ''.join(reduce(self._rmpipe, sup, [padded_pipe] * level))
        end_or_branch = e if last else b

        if level == -1:
            out.append(root.name)
        else:
            out.append('{}{}{} {}'.format(pre, end_or_branch, d, root.name))

        if nodes:
            level += 1
            traverse = self._traverse
            for node in nodes[:-1]:
                out.append(traverse(node, level, False, sup))
            out.append(traverse(nodes[-1], level, True, [level]+sup))

        return '\n'.join(out)

    @staticmethod
    def _rmpipe(prev, i):
        """Remove pipes if no previous level nodes"""
        if i < len(prev):
            prev[i] = '   '
        return prev

    def __repr__(self) -> str:
        return self._tree.__repr__()

    def __str__(self) -> str:
        return self.tree()

"""
Test result collection via abstract syntax tree transformation
"""

import ast

class CheckCallWrapper(ast.NodeTransformer):
    """
    Visits and replaces nodes in an abstract syntax tree in-place.
    
    Tracks import syntax and instances of ``taeg.Notebook`` in an AST. Wraps calls to 
    ``taeg.Notebook.check`` in calls to ``list.append`` to collect results of execution. Removes calls
    to ``taeg.Notebook.check_all``, `taeg.Notebook.export``, and ``taeg.Notebook.to_pdf``.
    
    Args:
        secret (``str``): random digits string that prevents check function from being modified
    
    Attributes:
        secret (``str``): random digits string that prevents check function from being modified
    """
    TAEG_IMPORT_SYNTAX = "import"
    TAEG_IMPORT_NAME = "taeg"
    TAEG_CLASS_NAME = "Notebook"
    TAEG_INSTANCE_NAME = "grader"

    def __init__(self, secret):
        self.secret = secret

    def check_node_constructor(self, expression):
        """
        Creates node that wraps expression in a list (``check_results_XX``) append call
        
        Args:
            expression (``ast.Name``): name for check function

        Returns:
            ``ast.Call``: function call object from calling check

        """
        args = [expression]
        func = ast.Attribute(
            attr='append',
            value=ast.Name(id='check_results_{}'.format(self.secret), ctx=ast.Load()),
            ctx=ast.Load(),
            keywords=[]
        )
        return ast.Call(func=func, args=args, keywords=[])

    def visit_ImportFrom(self, node):
        """
        Visits ``from ... import ...`` nodes and tracks the import syntax and alias of ``taeg.Notebook``

        Args:
            node (``ast.ImportFrom``): the import node

        Returns:
            ``ast.ImportFrom``: the original node
        """
        if node.module == "taeg" and "Notebook" in [n.name for n in node.names]:
            type(self).TAEG_IMPORT_SYNTAX = "from"
            nb_asname = [n.asname for n in node.names if n.name == "Notebook"][0]
            if nb_asname is not None:
                type(self).TAEG_CLASS_NAME = nb_asname
        return node

    def visit_Import(self, node):
        """
        Visits ``import ...`` nodes and tracks the import syntax and alias of ``taeg``

        Args:
            node (``ast.Import``): the import node

        Returns:
            ``ast.Import``: the original node
        """
        if "taeg" in [n.name for n in node.names]:
            type(self).TAEG_IMPORT_SYNTAX = "import"
            taeg_asname = [n.asname for n in node.names if n.name == "taeg"][0]
            if taeg_asname is not None:
                type(self).TAEG_IMPORT_NAME = taeg_asname
        return node

    def visit_Assign(self, node):
        """
        Visits assignment nodes to determine the name assigned to the instance of ``taeg.Notebook``
        created.

        Args:
            node (``ast.Assign``): the assignment node

        Returns:
            ``ast.Assign``: the original node
        """
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute) and type(self).TAEG_IMPORT_SYNTAX == "import":
                if node.value.func.attr == "Notebook" and isinstance(node.value.func.value, ast.Name):
                    if node.value.func.value.id == type(self).TAEG_IMPORT_NAME:
                        assert len(node.targets) == 1, "error parsing taeg.Notebook instance in ast"
                        type(self).TAEG_INSTANCE_NAME = node.targets[0].id
            elif isinstance(node.value.func, ast.Name) and type(self).TAEG_IMPORT_SYNTAX == "from":
                if node.value.func.id == type(self).TAEG_CLASS_NAME:
                    assert len(node.targets) == 1, "error parsing taeg.Notebook instance in ast"
                    type(self).TAEG_INSTANCE_NAME = node.targets[0].id
        return node

    def visit_Expr(self, node):
        """
        Visits expression nodes and removes them if they are calls to ``taeg.Notebook.check_all``,
        ``taeg.Notebook.export``, or ``taeg.Notebook.to_pdf`` or wraps them using 
        ``CheckCallWrapper.check_node_constructor`` if they are calls to ``taeg.Notebook.check``.

        Args:
            node (``ast.Expr``): the expression node

        Returns:
            ``ast.Expr``: the transformed node
            ``None``: if the node was a removed call
        """
        if isinstance(node.value, ast.Call):
            call_node = node.value
            if isinstance(call_node.func, ast.Attribute):
                if isinstance(call_node.func.value, ast.Name) and call_node.func.value.id == type(self).TAEG_INSTANCE_NAME:
                    if call_node.func.attr in ["check_all", "export", "to_pdf"]:
                        return None
                    elif call_node.func.attr == "check":
                        node.value = self.check_node_constructor(call_node)
        return node

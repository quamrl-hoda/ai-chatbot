"""
app/tools/calculator.py – Safe math evaluation tool.
"""
import ast
import operator as op
from langchain_core.tools import tool

_SAFE_OPS = {
    ast.Add: op.add, ast.Sub: op.sub,
    ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Pow: op.pow, ast.USub: op.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _SAFE_OPS[type(node.op)](_eval(node.operand))
    raise ValueError(f"Unsupported expression: {type(node)}")


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a safe math expression and return the numeric result.

    Args:
        expression: A mathematical expression string, e.g. '2 ** 10 + 3 * 4'.
    """
    try:
        result = _eval(ast.parse(expression, mode="eval").body)
        return str(result)
    except Exception as exc:
        return f"Error: {exc}"

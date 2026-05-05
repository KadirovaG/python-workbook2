import ast
import logging
import math
import os
import re
from collections import defaultdict, deque

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

# 1. Setup logging to see errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

history_by_chat = defaultdict(lambda: deque(maxlen=10))
scientific_mode_by_chat = defaultdict(lambda: False)

ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "pow": pow,
}

BASIC_OPERATORS = {
    ast.Add: (lambda a, b: a + b),
    ast.Sub: (lambda a, b: a - b),
    ast.Mult: (lambda a, b: a * b),
    ast.Div: (lambda a, b: a / b),
    ast.Pow: (lambda a, b: a ** b),
}

UNARY_OPERATORS = {
    ast.UAdd: (lambda a: a),
    ast.USub: (lambda a: -a),
}


class SafeEvaluator(ast.NodeVisitor):
    def __init__(self, scientific: bool) -> None:
        self.scientific = scientific

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        return super().visit(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in BASIC_OPERATORS:
            return BASIC_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported operator")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPERATORS:
            return UNARY_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    def visit_Num(self, node):
        return node.n

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed")

    def visit_Call(self, node):
        if not self.scientific:
            raise ValueError("Scientific functions are disabled")
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")
        func_name = node.func.id
        func = ALLOWED_FUNCTIONS.get(func_name)
        if func is None:
            raise ValueError("Unsupported function")
        args = [self.visit(arg) for arg in node.args]
        return func(*args)

    def visit_Name(self, node):
        raise ValueError("Variables are not allowed")

    def generic_visit(self, node):
        raise ValueError("Invalid expression")


def normalize_expression(expr: str, scientific: bool) -> str:
    expr = expr.replace("x", "*").replace("×", "*").replace(":", "/")
    expr = expr.replace("^", "**")
    expr = expr.replace("√", "sqrt")

    # Convert percentage syntax like 5% to (5/100)
    expr = re.sub(r"(?P<num>\d+(?:\.\d+)?)%", r"(\g<num>/100)", expr)

    if not scientific and "sqrt" in expr:
        raise ValueError("Scientific mode is required for sqrt")

    return expr


def evaluate_expression(expression: str, scientific: bool) -> float:
    normalized = normalize_expression(expression, scientific)
    tree = ast.parse(normalized, mode="eval")
    evaluator = SafeEvaluator(scientific=scientific)
    return evaluator.visit(tree)


async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()
    scientific = scientific_mode_by_chat[chat_id]

    try:
        result = evaluate_expression(user_text, scientific)
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        history_by_chat[chat_id].append(f"{user_text} = {result}")
        await update.message.reply_text(f"Result: {result}")
    except Exception:
        await update.message.reply_text(
            "Sorry, I couldn't understand that. Try something like '2 + 3 * 4', 'sqrt(9)', '5^2', '25%' or use /scientific to toggle advanced mode."
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Send me a math expression and I'll solve it. Use /history for the last 10 calculations and /scientific to toggle advanced mode."
    )


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    history_items = list(history_by_chat[chat_id])
    if not history_items:
        await update.message.reply_text("No history yet. Send a calculation first.")
        return

    await update.message.reply_text("\n".join(history_items))


async def scientific(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    scientific_mode_by_chat[chat_id] = not scientific_mode_by_chat[chat_id]
    mode = "Scientific" if scientific_mode_by_chat[chat_id] else "Basic"
    await update.message.reply_text(
        f"{mode} mode is now enabled. Scientific features: sqrt, ^, and percentage support."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Calculator commands:\n"
        "/history - show last 10 calculations\n"
        "/scientific - toggle scientific mode\n"
        "Supported expressions: +, -, *, /, ^, parentheses, sqrt(), %, and x for multiplication."
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("scientific", scientific))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))

    print("Calculator bot is running...")
    app.run_polling()

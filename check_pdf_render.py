"""Run using Python with pypdf installed. Generates a local QA PDF."""
import ast
import glob
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata
from datetime import datetime
from pypdf import PdfReader


def load_renderer(platform):
    path = Path(__file__).parent / platform / "system/code/generate_pdfs.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) or
             (isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant))]
    ns = dict(globals())
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), ns)
    ns["get_pandoc_path"] = lambda: None
    # QA uses local fonts and plain text, without downloading scripts.
    ns["CSS_STYLE"] = re.sub(r"@import[^;]+;", "", ns["CSS_STYLE"])
    ns["MATHJAX_SCRIPT"] = ns["MERMAID_SCRIPT"] = ""
    return ns


if __name__ == "__main__":
    out = Path(__file__).parent / "tmp/pdfs"
    out.mkdir(parents=True, exist_ok=True)
    source = out / "Week2.md"
    source.write_text("# 2주차 강의노트\n\n수업 일자: 2027-03-08\n\nWeek 2 - Class Date: 2027-03-08\n\n선택한 강의자료 기반 검증 문서입니다.\n", encoding="utf-8")
    pdf = out / "Week2.pdf"
    ns = load_renderer("URY_macOS")
    result = ns["convert_single_md_to_pdf"](str(source), str(pdf), "Week 2", str(out))
    text = "\n".join(page.extract_text() for page in PdfReader(result).pages)
    assert "2027-03-08" in text and "Week 2" in text, text
    print("PDF date/week verified:", result)

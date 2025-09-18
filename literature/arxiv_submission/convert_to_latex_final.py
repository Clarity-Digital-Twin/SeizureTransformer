#!/usr/bin/env python3
"""Convert markdown paper to properly formatted LaTeX"""

import re
from pathlib import Path

# Read the markdown
with open("PAPER_CLEAN_FIGS.md", "r") as f:
    content = f.read()

# Clean special characters
content = content.replace("×", "$\\times$")
content = content.replace("±", "$\\pm$")
content = content.replace("−", "$-$")
content = content.replace(">=", "$\\geq$")
content = content.replace("<=", "$\\leq$")
content = content.replace("~=", "$\\approx$")
content = content.replace("θ", "$\\theta$")

# Extract sections
title_match = re.search(r"# (.*?)\n", content)
title = title_match.group(1) if title_match else "Untitled"

# Extract author info
author_match = re.search(r"\*\*Author\*\*: (.*?)\n", content)
author_text = author_match.group(1) if author_match else ""

# Extract abstract
abstract_match = re.search(r"\*\*Abstract\*\*: (.*?)\n\n", content, re.DOTALL)
abstract = abstract_match.group(1).strip() if abstract_match else ""

# Convert markdown sections to LaTeX
latex_content = content

# Convert headers
latex_content = re.sub(r"^### (.*?)$", r"\\subsection{\1}", latex_content, flags=re.MULTILINE)
latex_content = re.sub(r"^## (.*?)$", r"\\section{\1}", latex_content, flags=re.MULTILINE)
latex_content = re.sub(r"^# (.*?)$", r"\\section{\1}", latex_content, flags=re.MULTILINE)

# Convert bold/italic
latex_content = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", latex_content)
latex_content = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", latex_content)

# Convert code blocks
latex_content = re.sub(r"```(.*?)```", r"\\begin{verbatim}\1\\end{verbatim}", latex_content, flags=re.DOTALL)
latex_content = re.sub(r"`([^`]+)`", r"\\texttt{\1}", latex_content)

# Convert lists
latex_content = re.sub(r"^- (.*?)$", r"\\item \1", latex_content, flags=re.MULTILINE)
latex_content = re.sub(r"(\\item .*\n)+", r"\\begin{itemize}\n\g<0>\\end{itemize}\n", latex_content)

# Convert numbered lists
latex_content = re.sub(r"^\d+\. (.*?)$", r"\\item \1", latex_content, flags=re.MULTILINE)

# Convert figures - extract caption and path
def convert_figure(match):
    caption = match.group(1)
    path = match.group(2)
    return f"""\\begin{{figure}}[ht]
\\centering
\\includegraphics[width=\\textwidth]{{{path}}}
\\caption{{{caption}}}
\\end{{figure}}"""

latex_content = re.sub(r"!\[(.*?)\]\((.*?)\)(?:\{.*?\})?", convert_figure, latex_content)

# Convert tables
def convert_table(match):
    table_text = match.group(0)
    lines = table_text.strip().split('\n')

    # Parse header
    header = lines[0].split('|')[1:-1]
    num_cols = len(header)

    # Create LaTeX table
    latex_table = "\\begin{table}[ht]\n\\centering\n"
    latex_table += "\\begin{tabular}{" + "l" * num_cols + "}\n\\toprule\n"

    # Add header
    latex_table += " & ".join([h.strip() for h in header]) + " \\\\\n\\midrule\n"

    # Add rows (skip separator line)
    for line in lines[2:]:
        if line.strip():
            row = line.split('|')[1:-1]
            latex_table += " & ".join([r.strip() for r in row]) + " \\\\\n"

    latex_table += "\\bottomrule\n\\end{tabular}\n"
    latex_table += "\\caption{Performance comparison}\n"
    latex_table += "\\end{table}"

    return latex_table

# Match markdown tables
latex_content = re.sub(r"\|.*\|\n\|[\-:\s|]+\|\n(?:\|.*\|\n)+", convert_table, latex_content)

# Create full LaTeX document
latex_doc = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{xcolor}
\usepackage{times}  % Better font

% Spacing adjustments
\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}
\setlength{\intextsep}{10pt plus 2pt minus 2pt}
\setlength{\floatsep}{10pt plus 2pt minus 2pt}
\setlength{\textfloatsep}{10pt plus 2pt minus 2pt}

% Caption formatting
\captionsetup{font=small,labelfont=bf,labelsep=period,skip=4pt}

% Abstract formatting
\renewenvironment{abstract}
{\small
\begin{center}
\bfseries Abstract
\end{center}
\quotation}
{\endquotation}

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    urlcolor=blue,
    citecolor=blue
}

\title{\Large\bfseries """ + title + r"""}

\author{
John H. Jung, MD, MS\\
Independent Researcher\\
\texttt{jj@novamindnyc.com}
}

\date{}  % No date

\begin{document}

\maketitle
\vspace{-20pt}  % Reduce space after title

\begin{abstract}
""" + abstract + r"""
\end{abstract}

""" + latex_content + r"""

\end{document}"""

# Write LaTeX file
with open("seizure_transformer_final.tex", "w") as f:
    f.write(latex_doc)

print("LaTeX file created: seizure_transformer_final.tex")
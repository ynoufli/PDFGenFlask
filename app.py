from flask import Flask, render_template, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

TEMPLATE = r"""
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\geometry{margin=2cm}

\title{\textbf{{{{ title }}}}}

\begin{document}
\maketitle

\section*{Introduction}
{{{{ intro }}}}

\end{document}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]

        uid = str(uuid.uuid4())
        tex_file = f"{uid}.tex"
        pdf_file = f"{uid}.pdf"

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.replace("{{ title }}", title)
                            .replace("{{ intro }}", intro))

        subprocess.run(["pdflatex", tex_file],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        return send_file(pdf_file, as_attachment=True)

    return """
    <h2>Génération PDF LaTeX</h2>
    <form method="post">
        <input name="title" placeholder="Titre"><br><br>
        <textarea name="intro" placeholder="Introduction"></textarea><br><br>
        <button type="submit">Générer PDF</button>
    </form>
    """

if __name__ == "__main__":
    app.run()

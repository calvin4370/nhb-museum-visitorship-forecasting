"""
Builds outputs/{museum}/{museum}_summary.txt: 
A report combining each model's eval metrics with its own predicted FY totals, and the
historical + predicted total visitors by financial year.
"""

import subprocess
from datetime import datetime

import pandas as pd


def git_branch():
    """
    Returns the current git branch, the short commit SHA if HEAD is detached,
    or None when git is unavailable or this is not a repo.
    """
    try:
        run = lambda args: subprocess.run(
            args, capture_output=True, text=True, check=True
        ).stdout.strip()
        name = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return run(["git", "rev-parse", "--short", "HEAD"]) if name == "HEAD" else name
    except (OSError, subprocess.CalledProcessError):
        return None


def timestamp_now():
    """
    Returns the current local time as e.g. "8 Sep 2026 7.56pm". 
    Built manually rather than with strftime, as its no-leading-zero codes differ per platform.
    """
    now = datetime.now()
    hour = now.hour % 12 or 12
    meridiem = "am" if now.hour < 12 else "pm"
    return f"{now.day} {now:%b} {now.year} {hour}.{now:%M}{meridiem}"


def FY_label(timestamp):
    """
    Returns the Financial Year label from the timestamp.
    Financial years run from April to March, e.g. FY2026 is Apr 2026 - Mar 2027.
    """
    year = timestamp.year if timestamp.month >= 4 else timestamp.year - 1
    return f"FY{year}"


def FY_totals(df, value_col="value"):
    """
    Sums `value_col` per financial year. 
    Returns a Series indexed by FY label.
    """
    labels = df["timestamp"].apply(FY_label)
    return df.groupby(labels)[value_col].sum().sort_index()


# ============================================================ #
# Summary TXT
# ============================================================ #


def format_table(df, sep="  "):
    """
    Render a DataFrame as plain text with every column left-aligned and
    columns separated by `sep`. pandas' own to_string() right-aligns numeric
    columns and only pads by a single space, which reads as cramped/uneven --
    this gives full manual control instead.
    """
    str_df = df.astype(str)
    widths = {col: max(str_df[col].str.len().max(), len(col)) for col in df.columns}
    header = sep.join(col.ljust(widths[col]) for col in df.columns)
    rows = [
        sep.join(row[col].ljust(widths[col]) for col in df.columns)
        for _, row in str_df.iterrows()
    ]
    return "\n".join([header] + rows)


def write_summary_txt(save_path, museum_code, eval_table, fy_table, per_model_fy_table):
    """
    Writes the report file containing model evaluation results and predictions
    to a txt file at `save_path`. 
    """
    # eval_table is sorted lowest-RMSE-first, so its first row is the winning model,
    # and the FY totals are built from that model's forecast
    winning_model = eval_table.iloc[0]["Model"]

    # Document title
    report_title = f"[--------------- Summary Report ({museum_code}) ---------------]"

    # Build the report as a list of lines, with the run's provenance under the title
    lines = [report_title]

    # Add provenance info: git branch and timestamp
    branch = git_branch()
    if branch:
        lines.append(f"Branch:    {branch}")
    lines.append(f"Generated: {timestamp_now()}")
    lines.append("")

    # Append Table 1: Every model's eval metrics alongside its own forecast FY totals
    lines.append("======== Model Evaluation Results + Predictions ========")
    lines.append(format_table(per_model_fy_table))
    lines.append("\n")

    # Append Table 2: Historical then predicted FY totals, from the winning model's forecast
    lines.append("======== Total Visitors ('000s) by Financial Year ========")
    lines.append(f"({winning_model})")
    lines.append(format_table(fy_table))
    lines.append("\n")

    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ============================================================ #
# Summary MD
# ============================================================ #

# Fixed pixel widths for the FY tables' two columns, so the tables that sit
# beside each other line up. Their content is the same shape for every museum.
FY_TABLE_WIDTHS = [140, 150]

def format_html_table(df, align=None, widths=None):
    """
    Render a DataFrame as an HTML table. Markdown renderers pass HTML through,
    and it stays more compact than a pipe table. `align` sets the legacy float
    attribute and `widths` the per-column pixel widths -- both survive GitHub's
    sanitiser, where inline CSS does not.
    """
    attr = f' align="{align}"' if align else ""
    head = "".join(
        f'<th width="{widths[i]}">{col}</th>' if widths else f"<th>{col}</th>"
        for i, col in enumerate(df.columns)
    )
    body = "".join(
        "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
        for row in df.astype(str).values
    )
    return f"<table{attr}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def split_rows(df, parts=2):
    """
    Splits a table's rows into `parts` frames, filled top to bottom, so they can
    be rendered as separate tables sitting next to each other.
    """
    per_part = -(-len(df) // parts)  # ceiling division
    return [df.iloc[i:i + per_part] for i in range(0, len(df), per_part)]


def format_html_tables_side_by_side(frames, widths=None):
    """
    Renders each frame as its own table, all sharing one set of column widths,
    with the first floated left and the last right so they sit apart. Clears the
    float afterwards so whatever follows starts below them.
    """
    aligns = ["left"] * (len(frames) - 1) + ["right"]
    tables = "".join(
        format_html_table(frame, align=align, widths=widths)
        for frame, align in zip(frames, aligns)
    )
    return tables + '<br clear="all">'


def write_summary_md(save_path, museum_code, eval_table, fy_table, per_model_fy_table):
    """
    Writes the same report as write_summary_txt, in markdown, to `save_path`.
    """
    # eval_table is sorted lowest-RMSE-first, so its first row is the winning model,
    # and the FY totals are built from that model's forecast
    winning_model = eval_table.iloc[0]["Model"]

    # Document title
    lines = [f"## Summary Report ({museum_code})", ""]

    # Append Provenance in a code block
    branch = git_branch()
    lines.append("```")
    if branch:
        lines.append(f"Branch:    {branch}")
    lines.append(f"Generated: {timestamp_now()}")
    lines.append("```")
    lines.append("")

    # Append Table 1: Every model's eval metrics alongside its own forecast FY totals
    lines.append("### Model Evaluation Results + Predictions")
    lines.append("")
    lines.append(format_html_table(per_model_fy_table))
    lines.append("")

    # Append Table 2: Historical then predicted FY totals, from the winning model's forecast,
    # split across two side-by-side tables to keep the whole report screenshotable
    lines.append(f"### Total Visitors ('000s) by Financial Year ({winning_model})")
    lines.append("")
    lines.append(format_html_tables_side_by_side(split_rows(fy_table), FY_TABLE_WIDTHS))
    lines.append("")

    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

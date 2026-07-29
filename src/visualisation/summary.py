"""
Builds outputs/{museum}/{museum}_summary.txt: 
A report combining the model eval rankings, historical + predicted total visitors by financial
year, and each model's own predicted FY totals.
"""

import pandas as pd


def FY_label(timestamp):
    """
    Returns the Financial Year label from the timestamp.
    Financial years run from April to March, e.g. FY2026 is Apr 2026 - Mar 2026.
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


def write_summary_txt(save_path, eval_table, fy_table, per_model_fy_table):
    """
    Writes the 3 tables to the report file
    """
    sections = [
        ("Model Evaluation", eval_table),
        ("Total Visitors by Financial Year", fy_table),
        ("Forecast FY Totals by Model", per_model_fy_table),
    ]
    lines = []
    for title, table in sections:
        lines.append(f"======== {title} ========")
        lines.append(format_table(table))
        lines.append("")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines))

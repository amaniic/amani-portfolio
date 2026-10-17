"""Calculate metrics from fixed, reported research confusion matrices.

This is new portfolio demonstration code, not the institutional training
implementation. Rows are actual classes and columns are predicted classes.
"""

from math import isfinite


def summarize(labels, matrix):
    """Return accuracy, per-class metrics, and macro F1 for a count matrix."""
    size = len(labels)
    if not size or len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("The count matrix must be square and match the labels.")
    if any(not isfinite(x) or x < 0 or int(x) != x for row in matrix for x in row):
        raise ValueError("Counts must be finite, nonnegative integers.")
    total = sum(map(sum, matrix))
    if not total:
        raise ValueError("The count matrix must contain at least one observation.")
    rows = []
    for index, label in enumerate(labels):
        correct = matrix[index][index]
        support = sum(matrix[index])
        predicted = sum(row[index] for row in matrix)
        precision = correct / predicted if predicted else 0.0
        recall = correct / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows.append((label, precision, recall, f1, support))
    accuracy = sum(matrix[i][i] for i in range(size)) / total
    macro_f1 = sum(row[3] for row in rows) / size
    return accuracy, macro_f1, rows


def print_report(title, labels, matrix):
    accuracy, macro_f1, rows = summarize(labels, matrix)
    print(title)
    print(f"Accuracy: {accuracy:.2%}; macro F1: {macro_f1:.4f}")
    print(f"{'Class':24} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Support':>9}")
    for label, precision, recall, f1, support in rows:
        print(f"{label:24} {precision:10.4f} {recall:10.4f} {f1:10.4f} {support:9d}")
    print()


if __name__ == "__main__":
    print_report(
        "Hazard classification — reported validation matrix",
        ["Fire", "Flood", "Infrastructure Damage", "Road Emergency"],
        [[95, 0, 1, 1], [0, 98, 1, 2], [1, 2, 82, 12], [0, 2, 1, 90]],
    )
    print_report(
        "Damage severity — final Stage 2 validation pass",
        ["Mild Damage", "Severe Damage"],
        [[125, 45], [82, 306]],
    )
    print("Severity best validation accuracy was 79.57% at a different checkpoint.")

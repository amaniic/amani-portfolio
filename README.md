# Amani Ibrahim Carbonell

Computer Engineering student at the University of South Florida, with a minor in Biomedical Physics. Expected graduation: May 2028.

My interests include applied machine learning, computer vision, and software engineering.

## What is in this repository

- `site/`: the source of my portfolio website, built with HTML, CSS, and JavaScript.
- `evaluate_reported_results.py`: a small, newly written Python script that calculates metrics from the confusion matrices reported in my research case study. It requires only the Python standard library.

## Selected research

### Emergency image classification

At the Polytechnic University of Puerto Rico, I developed two EfficientNet-B0 classifiers as part of undergraduate research into a proposed emergency-reporting system for Puerto Rico.

My contributions included dataset preparation and curation, Python/PyTorch implementation, transfer learning, staged fine-tuning, model evaluation, research writing, and relational schema design.

| Task | Reported best validation accuracy | Evaluation context |
| --- | ---: | --- |
| Four-class hazard classification | 94.07% | 388 validation images; macro F1 reported as 0.94 |
| Binary damage severity | 79.57% | Best result across training stages; the final Stage 2 confusion matrix corresponds to approximately 77.24% accuracy |

The hazard dataset contained 1,949 images curated from six public sources. Its four categories were Fire, Flood, Infrastructure Damage, and Road Emergency.

These are validation results used during model development, not independent external test results. Some road-emergency examples came from a source containing synthetic images. Severity labels remained subjective. The two tasks used different datasets and should not be treated as a direct benchmark.

### Scope and attribution

This repository is a portfolio website and research case study. It does not contain the original institution-owned training code, datasets, model weights, or report PDF. The metrics script is new code that operates only on numerical counts documented in the case study; it does not train or run an image classifier.

The numerical results are drawn from my 2026 research report, *Design and Development of an Intelligent Emergency State Reporting System for Puerto Rico*, conducted at the Polytechnic University of Puerto Rico.

## Run the metrics example

```bash
python3 evaluate_reported_results.py
```

The script prints accuracy, per-class precision/recall/F1, and macro F1. Small differences from the report's displayed values reflect rounding. It reproduces metrics from fixed reported counts; it does not reproduce training or independently validate the research.

## View the website locally

```bash
python3 -m http.server 8000 --directory site
```

Open `http://localhost:8000` in a browser. The website's result tabs support keyboard navigation. This public source copy omits the résumé and private contact details.

## Connect

[LinkedIn](https://www.linkedin.com/in/amani-ibr)

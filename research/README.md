# Emergency image classification — research source

Source supplied by **Amani Ibrahim Carbonell**, cleaned and organized with AI assistance. This package contains real submitted research code and explicitly documented adaptations; it does not contain invented severity training code.

## Included

- `reference/submitted_train_emergency.py`: formatting-repaired submitted emergency training code.
- `scripts/train_emergency.py`: runnable adaptation using EfficientNet-B0 transfer learning for four emergency classes.
- `scripts/evaluate_models.py`: evaluation of an emergency (four classes) or severity (two classes) state-dict checkpoint, with accuracy, confusion matrix, precision, recall, and F1.
- `scripts/prepare_severity_by_event.py`: CrisisMMD TSV-to-folder organization for event-based inspection, excluding `little_or_no_damage`.
- `tests/test_preparation.py`: small synthetic-file tests for preparation logic; no dataset images are included.

The supplied defaults are 12 epochs, batch size 16, Adam learning rate 0.0001, and a frozen EfficientNet-B0 feature extractor. See `CHANGELOG.md` for behavior changes in the adapted scripts.

## Setup

Use Python 3.10 or newer in a virtual environment. Install mutually compatible PyTorch and torchvision builds appropriate for your operating system/CPU/CUDA using the official PyTorch installation instructions, then install `scikit-learn` and `tqdm`. `requirements.txt` lists dependencies but is not an environment lockfile; no full model run has been verified in the preparation environment.

## Emergency training

Prepare `data/CustomDataset/train/<class>/` and `data/CustomDataset/val/<class>/`. The four class folders in the supplied code are `Fire`, `Flood`, `InfrastructureDamage`, and `RoadEmergency`; train and validation class mappings must match.

```sh
python scripts/train_emergency.py --dataset data/CustomDataset --output models/best_emergency_model.pt
```

The initial ImageNet weights download requires internet access. Training saves the best state dictionary and `models/best_emergency_model.classes.json`. A fresh run is not expected to reproduce a reported number exactly: dataset version, split, seed, preprocessing, and training behavior matter. This script does not impose a deterministic seed.

## Evaluate either model

```sh
python scripts/evaluate_models.py --model models/best_emergency_model.pt --dataset data/CustomDataset/val --classes models/best_emergency_model.classes.json
python scripts/evaluate_models.py --model models/severity_classifier_v1_79.6pct.pt --dataset data/SeverityDataset/val --classes models/severity.classes.json
```

For a legacy checkpoint, create the JSON list from its **verified training output order**. Do not guess the severity output order from class names or a filename. A checkpoint filename containing a percentage is not evidence that evaluation was rerun. Only use trusted state-dictionary checkpoints.

## Organize CrisisMMD by event

```sh
python scripts/prepare_severity_by_event.py --crisis-root data/CrisisMMD_v2.0 --output outputs/SeverityByEvent
python -m unittest discover -s tests -v
```

The script expects the submitted TSV column names `image` and `label`. Check the actual dataset version before use. Output is `train|val/<event>/<severity>/<date>/<image>`; this event-first layout must **not** be passed directly to `ImageFolder` as a two-class severity dataset, because the top-level folders would label events. Use it to inspect events or write a deliberate severity loader. It does not create an event-held-out evaluation split or prove absence of data leakage.

## Scope and sharing

Datasets, saved weights, original images, credentials, and local private paths are excluded from the adapted scripts. The formatting-repaired reference retains a generic historical Windows path. Reported project metrics have not been reproduced here. This research is not a validated emergency-response system.

No license or independent ownership of university research is asserted by this package.

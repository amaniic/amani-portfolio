# Changes from submitted code

The `reference/submitted_train_emergency.py` file retains the supplied training algorithm and comments, after removing Markdown escape characters, HTML entities, nonbreaking spaces, and excess blank lines. The malformed local Windows path was restored to `C:\AI_Projects\CustomDataset`. It remains a reference script that starts training when executed/imported.

The runnable scripts are adaptations, not unchanged historical files:

- Replace machine-specific paths with command-line arguments; add main guards.
- Preserve the supplied four-class EfficientNet-B0 classifier, data augmentation, Adam optimizer, 12-epoch default, batch size 16, and 0.0001 learning rate.
- Freeze backbone BatchNorm running statistics during training. The submitted script froze gradients but still called `model.train()` on the whole model, allowing those statistics to change.
- Average training loss by sample count and report the best saved checkpoint, rather than mixing final-epoch predictions with best-checkpoint accuracy.
- Save a class-order JSON beside each newly trained checkpoint. Evaluation requires that metadata (or a verified JSON list for a legacy checkpoint) instead of assuming folder order matches the checkpoint.
- Use explicit metric labels, zero-division handling, and `weights_only=True` checkpoint loading.
- Deduplicate the event-preparation script, replace pandas iteration with standard-library CSV, validate TSV paths/labels, count missing files, and prevent silent overwrites. Preserve date subfolders within each event/severity folder.

These changes may change results. No new training run or accuracy reproduction is claimed. Severity-model training code was not provided and has not been invented.

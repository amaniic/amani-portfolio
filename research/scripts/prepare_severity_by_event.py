"""Organize CrisisMMD damage images by split, event, and severity.
Adapted from Amani's submitted preparation script, duplicated once in the paste.
This layout is for per-event inspection, not a severity ImageFolder training root.
"""
import argparse
import csv
import shutil
from collections import Counter
from pathlib import Path, PurePosixPath

def process_split(tsv_path, split_name, crisis_root, output_root):
    crisis_root, output_root = Path(crisis_root).resolve(), Path(output_root).resolve()
    counts = Counter()
    with Path(tsv_path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, delimiter='	')
        if not {'image', 'label'}.issubset(reader.fieldnames or []):
            raise ValueError('TSV must contain image and label columns')
        for row in reader:
            label = row['label']
            if label == 'little_or_no_damage':
                counts['excluded'] += 1
                continue
            if label not in {'mild_damage', 'severe_damage'}:
                raise ValueError(f'Unexpected damage label: {label!r}')
            relative = PurePosixPath(row['image'].replace('\\', '/'))
            if relative.is_absolute() or '..' in relative.parts or len(relative.parts) < 3 or relative.parts[0] != 'data_image':
                raise ValueError(f'Unexpected image path: {relative}')
            event = relative.parts[1]
            source = (crisis_root / str(relative)).resolve()
            if not source.is_relative_to(crisis_root):
                raise ValueError('Image path escapes dataset root')
            if not source.is_file():
                print('Missing:', source)
                counts['missing'] += 1
                continue
            # Preserve the dated subpath so identical filenames do not overwrite.
            destination = output_root / split_name / event / label / Path(*relative.parts[2:])
            if destination.exists():
                raise FileExistsError(f'Refusing to overwrite: {destination}')
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            counts['copied'] += 1
    return dict(counts)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--crisis-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='Use a new or empty destination')
    args = parser.parse_args()
    splits = args.crisis_root / 'crisismmd_datasplit_all'
    for filename, split in [('task_damage_text_img_train.tsv','train'), ('task_damage_text_img_dev.tsv','val')]:
        counts = process_split(splits / filename, split, args.crisis_root, args.output)
        print(split, counts)
    print('Finished. Review missing counts before using the output.')

if __name__ == '__main__':
    main()

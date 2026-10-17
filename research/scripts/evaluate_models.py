"""Evaluate one supplied EfficientNet-B0 state_dict checkpoint at a time.
Derived from Amani's two-model evaluation script; no checkpoints are included.
"""
import argparse
import json
from pathlib import Path

def main():
    import torch
    from torch import nn
    from torchvision import datasets, transforms, models
    from torchvision.models import EfficientNet_B0_Weights
    from torch.utils.data import DataLoader
    from sklearn.metrics import classification_report, confusion_matrix
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--dataset', type=Path, required=True, help='Validation class folders')
    parser.add_argument('--classes', type=Path, required=True, help='JSON list of class names in CHECKPOINT output order')
    parser.add_argument('--batch-size', type=int, default=16)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error('batch size must be positive')
    classes = json.loads(args.classes.read_text())
    if not isinstance(classes, list) or len(classes) not in (2, 4) or not all(isinstance(x, str) for x in classes) or len(set(classes)) != len(classes):
        raise ValueError('Classes JSON must contain two or four distinct names in checkpoint output order')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    weights = EfficientNet_B0_Weights.DEFAULT
    transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(), transforms.Normalize(weights.transforms().mean, weights.transforms().std)])
    dataset = datasets.ImageFolder(args.dataset, transform=transform)
    if set(dataset.classes) != set(classes):
        raise ValueError('Validation class names do not match checkpoint class names')
    # ImageFolder sorts folder names; checkpoint metadata determines model output order.
    remap = [classes.index(name) for name in dataset.classes]
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(classes))
    model.load_state_dict(torch.load(args.model, map_location=device, weights_only=True))
    model.to(device).eval()
    predictions, labels = [], []
    with torch.no_grad():
        for images, targets in loader:
            predictions.extend(model(images.to(device)).argmax(1).cpu().tolist())
            labels.extend(remap[index] for index in targets.tolist())
    indices = list(range(len(classes)))
    print('Device:', device, 'Validation size:', len(dataset), 'Class order:', classes)
    print('Accuracy:', sum(p == y for p, y in zip(predictions, labels)) / len(labels))
    print('Confusion matrix (rows=true, columns=predicted):')
    print(confusion_matrix(labels, predictions, labels=indices))
    print(classification_report(labels, predictions, labels=indices, target_names=classes, zero_division=0))

if __name__ == '__main__':
    main()

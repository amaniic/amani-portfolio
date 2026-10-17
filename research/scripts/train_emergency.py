"""Runnable adaptation of Amani's supplied EfficientNet-B0 training script.
See CHANGELOG.md for deliberate changes from the submitted reference.
"""
import argparse
import json
from pathlib import Path

def main():
    import torch
    from torch import nn, optim
    from torch.utils.data import DataLoader
    from torchvision import datasets, transforms, models
    from torchvision.models import EfficientNet_B0_Weights
    from tqdm import tqdm
    from sklearn.metrics import classification_report, confusion_matrix

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True, help='Folder containing train/ and val/')
    parser.add_argument('--output', type=Path, default=Path('models/best_emergency_model.pt'))
    parser.add_argument('--epochs', type=int, default=12)
    parser.add_argument('--batch-size', type=int, default=16)
    parser.add_argument('--lr', type=float, default=1e-4)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.lr <= 0:
        parser.error('epochs, batch size, and learning rate must be positive')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    weights = EfficientNet_B0_Weights.DEFAULT
    mean, std = weights.transforms().mean, weights.transforms().std
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10), transforms.ColorJitter(0.2, 0.2, 0.2, 0.1),
        transforms.ToTensor(), transforms.Normalize(mean, std)])
    val_transform = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(), transforms.Normalize(mean, std)])
    train = datasets.ImageFolder(args.dataset / 'train', transform=train_transform)
    val = datasets.ImageFolder(args.dataset / 'val', transform=val_transform)
    if len(train.classes) != 4 or train.class_to_idx != val.class_to_idx:
        raise ValueError('Expected four classes with identical train/val class mappings')
    train_loader = DataLoader(train, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val, batch_size=args.batch_size, shuffle=False)
    print('Device:', device, 'Classes:', train.class_to_idx)
    print('Train size:', len(train), 'Validation size:', len(val))
    model = models.efficientnet_b0(weights=weights)
    for parameter in model.features.parameters():
        parameter.requires_grad = False
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 4)
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=args.lr)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.with_suffix('.classes.json').write_text(json.dumps(train.classes, indent=2)+'\n')

    def validate():
        model.eval()
        labels, predictions = [], []
        with torch.no_grad():
            for images, targets in val_loader:
                outputs = model(images.to(device))
                labels.extend(targets.tolist())
                predictions.extend(outputs.argmax(1).cpu().tolist())
        accuracy = sum(p == y for p, y in zip(predictions, labels)) / len(labels)
        return accuracy, labels, predictions

    best = -1.0
    for epoch in range(args.epochs):
        model.train()
        # Freeze BatchNorm running statistics as well as backbone gradients.
        model.features.eval()
        loss_sum, correct = 0.0, 0
        for images, labels in tqdm(train_loader, desc=f'Epoch {epoch+1}/{args.epochs}'):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            loss_sum += loss.item() * len(labels)
            correct += (outputs.argmax(1) == labels).sum().item()
        accuracy, _, _ = validate()
        print(f'Train loss: {loss_sum/len(train):.4f}; train acc: {correct/len(train):.4f}; val acc: {accuracy:.4f}')
        if accuracy > best:
            best = accuracy
            torch.save(model.state_dict(), args.output)
            print('Saved best checkpoint:', args.output)
    model.load_state_dict(torch.load(args.output, map_location=device, weights_only=True))
    accuracy, labels, predictions = validate()
    indices = list(range(4))
    print('Best-checkpoint validation accuracy:', accuracy)
    print(confusion_matrix(labels, predictions, labels=indices))
    print(classification_report(labels, predictions, labels=indices,
                                target_names=train.classes, zero_division=0))

if __name__ == '__main__':
    main()

import os

# os = "operating system" utilities.

# We use it mainly for safe path-building (works across Windows/Mac/Linux).

import torch

# PyTorch core library.

# Gives us tensors (like NumPy arrays but optimized for deep learning) and GPU support.

import torch.nn as nn

# torch.nn contains building blocks for neural networks:

# layers (Linear, Conv2d), activations, losses (CrossEntropyLoss), etc.

import torch.optim as optim

# torch.optim contains "optimizers" (Adam, SGD, RMSProp).

# Optimizers apply gradient updates to model parameters so learning happens.

from torchvision import datasets, transforms, models

# torchvision.datasets: common dataset loaders (ImageFolder, CIFAR, etc.)

# torchvision.transforms: preprocessing + augmentation tools for images

# torchvision.models: pretrained CNN architectures (ResNet, EfficientNet, etc.)

from torchvision.models import EfficientNet_B0_Weights

# This provides the *official* pretrained weights configuration for EfficientNet-B0,

# including recommended normalization values and preprocessing.

from torch.utils.data import DataLoader

# DataLoader creates an iterable over the dataset that yields batches of data.

# Handles batching, optional shuffling, and multi-process loading.

from sklearn.metrics import classification_report, confusion_matrix

# scikit-learn metrics:

# confusion_matrix: counts how predictions vs true labels align

# classification_report: precision/recall/F1/support per class

from tqdm import tqdm

# tqdm provides a progress bar so you can *see* training is moving.

import numpy as np

# NumPy is a numerical library.

# Not strictly necessary here, but commonly used (and handy for arrays/metrics).

# ======================

# CONFIG

# ======================

DATASET_DIR = r"C:\AI_Projects\CustomDataset"

# Root directory containing your dataset.

# REQUIRED folder structure for ImageFolder:

# CustomDataset/

#   train/

#     Fire/

#     Flood/

#     InfrastructureDamage/

#     RoadEmergency/

#   val/

#     Fire/

#     Flood/

#     InfrastructureDamage/

#     RoadEmergency/

BATCH_SIZE = 16

# Number of images per batch.

# Training doesn't typically process ALL images at once (too heavy).

# Instead, it processes small batches:

# - forward pass on batch

# - compute loss

# - backprop

# - update weights

# Repeats until all training images have been seen (one epoch).

EPOCHS = 12

# How many times we pass over the FULL training dataset.

# 12 epochs means:

# model sees each training image ~12 times (with random augmentations each time).

LR = 1e-4

# Learning rate.

# This controls how big each weight update step is.

# Too high → training becomes unstable / may diverge.

# Too low → training may be extremely slow or get stuck.

NUM_CLASSES = 4

# Number of categories we want the model to output.

# Here: Fire, Flood, InfrastructureDamage, RoadEmergency

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Chooses device for computation.

# - "cuda" = NVIDIA GPU (fast for deep learning)

# - "cpu"  = slower but works anywhere

print("Using device:", device)

# Prints out what device you're training on.

# In your case it prints cpu.

# ======================

# TRANSFORMS

# ======================

weights = EfficientNet_B0_Weights.DEFAULT

# Loads the default pretrained weight configuration for EfficientNet-B0.

# Important: "weights" also implies a specific preprocessing style (ImageNet-style).

imagenet_mean = weights.transforms().mean

# The mean RGB values used to normalize images during ImageNet training.

# Normalization is like "standardizing" input so the model receives data in the style it expects.

imagenet_std = weights.transforms().std

# The std (standard deviation) RGB values used for ImageNet normalization.

train_transform = transforms.Compose([

    # Compose() means: apply these transforms in order, one after the other.

    transforms.RandomResizedCrop(224),

    # RandomResizedCrop does two things:

    # (1) picks a random part of the image (random crop)

    # (2) resizes that crop to 224x224

    #

    # Why do this?

    # - Forces the model to be robust to framing/zoom differences.

    # - If a user takes a photo "closer" or "farther", model still learns the concept.

    transforms.RandomHorizontalFlip(),

    # Randomly flips the image left-right (usually 50% chance).

    #

    # Why do this?

    # - Many real scenes can be mirrored and still be the same class.

    # - Helps prevent the model from learning "direction-specific" bias.

    transforms.RandomRotation(10),

    # Rotates the image by a random angle between -10 and +10 degrees.

    #

    # Why do this?

    # - Phone images aren’t always level; users tilt cameras.

    # - Model learns to ignore minor rotation.

    transforms.ColorJitter(0.2, 0.2, 0.2, 0.1),

    # Randomly changes color properties:

    # brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1

    #

    # Why do this?

    # - Real photos vary because of sunlight, night lighting, shadows.

    # - Helps model not “cheat” by relying on a specific lighting condition.

    transforms.ToTensor(),

    # Converts PIL image (like a normal image object) into a PyTorch tensor.

    # Also scales pixel values:

    # - Before: 0..255 ints

    # - After:  0..1 floats

    #

    # Deep learning expects numbers in tensor form.

    transforms.Normalize(imagenet_mean, imagenet_std)

    # Normalize each RGB channel:

    # new_pixel = (pixel - mean) / std

    #

    # Why normalize?

    # - EfficientNet pretrained weights expect inputs normalized like ImageNet.

    # - If you skip this, performance often drops because input distribution changes.

])

val_transform = transforms.Compose([

    # Validation transform should be "stable" and not random.

    # Because validation is meant to evaluate fairly and consistently.

    transforms.Resize(256),

    # Resize the image so the shorter side becomes 256 pixels.

    # This is a standard ImageNet evaluation recipe.

    transforms.CenterCrop(224),

    # Take a 224x224 crop from the center.

    # No randomness → consistent evaluation.

    transforms.ToTensor(),

    # Convert to tensor.

    transforms.Normalize(imagenet_mean, imagenet_std)

    # Normalize same as training.

])

# ======================

# DATASETS

# ======================

train_dataset = datasets.ImageFolder(

    os.path.join(DATASET_DIR, "train"),

    transform=train_transform

)

# ImageFolder:

# - looks inside train/

# - each subfolder name becomes a class label

# - each image inside becomes one sample

#

# It also creates:

# train_dataset.classes → list of class names in sorted order

# train_dataset.class_to_idx → mapping {class_name: numeric_label}

val_dataset = datasets.ImageFolder(

    os.path.join(DATASET_DIR, "val"),

    transform=val_transform

)

# Same idea, but for validation set.

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# DataLoader wraps the dataset and yields mini-batches.

# shuffle=True:

# - randomly shuffles the training data each epoch

# - prevents the model from learning “order patterns” in the dataset

# - reduces bias (e.g., if all Fire images appear first every time)

val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# shuffle=False for validation:

# - not required (we don't train on it)

# - keeps evaluation stable and reproducible

print("Classes:", train_dataset.classes)

# Shows the detected class folder names.

# Also reveals the exact order that becomes label indices (0..NUM_CLASSES-1).

print("Train size:", len(train_dataset))

# Total number of training images.

print("Val size:", len(val_dataset))

# Total number of validation images.

# ======================

# MODEL

# ======================

model = models.efficientnet_b0(weights=weights)

# Loads EfficientNet-B0 architecture and fills it with pretrained weights.

#

# Key concept: Transfer Learning

# - The model already learned general features (edges, textures, shapes) from ImageNet.

# - We reuse that knowledge instead of training from scratch.

for param in model.features.parameters():

    param.requires_grad = False

    # Freeze the backbone (feature extractor).

    #

    # "Backbone" = convolutional layers that detect general features.

    # Freezing means:

    # - We do NOT compute gradients for those parameters.

    # - They do NOT update during training.

    #

    # Why freeze?

    # - Dataset is relatively small (~2k images).

    # - Training the full network could overfit fast.

    # - Freezing makes training faster and more stable.

    # - You mostly train only the last classifier layer.

in_features = model.classifier[1].in_features

# EfficientNet’s classifier is something like:

# classifier = Sequential(Dropout(...), Linear(...))

# classifier[1] is the Linear layer.

# .in_features is how many features it receives from the CNN (usually 1280).

model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)

# Replace the final classification layer.

# Pretrained ImageNet model outputs 1000 classes.

# We need 4 classes, so we create a new Linear layer.

model = model.to(device)

# Move the model parameters to CPU or GPU.

# If model is on GPU, inputs must also be on GPU.

criterion = nn.CrossEntropyLoss()

# CrossEntropyLoss is the standard loss for multi-class classification.

# Internally it does:

# - applies Softmax to logits (turns raw scores into probabilities)

# - computes negative log likelihood loss

#

# Important: it expects:

# - outputs = raw logits of shape [batch_size, num_classes]

# - labels = integer class indices of shape [batch_size]

optimizer = optim.Adam(model.classifier.parameters(), lr=LR)

# Adam = optimizer that adapts step sizes automatically per parameter using moving averages.

# In practice:

# - more forgiving than plain SGD

# - usually converges faster early on

#

# We pass model.classifier.parameters() so ONLY the classifier learns.

# Backbone remains frozen.

# ======================

# TRAIN LOOP

# ======================

best_val_acc = 0

# We track the best validation accuracy so we can save the best model checkpoint.

for epoch in range(EPOCHS):

    # This loop runs once per epoch.

    # Each epoch = model sees all training data once (in batches).

    print(f"\nEpoch {epoch+1}/{EPOCHS}")

    # Show progress at epoch level.

    # ----------------------

    # TRAINING PHASE

    # ----------------------

    model.train()

    # Put the model in training mode.

    #

    # Important difference:

    # - training mode activates dropout (if present)

    # - batchnorm layers update their running statistics

    #

    # Even if you don’t think you use dropout, pretrained nets often include it.

    train_loss = 0

    # We'll accumulate loss over batches (optional, for reporting).

    train_correct = 0

    # We'll count how many predictions were correct across training set.

    # Loop over batches in the training loader with a progress bar.

    for images, labels in tqdm(train_loader):

        # Each iteration gives:

        # images: tensor [BATCH_SIZE, 3, 224, 224]

        # labels: tensor [BATCH_SIZE] containing integers 0..3

        images, labels = images.to(device), labels.to(device)

        # Move both images and labels to the same device as the model.

        optimizer.zero_grad()

        # VERY IMPORTANT:

        # Gradients in PyTorch accumulate by default.

        # So we must clear (zero) them before computing new gradients for this batch.

        outputs = model(images)

        # Forward pass:

        # images -> EfficientNet -> outputs (logits)

        #

        # outputs shape: [BATCH_SIZE, NUM_CLASSES]

        # Example per image: [score_fire, score_flood, score_infra, score_road]

        loss = criterion(outputs, labels)

        # Compute how "wrong" the model is.

        # CrossEntropy compares logits vs true labels.

        # Lower loss = better.

        # Loss is computed per batch.

        loss.backward()

        # Backpropagation:

        # Computes gradients d(loss)/d(parameter) for each trainable parameter.

        # Because backbone is frozen, gradients are only calculated for classifier layer.

        optimizer.step()

        # Weight update step:

        # Adam uses gradients to update parameters.

        # This is literally "learning": it changes weights to reduce future loss.

        train_loss += loss.item()

        # loss.item() converts a 1-value tensor into a normal Python float.

        # We accumulate it so we can compute average loss later if we want.

        preds = outputs.argmax(1)

        # Convert logits to predicted class.

        #

        # argmax(1) means:

        # - look across class dimension

        # - pick the index with the largest score

        #

        # preds shape: [BATCH_SIZE]

        train_correct += (preds == labels).sum().item()

        # Compare predicted labels to true labels:

        # (preds == labels) gives True/False per image.

        # .sum() counts how many True.

        # .item() converts to integer.

        # Then add to running total.

    train_acc = train_correct / len(train_dataset)

    # Training accuracy = correct predictions / total training images.

    # This tells how well it’s fitting training set.

    avg_train_loss = train_loss / len(train_loader)

    # Average loss across training batches (more stable than printing last batch loss).

    # ----------------------

    # VALIDATION PHASE

    # ----------------------

    model.eval()

    # Put model in evaluation mode.

    #

    # Key effects:

    # - dropout OFF (so predictions are deterministic)

    # - batchnorm uses stored running mean/var (no updates)

    #

    # Without eval(), validation results can be noisy and unfair.

    val_correct = 0

    # Count correct validation predictions.

    all_preds = []

    # We'll store all predicted labels to compute confusion matrix and classification report.

    all_labels = []

    # We'll store all true labels.

    with torch.no_grad():

        # Disables gradient calculations.

        #

        # Why do this?

        # - We do not train during validation

        # - Saves memory

        # - Runs faster

        for images, labels in val_loader:

            # Iterate over validation batches.

            images, labels = images.to(device), labels.to(device)

            # Move to device.

            outputs = model(images)

            # Forward pass only.

            preds = outputs.argmax(1)

            # Predicted class indices for this batch.

            val_correct += (preds == labels).sum().item()

            # Add number of correct predictions in this batch.

            all_preds.extend(preds.cpu().numpy())

            # Move preds to CPU (scikit-learn needs CPU arrays),

            # convert to NumPy array,

            # and add each element to list.

            all_labels.extend(labels.cpu().numpy())

            # Same process for true labels.

    val_acc = val_correct / len(val_dataset)

    # Validation accuracy = correct predictions / total validation images.

    # This is the score we trust most for real performance.

    print(f"Train Loss: {avg_train_loss:.4f}")

    # Print average training loss for this epoch.

    print(f"Train Acc: {train_acc:.4f}")

    # Print training accuracy.

    print(f"Val Acc: {val_acc:.4f}")

    # Print validation accuracy.

    if val_acc > best_val_acc:

        # If current model is the best we've seen so far, we save it.

        best_val_acc = val_acc

        # Update best score tracker.

        torch.save(model.state_dict(), "best_emergency_model.pt")

        # Save ONLY the weights (state_dict) to disk.

        # This is your "best checkpoint" model.

        print("Saved best model.")

        # Confirmation message.

# ======================

# FINAL REPORT

# ======================

print("\nFinal Validation Report")

# Header for readability.

print(confusion_matrix(all_labels, all_preds))

# Confusion matrix:

# Rows = true labels

# Columns = predicted labels

# Diagonal = correct predictions

# Off-diagonal = mistakes (which classes are confused with which)

print(classification_report(all_labels, all_preds, target_names=train_dataset.classes))

# classification_report prints:

# precision, recall, f1-score, support for each class

# Precision = True Positives / (True Positives + False Positives); measures how many predicted positives are actually correct.

# Recall = True Positives / (True Positives + False Negatives); measures how many actual positives the model successfully detected.

# F1-score = 2 * (Precision * Recall) / (Precision + Recall); harmonic mean balancing precision and recall.

# Support is the number of true samples belonging to each class in the validation dataset.

print("Best Val Accuracy:", best_val_acc)

# Shows the highest validation accuracy achieved across all epochs.

# Validation accuracy = correct predictions / total validation samples; used as primary generalization performance metric.

# Amani Ibrahim Carbonell

Computer Engineering student at the University of South Florida, with a minor in Biomedical Physics. Expected graduation: May 2028.

My interests include applied machine learning, computer vision, and software engineering.

## Projects and source

| Folder | Contents |
| --- | --- |
| [research](research/) | My supplied EfficientNet-B0 emergency training code, model evaluation, and CrisisMMD preparation, organized with AI assistance |
| [cinevault](cinevault/) | Java/Spring Boot movie inventory with a local H2 database |
| [site](site/) | HTML, CSS, and JavaScript for my portfolio website |

### Emergency image classification

At the Polytechnic University of Puerto Rico, I developed two EfficientNet-B0 classifiers as part of undergraduate research into a proposed emergency-reporting system for Puerto Rico.

| Task | Reported best validation accuracy | Context |
| --- | ---: | --- |
| Four-class hazard classification | 94.07% | 388 validation images; macro F1 reported as 0.94 |
| Binary damage severity | 79.57% | Best result across training stages; final Stage 2 confusion matrix corresponds to approximately 77.24% |

These are results reported in my research, not newly reproduced runs or independent external tests. The supplied training script represents one training stage, not the complete history behind those best results. See [research/README.md](research/README.md) for run instructions, source provenance, limitations, and documented adaptations. Data and saved model weights are not included; severity training code was not supplied.

### CineVault — Movie Inventory

A Java web application for managing a personal movie collection, developed for CECS 3210: Advanced Programming.

Features include adding, viewing, editing, and deleting movies; movie-ID lookup; duplicate prevention; input validation; and a persistent local H2 database. Built with Spring Boot, Thymeleaf, Spring Data JPA, HTML, CSS, and JavaScript, with four passing integration tests.

See [cinevault/README.md](cinevault/README.md) for setup and usage instructions.

## View the portfolio locally

1. Download this repository as a ZIP using **Code → Download ZIP** and extract it.
2. Open a terminal in the extracted folder containing this README.
3. Run this command **in the terminal**:

```sh
python3 -m http.server 8000 --directory site
```

On Windows, use `py -m http.server 8000 --directory site` if needed.

4. Leave the terminal open and visit [http://localhost:8000](http://localhost:8000) in your browser.

The local address only works while the server is running on your computer. The public website source omits the résumé and private contact details.

## Connect

[LinkedIn](https://www.linkedin.com/in/amani-ibr)

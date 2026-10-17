# CineVault — reconstructed movie inventory

**Status: a new, AI-assisted reconstruction from a project manual, not the recovered original source code.**

The original CECS 3210: Advanced Programming team project (2025) was created by **Amani Ibrahim Carbonell and Arianys Coll-cuchi Escuté**. This implementation was written in 2026 using the supplied manual and screenshots as a behavioral reference. It does not establish either teammate's individual contribution to the original project.

## What it does

- Add, view, edit, and delete movies using a web interface.
- Store title, director, plot, rating, budget, release date, and an optional poster path.
- Find movies by ID and browse a poster-card inventory.
- Reject duplicate title/director/release-year combinations, including case and repeated-whitespace variations.
- Save the inventory to a local H2 database across restarts.
- Display validation messages, a delete confirmation, Help, and About pages.

## Run locally

Install a **JDK 17 or newer** and **Apache Maven 3.6.3 or newer**. A Java runtime alone is not enough.

1. Extract this project and open a terminal in the folder containing `pom.xml`.
2. Run `mvn test` to run the integration tests.
3. Run `mvn spring-boot:run` and leave the terminal open.
4. Open **http://localhost:8080** in a browser.
5. Stop the server with Ctrl+C.

The URL only works while the application is running on your computer. This is a Java server application; double-clicking the HTML templates will not run it.

For a runnable JAR: `mvn package`, then `java -jar target/cinevault-1.0.0.jar`.

## Source guide

| File | Purpose |
| --- | --- |
| `Movie.java` | Movie fields and validation rules |
| `MovieRepository.java` | Database queries through Spring Data JPA |
| `MovieService.java` | CRUD behavior and duplicate checks |
| `MovieController.java` | Browser routes and form handling |
| `WebSecurity.java` | CSRF protection for form submissions |
| `templates/` | Thymeleaf HTML pages |
| `static/style.css` | Dark, lavender-accented layout |
| `CineVaultIntegrationTest.java` | CRUD, duplicate, validation, and rendering checks |

Java files are under `src/main/java/com/cinevault`; templates and static files are under `src/main/resources`.

## Reconstruction choices

The manual documents Spring Boot, HTML/CSS, Bootstrap, and H2. This version uses Spring Boot, Thymeleaf, JPA, H2, and custom CSS. The architecture, field types, templates, and tests here are newly written choices, not claims about the missing implementation. The original poster collage and Bootstrap dependency are not reproduced. Budget is entered as a numeric USD amount instead of shorthand such as “34M.” Posters are optional files placed in `src/main/resources/static/posters` and referenced as `/posters/example.jpg`; no image upload is implemented.

There is no account system. The server binds to loopback for local use. CSRF protection is enabled, but this class-project reconstruction has not been hardened for public multi-user deployment. The H2 files are stored in `data/`, excluded from Git. Delete `data/` only if you intend to erase your inventory.

No research scripts, student IDs, personal contact information, original private database, or original movie poster assets are included. No license is asserted for the original team project.

## Validation

Compiled and ran the four Spring Boot integration tests during reconstruction: all passed. These cover CRUD, duplicate rules, HTML template rendering/escaping, ID lookup, invalid input, CSRF, and deletion. Browser visual review and production deployment have not been performed.

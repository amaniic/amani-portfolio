# CineVault — Movie Inventory

A Java web application for organizing a personal movie collection, developed for CECS 3210: Advanced Programming.

Built with Spring Boot, Thymeleaf, Spring Data JPA, H2, HTML, CSS, and JavaScript.

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

## Using the inventory

Enter budgets as numeric amounts in US dollars. Posters are optional local files: place an image in `src/main/resources/static/posters` and use its path, such as `/posters/example.jpg`.

The inventory is stored in a local H2 database in `data/`, excluded from Git. Movies remain available after restarting the application. Deleting `data/` erases the inventory.

The application runs locally with CSRF protection for forms. It has no account system.

## Validation

All four Spring Boot integration tests pass. These cover CRUD, duplicate rules, HTML template rendering/escaping, ID lookup, invalid input, CSRF, and deletion. Browser visual review and production deployment have not been performed.

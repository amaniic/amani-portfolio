package com.cinevault;
import java.math.BigDecimal;
import java.time.LocalDate;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import static org.assertj.core.api.Assertions.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
@SpringBootTest @AutoConfigureMockMvc
class CineVaultIntegrationTest {
    @Autowired MovieService service;
    @Autowired MovieRepository repository;
    @Autowired MockMvc web;
    @BeforeEach void clear() { repository.deleteAll(); }
    Movie movie(String title, String director, int year) {
        Movie m = new Movie(); m.setTitle(title); m.setDirector(director);
        m.setPlot("A fictional movie used for testing."); m.setRating("PG");
        m.setBudget(new BigDecimal("1000.00")); m.setReleaseDate(LocalDate.of(year, 1, 1));
        return m;
    }
    @Test void crudAndNotFound() {
        Movie saved = service.save(movie("Test Movie", "A Director", 2025), null);
        assertThat(service.all()).hasSize(1);
        Movie edit = movie("Updated Movie", "A Director", 2025);
        service.save(edit, saved.getId());
        assertThat(service.get(saved.getId()).getTitle()).isEqualTo("Updated Movie");
        service.delete(saved.getId());
        assertThat(service.all()).isEmpty();
        assertThatThrownBy(() -> service.get(saved.getId())).isInstanceOf(org.springframework.web.server.ResponseStatusException.class);
    }
    @Test void duplicateRuleAndAllowedVariations() {
        Movie first = service.save(movie("The  Movie", "A Director", 2025), null);
        assertThatThrownBy(() -> service.save(movie(" the movie ", "a director", 2025), null))
            .isInstanceOf(MovieService.DuplicateMovieException.class);
        service.save(movie("the movie", "a director", 2026), null);
        service.save(movie("the movie", "Another Director", 2025), null);
        service.save(movie("The Movie", "A Director", 2025), first.getId());
        assertThat(repository.count()).isEqualTo(3);
    }
    @Test void rendersTemplatesAndEscapesMovieText() throws Exception {
        Movie saved = service.save(movie("<script>alert(1)</script>", "Director", 2025), null);
        for (String url : new String[]{"/", "/movies", "/movies/new", "/help", "/about", "/movies/"+saved.getId(), "/movies/"+saved.getId()+"/edit"})
            web.perform(get(url)).andExpect(status().isOk());
        web.perform(get("/movies/"+saved.getId())).andExpect(content().string(org.hamcrest.Matchers.containsString("&lt;script&gt;")));
        web.perform(get("/lookup").param("id", saved.getId().toString()).param("action", "edit"))
            .andExpect(redirectedUrl("/movies/"+saved.getId()+"/edit"));
        web.perform(get("/movies/999999")).andExpect(status().isNotFound());
    }
    @Test void formValidationCsrfAndDelete() throws Exception {
        web.perform(post("/movies")).andExpect(status().isForbidden());
        web.perform(post("/movies").with(csrf()).param("title", "").param("budget", "-1"))
            .andExpect(status().isOk()).andExpect(view().name("form"));
        assertThat(repository.count()).isZero();
        web.perform(post("/movies").with(csrf()).param("title", "Example").param("director", "Director")
            .param("plot", "Example plot").param("rating", "PG").param("budget", "1000")
            .param("releaseDate", "2025-01-01").param("poster", ""))
            .andExpect(status().is3xxRedirection());
        Movie saved = service.all().get(0);
        web.perform(post("/movies/"+saved.getId()+"/delete").with(csrf()))
            .andExpect(redirectedUrl("/movies"));
        assertThat(repository.count()).isZero();
    }
}

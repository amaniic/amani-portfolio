package com.cinevault;
import jakarta.validation.Valid;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
@Controller
public class MovieController {
    private final MovieService movies;
    public MovieController(MovieService movies) { this.movies = movies; }
    @GetMapping("/") String home() { return "home"; }
    @GetMapping("/help") String help() { return "help"; }
    @GetMapping("/about") String about() { return "about"; }
    @GetMapping("/movies") String list(Model model) { model.addAttribute("movies", movies.all()); return "list"; }
    @GetMapping("/movies/new") String create(Model model) {
        model.addAttribute("movie", new Movie()); return "form";
    }
    @GetMapping("/movies/{id}") String detail(@PathVariable long id, Model model) {
        model.addAttribute("movie", movies.get(id)); return "detail";
    }
    @GetMapping("/movies/{id}/edit") String edit(@PathVariable long id, Model model) {
        model.addAttribute("movie", movies.get(id)); return "form";
    }
    @GetMapping("/lookup") String lookup(@RequestParam long id, @RequestParam(defaultValue="view") String action) {
        movies.get(id);
        return "redirect:/movies/" + id + (action.equals("edit") ? "/edit" : "");
    }
    @PostMapping("/movies") String add(@Valid @ModelAttribute("movie") Movie movie, BindingResult errors) {
        return save(movie, null, errors);
    }
    @PostMapping("/movies/{id}") String update(@PathVariable long id, @Valid @ModelAttribute("movie") Movie movie, BindingResult errors) {
        movies.get(id); movie.setId(id); return save(movie, id, errors);
    }
    private String save(Movie movie, Long id, BindingResult errors) {
        if (errors.hasErrors()) return "form";
        try { return "redirect:/movies/" + movies.save(movie, id).getId(); }
        catch (MovieService.DuplicateMovieException | DataIntegrityViolationException e) {
            errors.reject("duplicate", "A movie with this title, director, and release year already exists.");
            return "form";
        }
    }
    @PostMapping("/movies/{id}/delete") String delete(@PathVariable long id) {
        movies.delete(id); return "redirect:/movies";
    }
}

package com.cinevault;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
@Service
public class MovieService {
    private final MovieRepository movies;
    public MovieService(MovieRepository movies) { this.movies = movies; }
    public List<Movie> all() { return movies.findAll(Sort.by("title").ascending()); }
    public Movie get(long id) {
        return movies.findById(id).orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Movie not found"));
    }
    @Transactional
    public Movie save(Movie input, Long id) {
        input.prepareKeys();
        var duplicate = movies.findByTitleKeyAndDirectorKeyAndReleaseYear(input.getTitleKey(), input.getDirectorKey(), input.getReleaseYear());
        if (duplicate.isPresent() && !duplicate.get().getId().equals(id))
            throw new DuplicateMovieException();
        Movie target = id == null ? new Movie() : get(id);
        target.setTitle(input.getTitle()); target.setDirector(input.getDirector());
        target.setPlot(input.getPlot()); target.setRating(input.getRating());
        target.setBudget(input.getBudget()); target.setReleaseDate(input.getReleaseDate());
        target.setPoster(input.getPoster()); target.prepareKeys();
        return movies.saveAndFlush(target);
    }
    @Transactional
    public void delete(long id) { movies.delete(get(id)); }
    public static class DuplicateMovieException extends RuntimeException {}
}

package com.cinevault;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
public interface MovieRepository extends JpaRepository<Movie, Long> {
    Optional<Movie> findByTitleKeyAndDirectorKeyAndReleaseYear(String titleKey, String directorKey, int year);
}

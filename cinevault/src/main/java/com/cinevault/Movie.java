package com.cinevault;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.time.LocalDate;
@Entity
@Table(name="movies", uniqueConstraints=@UniqueConstraint(columnNames={"title_key", "director_key", "release_year"}))
public class Movie {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    @NotBlank @Size(max=200)
    private String title;
    @NotBlank @Size(max=200)
    private String director;
    @NotBlank @Size(max=4000)
    @Column(length=4000)
    private String plot;
    @NotBlank @Pattern(regexp="G|PG|PG-13|R|NC-17|NR")
    private String rating;
    @NotNull @DecimalMin("0.0") @Digits(integer=12, fraction=2)
    private BigDecimal budget;
    @NotNull
    private LocalDate releaseDate;
    @Size(max=500) @Pattern(regexp="^$|/posters/[A-Za-z0-9._-]+", message="Use a local /posters/filename path, or leave blank")
    private String poster = "";
    @Column(name="title_key", nullable=false, length=200) private String titleKey;
    @Column(name="director_key", nullable=false, length=200) private String directorKey;
    @Column(name="release_year", nullable=false) private int releaseYear;
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String value) { this.title = value; }
    public String getDirector() { return director; }
    public void setDirector(String value) { this.director = value; }
    public String getPlot() { return plot; }
    public void setPlot(String value) { this.plot = value; }
    public String getRating() { return rating; }
    public void setRating(String value) { this.rating = value; }
    public BigDecimal getBudget() { return budget; }
    public void setBudget(BigDecimal value) { this.budget = value; }
    public LocalDate getReleaseDate() { return releaseDate; }
    public void setReleaseDate(LocalDate value) { this.releaseDate = value; }
    public String getPoster() { return poster; }
    public void setPoster(String value) { this.poster = value; }
    public void prepareKeys() {
        title = title.strip(); director = director.strip();
        titleKey = title.toLowerCase(java.util.Locale.ROOT).replaceAll("\\s+", " ");
        directorKey = director.toLowerCase(java.util.Locale.ROOT).replaceAll("\\s+", " ");
        releaseYear = releaseDate.getYear();
    }
    public String getTitleKey() { return titleKey; }
    public String getDirectorKey() { return directorKey; }
    public int getReleaseYear() { return releaseYear; }
}

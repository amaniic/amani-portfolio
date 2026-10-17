package com.cinevault;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
@Configuration
public class WebSecurity {
    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // Local, single-user project. Keep CSRF protection for all mutations.
        return http.authorizeHttpRequests(a -> a.anyRequest().permitAll()).build();
    }
}

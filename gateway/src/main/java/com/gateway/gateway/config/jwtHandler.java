package com.gateway.gateway.config;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class jwtHandler {

    @Value("${security.jwt.secret}")
    private String SECRET;

    public void validateToken(final String token) {
    try {
        Jwts.parserBuilder()
            .setSigningKey(getSignKey())
            .build()
            .parseClaimsJws(token);
    } catch (ExpiredJwtException e) {
        System.out.println("Token expirado");
        throw new RuntimeException("Token expirado", e);
    } catch (Exception e) {
        System.out.println("Token inválido: " + e.getMessage());
        throw new RuntimeException("Token inválido", e);
    }
}

    private Key getSignKey() {
        // usar directamente UTF-8 para consistency con micro-users
        byte[] keyBytes = SECRET.getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}

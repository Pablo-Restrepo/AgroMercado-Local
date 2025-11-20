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
        byte[] keyBytes;
        try {
            // intentar interpretar SECRET como base64 (recomendado)
            keyBytes = Decoders.BASE64.decode(SECRET.trim());
        } catch (IllegalArgumentException ex) {
            // fallback: usar bytes UTF-8 del secret (legacy/dev)
            System.out.println("SECRET no es base64, usando bytes UTF-8 como fallback (mejor usar base64 de 32 bytes)");
            keyBytes = SECRET.getBytes(StandardCharsets.UTF_8);
        } catch (Exception e) {
            System.out.println("Error al decodificar la secret key: " + e.getMessage());
            throw new RuntimeException("Error al decodificar la secret key", e);
         }
        return Keys.hmacShaKeyFor(keyBytes);
    }
}

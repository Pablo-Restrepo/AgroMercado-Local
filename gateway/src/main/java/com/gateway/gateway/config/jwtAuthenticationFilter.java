package com.gateway.gateway.config;

import java.util.List;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.stereotype.Component;
import org.springframework.util.AntPathMatcher;
import org.springframework.http.server.reactive.ServerHttpRequest;

@Component
public class jwtAuthenticationFilter extends AbstractGatewayFilterFactory<jwtAuthenticationFilter.Config> {

    @Autowired
    private jwtHandler jwtHandler;

    public jwtAuthenticationFilter() {
        super(Config.class);
    }

    @Override
    public GatewayFilter apply(Config config) {
        return ((exchange, chain) -> {
            ServerHttpRequest request = exchange.getRequest();
            String path = request.getURI().getPath();
            String method = request.getMethod().toString();
            // Si el endpoint y método son públicos, saltar validación
            if (isPublic(path, method, config.getPublicEndpoints())) {
                return chain.filter(exchange);
            }

            String authHeader = exchange.getRequest().getHeaders().get(HttpHeaders.AUTHORIZATION).get(0);
            if (authHeader != null && authHeader.startsWith("Bearer ")) {
                authHeader = authHeader.substring(7);
                try {
                    jwtHandler.validateToken(authHeader);
                    return chain.filter(exchange);
                } catch (Exception e) {
                    exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                    return exchange.getResponse().setComplete();
                }
            } else {
                exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                return exchange.getResponse().setComplete();
            }

        });

    }

    private boolean isPublic(String path, String method, List<PublicEndpoint> publicEndpoints) {
        if (publicEndpoints == null)
            return false;
        AntPathMatcher pathMatcher = new AntPathMatcher();

        return publicEndpoints.stream().anyMatch(endpoint -> pathMatcher.match(endpoint.getPath(), path) &&
                (endpoint.getMethods() == null || endpoint.getMethods().contains(method)));
    }

    // -------------------------------
    // Configuración del filtro
    // -------------------------------
    public static class Config {
        private List<PublicEndpoint> publicEndpoints;

        public List<PublicEndpoint> getPublicEndpoints() {
            return publicEndpoints;
        }

        public void setPublicEndpoints(List<PublicEndpoint> publicEndpoints) {
            this.publicEndpoints = publicEndpoints;
        }
    }

    // -------------------------------
    // Clase auxiliar para cada endpoint público
    // -------------------------------
    public static class PublicEndpoint {
        private String path;
        private List<String> methods;

        public String getPath() {
            return path;
        }

        public void setPath(String path) {
            this.path = path;
        }

        public List<String> getMethods() {
            return methods;
        }

        public void setMethods(List<String> methods) {
            this.methods = methods;
        }
    }

}

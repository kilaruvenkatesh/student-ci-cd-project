FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy frontend files
COPY index.html /usr/share/nginx/html/index.html

# Expose port
EXPOSE 80

FROM nginx:alpine

# Copy static files to Nginx directory
COPY . /usr/share/nginx/html

# Use sample admin config as default for deployment
RUN mv /usr/share/nginx/html/admin-config.sample.json /usr/share/nginx/html/admin-config.json

# Expose the port for the frontend
EXPOSE 80

# Use default Nginx configuration
CMD ["nginx", "-g", "daemon off;"]
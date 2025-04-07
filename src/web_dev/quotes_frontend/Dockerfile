FROM nginx:alpine

# Copy static files to Nginx directory
COPY . /usr/share/nginx/html

# Expose the port for the frontend
EXPOSE 80

# Use default Nginx configuration
CMD ["nginx", "-g", "daemon off;"]
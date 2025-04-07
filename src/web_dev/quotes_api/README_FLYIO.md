# Fly.io Deployment Guide for Quotes API

This guide provides step-by-step instructions for deploying, building, and updating your FastAPI Quotes application on Fly.io.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Deployment](#initial-deployment)
- [Deployment Commands](#deployment-commands)
- [Viewing and Managing Your Application](#viewing-and-managing-your-application)
- [Common Deployment Tasks](#common-deployment-tasks)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

1. Installed the Fly CLI (`flyctl` or `fly`):
   ```bash
   # macOS with Homebrew
   brew install flyctl
   
   # Other platforms
   curl -L https://fly.io/install.sh | sh
   ```

2. Signed up for Fly.io and authenticated:
   ```bash
   fly auth login
   ```

3. Prepared your FastAPI application with:
   - A `requirements.txt` file listing all dependencies
   - A `Dockerfile` for containerization
   - (Optional but recommended) A `fly.toml` configuration file

## Initial Deployment

To deploy your application to Fly.io for the first time:

1. Navigate to your project directory:
   ```bash
   cd /Volumes/SN770/source code/python/proj1/src/web_dev/quotes_api
   ```

2. Launch a new Fly app (this will guide you through setup if you don't have a fly.toml):
   ```bash
   fly launch
   ```
   
   This interactive command will:
   - Ask you to name your application (or generate a name)
   - Select a region for deployment
   - Ask about database setup (if needed)
   - Detect your Dockerfile and build your application
   - Create a `fly.toml` configuration file

3. Deploy your application:
   ```bash
   fly deploy
   ```

## Deployment Commands

### Basic Commands

```bash
# Deploy your application
fly deploy

# Check application status
fly status

# View application logs
fly logs

# Open the application URL in your browser
fly open

# SSH into your application
fly ssh console
```

### Volume Management

For persistent storage (like your SQLite database):

```bash
# Create a volume
fly volumes create quotes_data --size 1 --region ord

# List volumes
fly volumes list

# Delete a volume (CAUTION: will delete all data)
fly volumes delete <volume-id>
```

### Scaling

```bash
# Scale to more instances
fly scale count 2

# Scale down to a single instance
fly scale count 1

# Change machine size
fly scale vm shared-cpu-1x
```

## Viewing and Managing Your Application

### Monitoring

```bash
# View application metrics and status
fly status

# Monitor application (real-time dashboard)
fly monitoring

# View detailed logs
fly logs
```

### Application Management

```bash
# Restart the application
fly apps restart

# Stop the application
fly apps stop

# Start the application
fly apps start
```

### Environment Variables

```bash
# Set environment variables
fly secrets set KEY=VALUE

# List environment variables
fly secrets list
```

## Common Deployment Tasks

### Updating Your Application

After making changes to your code:

1. Commit your changes
2. Run `fly deploy`

### Database Migrations

If you need to run database migrations:

1. SSH into your application:
   ```bash
   fly ssh console
   ```

2. Navigate to your application directory and run migration scripts

### Accessing Your SQLite Database

To access your SQLite database:

```bash
# SSH into your application
fly ssh console

# Navigate to the data directory
cd /app/data

# Use SQLite to access your database
sqlite3 quotes.db
```

### Backing Up Your Database

To create a backup of your SQLite database:

```bash
# SSH into your application
fly ssh console

# Copy the database file
cp /app/data/quotes.db /app/data/quotes_backup.db

# Exit the SSH session
exit

# Download the backup file locally
fly sftp get /app/data/quotes_backup.db ./local_backup.db
```

## Troubleshooting

### Common Issues

1. **Application not responding:**
   ```bash
   fly status
   fly logs
   ```

2. **Deployment failures:**
   ```bash
   fly deploy --verbose
   ```

3. **Volume issues:**
   ```bash
   fly volumes list
   ```

4. **Connection issues:**
   - Check your `fly.toml` to ensure ports are correctly configured
   - Verify the application is listening on `0.0.0.0` not just `127.0.0.1`

### Support Resources

- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io Community](https://community.fly.io/)
- [Fly.io Status Page](https://status.fly.io/)

## Additional Notes

- Your application is accessible at: `https://quotes-api-thrumming-log-8356.fly.dev/`
- API documentation is available at: `https://quotes-api-thrumming-log-8356.fly.dev/docs`
- Remember that idle applications will automatically stop to save resources, and will restart when traffic is received
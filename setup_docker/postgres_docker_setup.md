# PostgreSQL Docker Setup Guide

This guide walks you through setting up PostgreSQL using Docker and Docker Compose.

## Prerequisites
- Docker installed and running
- Docker Compose installed
- Basic understanding of Docker concepts

## Setup Steps

### 1. Create Docker Compose File
Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: local_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### 2. Start PostgreSQL Container
Run the following command in the directory containing your `docker-compose.yml`:
```bash
docker compose up -d
```

### 3. Verify Container Status
Check if the container is running:
```bash
docker ps
```

Expected output should show something like:
```
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS         PORTS                    NAMES
b21e84b4fc4f   postgres:latest   "docker-entrypoint.s…"   16 seconds ago   Up 8 seconds   0.0.0.0:5432->5432/tcp   local_postgres
```

## Connection Details

- Host: localhost
- Port: 5432
- Username: postgres
- Password: postgres
- Default database: testdb

## Connecting to PostgreSQL

### 1. Using psql Command Line (if installed locally)
```bash
psql -h localhost -p 5432 -U postgres -d testdb
```

### 2. Using Docker Container's psql
```bash
docker exec -it local_postgres psql -U postgres -d testdb
```

### 3. Using GUI Tools
You can connect using various GUI tools:
- pgAdmin 4
- DBeaver
- DataGrip

Connection parameters remain the same as listed above.

## Common Operations

### View Logs
```bash
docker logs local_postgres
```

### Stop Container
```bash
docker compose down
```

### Stop Container and Remove Data
```bash
docker compose down -v
```

### Restart Container
```bash
docker compose restart
```

## Data Persistence
- Data is persisted in a Docker volume named `postgres_data`
- Volume location: `/var/lib/docker/volumes/setup_docker_postgres_data/_data`
- The volume survives container restarts and removals
- Data remains intact unless you explicitly remove the volume

### Volume Management Commands
```bash
# Inspect volume details
docker volume inspect setup_docker_postgres_data

# List all Docker volumes
docker volume ls

# Remove volume (caution: this will delete all data!)
docker volume rm setup_docker_postgres_data
```

Note: The volume directory is managed by Docker and requires root privileges to access directly. It's recommended to use Docker commands and PostgreSQL tools for data management rather than accessing the volume directory directly.

## Security Considerations
- The current setup uses basic credentials for demonstration
- For production:
  - Use strong passwords
  - Consider using Docker secrets
  - Restrict network access
  - Enable SSL/TLS
  - Configure proper user permissions

## Troubleshooting

### 1. Port Conflict
If port 5432 is already in use:
- Stop any existing PostgreSQL instances
- Or modify the port mapping in docker-compose.yml:
  ```yaml
  ports:
    - "5433:5432"  # Maps to port 5433 on host
  ```

### 2. Connection Issues
- Verify the container is running: `docker ps`
- Check container logs: `docker logs local_postgres`
- Ensure no firewall is blocking port 5432
- Verify correct credentials are being used

### 3. Performance Issues
- Monitor container resources: `docker stats local_postgres`
- Adjust PostgreSQL configuration if needed
- Consider mounting configuration file for custom settings

## Stopping and Cleaning Up

### 1. Stop PostgreSQL Container
To stop the PostgreSQL container while preserving the data:
```bash
# Using Docker Compose (recommended)
docker compose down

# Alternative using Docker commands
docker stop local_postgres
docker rm local_postgres
```

### 2. Verify Container Status
Check if the container has been stopped and removed:
```bash
docker ps -a
```
If the container is not listed, it has been successfully removed.

### 3. Remove PostgreSQL Image (Optional)
If you want to remove the PostgreSQL image:
```bash
# List images first to verify
docker images

# Remove the PostgreSQL image
docker rmi postgres:latest
```

### 4. Clean Up Options
Different levels of cleanup:

```bash
# Stop containers only (preserves data and images)
docker compose down

# Stop containers and remove volumes (DELETES ALL DATA!)
docker compose down -v

# Stop containers and remove images
docker compose down --rmi all

# Complete cleanup (stops containers, removes volumes and images)
docker compose down -v --rmi all
```

Note: Be very careful with the `-v` flag as it will delete all your database data permanently.

### 5. Network Cleanup
Docker Compose automatically manages networks:
- The default network is removed when running `docker compose down`
- To list networks: `docker network ls`
- To remove a specific network: `docker network rm network_name`

## Backup and Restore

### Create Backup
```bash
docker exec -t local_postgres pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

### Restore from Backup
```bash
cat your_dump.sql | docker exec -i local_postgres psql -U postgres
```

## Additional Resources
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

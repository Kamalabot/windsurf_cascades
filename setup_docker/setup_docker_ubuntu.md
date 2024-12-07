# Docker Installation Guide for Ubuntu

This guide will walk you through the process of installing Docker on Ubuntu.

## Prerequisites
- Ubuntu operating system
- Sudo privileges
- Stable internet connection

## Installation Steps

### 1. Update Package Index
```bash
sudo apt update
```

### 2. Install Required Dependencies
Install packages to allow apt to use HTTPS repositories:
```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

### 3. Add Docker's GPG Key
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

### 4. Add Docker Repository
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

### 5. Update Package Database
```bash
sudo apt update
```

### 6. Install Docker
```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 7. Verify Installation
Run the hello-world container to verify that Docker is installed correctly:
```bash
sudo docker run hello-world
```

### 8. (Optional) Run Docker without Sudo
Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```
**Note**: You'll need to log out and back in for this change to take effect.

## Verification
Check Docker version:
```bash
docker --version
```

## Basic Docker Commands

Here are some essential Docker commands to get you started:

- `docker ps`: List running containers
- `docker ps -a`: List all containers (including stopped ones)
- `docker images`: List downloaded images
- `docker pull <image_name>`: Download a Docker image
- `docker run <image_name>`: Run a container from an image
- `docker stop <container_id>`: Stop a running container
- `docker rm <container_id>`: Remove a container
- `docker rmi <image_id>`: Remove an image

## Cleaning Up Docker Resources

### 1. Remove Test Container
```bash
# List all containers (running and stopped)
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
78baaf221efa   hello-world   "/hello"   10 minutes ago   Exited (0) 10 minutes ago            upbeat_satoshi

# Remove the container using its ID or name
$ docker rm 78baaf221efa
78baaf221efa
```

### 2. Remove Test Image
```bash
# List all images
$ docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
hello-world   latest    d2c94e258dcb   19 months ago   13.3kB

# Remove the hello-world image
$ docker rmi hello-world
Untagged: hello-world:latest
Untagged: hello-world@sha256:305243c734571da2d100c8c8b3c3167a098cab6049c9a5b066b6021a60fcb966
Deleted: sha256:d2c94e258dcb3c5ac2798d32e1249e42ef01cba4841c2234249495f87264ac5a
Deleted: sha256:ac28800ec8bb38d5c35b49d45a6ac4777544941199075dff8c4eb63e093aa81e
```

### 3. Verify Cleanup
```bash
# Verify no containers remain
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

# Verify image is removed
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
```

### Common Cleanup Commands
```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Remove all unused Docker objects (containers, images, networks, and volumes)
docker system prune

# Remove everything including volumes (CAUTION: this will delete all data!)
docker system prune -a --volumes
```

Note: Be careful with prune commands, especially when using the `--volumes` flag, as they will permanently delete resources and data.

## Test Results and Examples

### 1. Docker Service Status
```bash
$ systemctl status docker
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running)
     Docs: https://docs.docker.com
```
This shows that Docker is properly installed, running, and enabled to start on boot.

### 2. Hello World Test
```bash
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

### 3. View Running Containers
```bash
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
78baaf221efa   hello-world   "/hello"   9 seconds ago    Exited (0) 8 seconds ago             upbeat_satoshi
```

### 4. View Downloaded Images
```bash
$ docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
hello-world   latest    d2c94e258dcb   19 months ago   13.3kB
```

These test results confirm that:
- Docker service is running correctly
- Container creation and execution work as expected
- Image pulling from Docker Hub is functioning
- Container management commands are working properly

## Troubleshooting

If you encounter any issues:

1. Verify the Docker daemon is running:
```bash
sudo systemctl status docker
```

2. If the service is not running, start it:
```bash
sudo systemctl start docker
```

3. To enable Docker to start on boot:
```bash
sudo systemctl enable docker
```

## Additional Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/) - Repository for Docker images

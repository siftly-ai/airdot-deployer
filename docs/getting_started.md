# Airdot setup
This page provides detailed description for setting up airdot for following scenerios

- Local setup (basic without cluster)
- Local setup (basic with kind cluster setup)

## 📋 Local setup (basic without cluster)

This setup is for users who only want's to test airdot and are not much familier with how to setup local cluster or just want's to get hands-on quickly:

### Docker Install
Please visit the appropriate links to install Docker on your machine:
- For macOS, visit [here](https://docs.docker.com/desktop/install/mac-install/)
- For Windows, visit [here](https://docs.docker.com/desktop/install/windows-install/)
- For Linux, visit [here](https://docs.docker.com/desktop/install/linux-install/)

### Install Airdot python package

```bash
pip install airdot
```

### setting up minio and redis on local machine

Since for local setup airdot requires a test bucket we uses local minio for object storage and redis for storing metadata for user ML microservice to setup both you only need to run following command in terminal.

```bash
docker network create minio-network && wget  https://raw.githubusercontent.com/airdot-io/airdot-deployer/main/docker-compose.yaml && docker-compose -p airdot up
```

#### S2I install
For Mac
You can either follow the installation instructions for Linux (and use the darwin-amd64 link) or you can just install source-to-image with Homebrew:

```$ brew install source-to-image```

For Linux just run following command

```bash
curl -s https://api.github.com/repos/openshift/source-to-image/releases/latest| grep browser_download_url | grep linux-amd64 | cut -d '"' -f 4  | wget -qi -
```
For Windows please follow instruction [here](https://github.com/openshift/source-to-image#for-windows)


## 💻 Airdot Deployer Installation
Install the Airdot Deployer package using pip:

```bash
pip install "git+https://github.com/airdot-io/airdot-deployer.git@main#egg=airdot"
```

## or

```bash
pip install airdot
```

## 🎯 Let's try out

### Local Deployments

#### Run following in terminal to setup minio and redis on your machine

```bash
docker network create minio-network && wget  https://raw.githubusercontent.com/airdot-io/airdot-deployer/main/docker-compose.yaml && docker-compose -p airdot up
```

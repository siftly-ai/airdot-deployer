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

### Setting up minio and redis on local machine

Since for local setup airdot requires a test bucket we uses local minio for object storage and redis for storing metadata for user ML microservice to setup both you only need to run following command in terminal.

```bash
docker network create minio-network && wget  https://raw.githubusercontent.com/airdot-io/airdot-deployer/main/docker-compose.yaml && docker-compose -p airdot up
```

## 📋 Local setup (basic without cluster)

This setup is for users who want's to test how airdot helps in accelerating seldon-core deployment. The initial setup is similar to previous setup. 

### Docker Install
Please visit the appropriate links to install Docker on your machine:
- For macOS, visit [here](https://docs.docker.com/desktop/install/mac-install/)
- For Windows, visit [here](https://docs.docker.com/desktop/install/windows-install/)
- For Linux, visit [here](https://docs.docker.com/desktop/install/linux-install/)

### Install Airdot python package

```bash
pip install airdot
```

### Setting up minio and redis on local machine

Since for local setup airdot requires a test bucket we uses local minio for object storage and redis for storing metadata for user ML microservice to setup both you only need to run following command in terminal.

```bash
docker network create minio-network && wget  https://raw.githubusercontent.com/airdot-io/airdot-deployer/main/docker-compose.yaml && docker-compose -p airdot up
```

### S2I install

Airdot uses s2i for building seldon-core images using seldon-core builder images on top of your own ML microservice base image
For Mac
You can either follow the installation instructions for Linux (and use the darwin-amd64 link) or you can just install source-to-image with Homebrew:

```$ brew install source-to-image```

For Linux just run following command

```bash
curl -s https://api.github.com/repos/openshift/source-to-image/releases/latest| grep browser_download_url | grep linux-amd64 | cut -d '"' -f 4  | wget -qi -
```

For Windows please follow instruction [here](https://github.com/openshift/source-to-image#for-windows)

### Setting up seldon-core using kind cluster

One of the simple way of setting up seldon-core on local machine is to first setup a local custer using kind and then install seldon-core on top of it. Seldon-core has a very detailed blog of setting up seldon-core using kind please click [here](https://docs.seldon.io/projects/seldon-core/en/latest/install/kind.html)


### Checking installation

You can check if every thing went fine by just running few commands mentioned below.

To check if you are connected to local cluster
```bash
kubectl get nodes
```
You should get similar output Note - version might be different
```bash
NAME                   STATUS   ROLES           AGE   VERSION
seldon-control-plane   Ready    control-plane   58d   v1.27.3
```


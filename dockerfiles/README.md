# How to use dockerfile

## Build image

```bash
docker build -t <image_name> .
```

## Publish image

```bash
docker tag <image_name> <dockerhub_username>/<image_name>:<tag>
docker push <dockerhub_username>/<image_name>:<tag>
```

## Run container

```bash
docker run --ipc=host --gpus all -dt --name container-name <image_name>
```

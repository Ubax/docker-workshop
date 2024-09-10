# Inspecting the layers of the image

In this task, we will explore how to inspect the layers of a Docker image.

## Inspecting an image

Let's start by building simple image from `Dockerfile.one-layer`.

```sh
docker build -f Dockerfile.one-layer -t one-layer .
```

To view the details of the image, we can use the `docker image inspect` command:

```sh
docker image inspect one-layer > one-layer.json
```

Open the `one-layer.json` file, and you should see output similar to the following:

```json
[
    {
        "Id": "sha256:1c92092c8b88bff19e8dd2bb4a0d1bf335c93872ae5d4e97740fa46ea182b767",
        "RepoTags": [
            "single-layer:latest"
        ],
        "RepoDigests": [],
        "Parent": "",
        "Comment": "buildkit.dockerfile.v0",
        "Created": "2024-09-10T06:59:15.773294679Z",
        "ContainerConfig": { ...},
        "DockerVersion": "",
        "Author": "",
        "Config": { ... },
        "Architecture": "arm64",
        "Variant": "v8",
        "Os": "linux",
        "Size": 8825175,
        "GraphDriver": { ... },
        "RootFS": { ...},
        "Metadata": { ... },
        "Container": ""
    }
]
```

The fields we're particularly interested in are `RootFS` and `GraphDriver`:

- `RootFS` contains the SHA-256 hashes of the image's layers.
- `GraphDriver` shows the storage driver (e.g., `overlay2`) being used, along with the paths where the layers are stored.

## Inspecting layers

Next, build the other images and inspect them as well:

```sh
docker build -f Dockerfile.two-layers -t two-layers .
docker build -f Dockerfile.update -t update .
docker build -f Dockerfile.expose -t expose .
docker image inspect two-layers > two-layers.json
docker image inspect update > update.json
docker image inspect expose > expose.json
```

Now you can compare the images and their layers by looking at the SHA-256 hashes in each file.

### Expose

When comparing `expose.json` with `update.json`, you'll notice that both images have the same layers. This happens because the `EXPOSE` instruction in Docker does not create a new layer; it only adds metadata to the image. Therefore, adding the `EXPOSE` instruction won't affect Docker's cache.

## Image filesystem

If you're curious about where the layers are stored on disk, you can refer to the GraphDriver section in the update.json file. It will look something like this (though the paths may vary):

```json
...
"GraphDriver": {
    "Data": {
        "LowerDir": "/var/lib/docker/overlay2/xhryuf3omugv3asu7nmw6x65l/diff:/var/lib/docker/overlay2/qv003371z5bmlyx78mpuaw2yp/diff:/var/lib/docker/overlay2/96zixqmlpnlfo55q0l9umulq9/diff:/var/lib/docker/overlay2/1e69d1d5b61a6852c2cf0c24688f5f1e6adbd464b31db6dd8bfc561f55dde358/diff",
        ...
    },
    "Name": "overlay2"
}
...
```

This shows that Docker is using the `overlay2` storage driver, which efficiently manages the image's filesystem by stacking layers on top of each other. The `LowerDir` lists the multiple directories, each corresponding to a layer of the image. These layers are stacked on top of each other to form the final filesystem.

### Inspecting files

<details>
<summary>Mac and windows</summary>

To access `/var/lib/docker` on macOS or Windows, you'll need to enter the VM's file system using the following command:

```sh
docker run -it --rm -v /var/lib/docker:/var/lib/docker alpine sh
```
</details>

You can now explore the files for each layer. First, navigate to the rightmost `LowerDir`, which corresponds to the base image (in this case, `alpine`):

```sh
cd /var/lib/docker/overlay2/1e69d1d5b61a6852c2cf0c24688f5f1e6adbd464b31db6dd8bfc561f55dde358/diff # remember to use the path from your json file
ls
```

Next, move to the second directory to see the contents of another layer:

```sh
cd /var/lib/docker/overlay2/96zixqmlpnlfo55q0l9umulq9/diff # remember to use the path from your json file
ls
```

You should see something like this:
```
etc         index.html
```

Opening `index.html` will show you the content added by the first layer (`RUN echo "First layer" > /index.html`):

```sh
cat index.html
#### Should produce: First layer
```

## Inspecting container layers

You can also inspect the layers of the container. First run the container and create a file inside:

```sh
docker run -it update sh # update is the name of the image
> echo "Inside" > /inside.txt
> exit
```

Next, retrieve the container ID:
```sh
docker ps -a
```

Inspect the container by running:
```sh
docker inspect [container_id] > container.json
```

In `container.json`, the `GraphDriver` field will show that the container is using the same image layers but has an additional writable layer on top. To see the changes, navigate to the path specified in the `UpperDir`:
```sh
cd [UpperDir] # remember to use the path from your json file
ls
```

You should see:
```
inside.txt  root
```
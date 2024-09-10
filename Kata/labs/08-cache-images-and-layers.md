# Cache - Images and layers

When dealing with docker images, a layer, or image layer, is a change on an image. Every time you run one of the commands RUN, COPY or ADD in your Dockerfile it adds a new layer, causes the image to change to the new layer. You can think of it as staging changes when you're using Git: You add a file's change, then another one, then another one...

Consider the following Dockerfile:

```dockerfile
  FROM ubuntu:22.04
  RUN apt-get update -y
  RUN apt-get install -y python3 python3-pip python3-dev build-essential
  COPY requirements.txt /usr/src/app/
  RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
  COPY app.py /usr/src/app/
  EXPOSE 5000
  CMD ["python3", "/usr/src/app/app.py"]
```

First, we choose a starting image: `ubuntu:22.04`, which in turn has many layers.
We add another layer on top of our starting image, running an update on the system. After that yet another for installing the python ecosystem.
Then, we tell docker to copy the requirements to the container. That's another layer.

The concept of layers comes in handy at the time of building images. Because layers are intermediate images, if you make a change to your Dockerfile, docker will build only the layer that was changed and the ones after that. This is called layer caching.

Each layer is build on top of it's parent layer, meaning if the parent layer changes, the next layer does as well.

If you want to concatenate two layers (e.g. the update and install [which is a good idea](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#run)), then do them in the same RUN command:

```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
 python3 \
 python3-pip \
 python3-dev \
 build-essential
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
COPY app.py /usr/src/app/
EXPOSE 5000
CMD ["python3", "/usr/src/app/app.py"]
```

If you want to be able to use any cached layers from last time, they need to be run _before the update command_.

> NOTE:
> Once we build the layers, Docker will reuse them for new builds. This makes the builds much faster. This is great for continuous integration, where we want to build an image at the end of each successful build (e.g. in Jenkins). But the build is not only faster, the new image layers are also smaller, since intermediate images are shared between images.

Try to move the two `COPY` commands before for the `RUN` and build again to see it taking the cached layers instead of making new ones.

## More information

If you want to learn more about how docker layers are stored and cached you can go to [layers](../../Advanced/layers/Readme.md) task in the [Advanced](../../Advanced/) section.

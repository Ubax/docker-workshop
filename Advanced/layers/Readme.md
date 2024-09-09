# Inspecting the layers of the image

In this task we will inspect the layers of the image.

Let's start by building simple image with a Dockerfile.

```sh
docker build -t simple-file .
```

Now we need to inspect the image

```sh
docker image inspect simple-file > simple-file.json
```

Now go to `sipmle-file.json`.


If you are on mac or windows you need to enter the VM's file system to inspect the layers of the image.

```sh
docker run -it --rm -v /var/lib/docker:/var/lib/docker alpine sh
```


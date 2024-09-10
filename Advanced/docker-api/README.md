# Docker API

Reference: [Docker Engine API](https://docs.docker.com/reference/api/engine/)

## Calling API using curl

To call the Docker API you need to connect to docker socket. You can do it using following command:

```sh
curl --unix-socket /var/run/docker.sock [Docker URL]
```

For example, to get the list of containers:

```sh
curl --unix-socket /var/run/docker.sock http:/v1.47/containers/json
```

## Using Docker API in code

To connect to Docker API in code, there are libraries available for different languages. Here are some of them:
- NodeJs: [dockerode](https://github.com/apocas/dockerode)
- Python: [docker-py](https://github.com/docker/docker-py)
- Java: [docker-java](https://github.com/docker-java/docker-java)

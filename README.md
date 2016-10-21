# kubernetes-rabbitmq-petset

A RabbitMQ cluster for Kubernetes based on PetSet

To run the cluster, first build an image and push it to a registry:

```
docker build -t 127.0.0.1:31500/rabbitmq-clustered:latest .
docker push 127.0.0.1:31500/rabbitmq-clustered:latest
```

After that you can start the pet set:

```
kubectl create -f rabbitmq-cluster.yaml
```

Don't forget to adjust the registry url in the yaml file.

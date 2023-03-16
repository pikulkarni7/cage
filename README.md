# cage - celery service for birdy



**Publisher:** A separate RabbitMQ queue producer is declared and added to Celery's default producer_pool, which is pulled and used to publish new messages to that queue in a Celery task.

**Consumer:** A custom consumer class is defined and attached to Celery. The class is subscribed to the custom queue that is created/declared with the separate queue producer above. A handle_message callback function is defined in the custom consumer class so that every time a message is published to that particular queue, the consumer's callback is called, which consumes the message and sends an ack to RabbitMQ.


### Installation
`docker` and `docker-compose` are needed to be installed to run this project. These links can be followed to install both on Ubuntu:
- `docker`: https://docs.docker.com/install/linux/docker-ce/ubuntu/
- `docker-compose`: https://docs.docker.com/compose/install/

After installation, run:
```shell
docker-compose build
docker-compose up
```



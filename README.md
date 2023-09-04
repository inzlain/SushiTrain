# Sushi Train
Sushi Train is a payload management and delivery framework that was built to support use cases not easily handled by traditional phishing and C2 frameworks. Sushi Train focuses on providing a simple and highly usable interface for red team operators to manage and deliver their payloads in a controlled and safe way.

At it's core, Sushi Train is simply a way to handle incoming HTTP requests to your redirectors, and conditionally serve a response based on a policy system. This includes serving static files, dynamically created payloads using a modular payload system, and the ability to passthrough requests to other servers (i.e. proxy C2 traffic). You can use Sushi Train to deliver phishing payloads, implant stagers, tracking images, or anything else where you require a high level of control.

The [Sushi Train documentation](https://inzlain.gitbook.io/sushi-train) tells you more about Sushi Train and how to get started with deployment and usage.  If you are not sure if this is the right tool for you then have a read of [Is Sushi Train What I Am Looking For?](https://inzlain.gitbook.io/sushi-train/overview/is-sushi-train-what-i-am-looking-for)

## Quick Start Instructions
 1. Configure the `DELIVERY_HOSTNAME` and `MANAGEMENT_HOSTNAME` values in the `.env` file
 2. Deploy and start using Docker Compose via `docker compose up --detach`

Refer to the [deployment documentation](https://inzlain.gitbook.io/sushi-train/deployment/installation) for more detailed information.

## Development Status
Sushi Train is still in development and should be considered alpha software heading towards an eventual initial stable release. You should expect the occasional bug, missing functionality, and ongoing changes to how functionality works.
from clenv.cli.queue.queue_manager import QueueManager
from clearml.backend_api.session.client import APIClient

if __name__ == "__main__":
    manager = QueueManager()

    print(manager.get_available_queues())

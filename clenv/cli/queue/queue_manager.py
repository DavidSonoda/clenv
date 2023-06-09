from clearml.backend_api.session.client import APIClient
from clenv.cli.config.config_loader import ConfigLoader
import requests


# Write a subcommand about the queue management
class QueueManager:
    GET_ALL_EX = "queues.get_all_ex"

    def __init__(self):
        self.__client = APIClient(api_version="2.23")

        # Initialize an http client using requests
        self.__http_client = requests.Session()
        self.__config_loader = ConfigLoader(config_file_path="~/clearml.conf")
        self.__config_loader.load()

    def __refresh_token(self):
        resp = self.__client.auth.login()
        self.__token = resp.token

    def __get_all_queues(self):
        self.__refresh_token()
        api_server_addr = self.__config_loader.get_config_value("api.api_server")
        # Get JSON response from the API using the http client, the API url is /queues.get_all_ex
        # Also, pass the token in the header
        resp = self.__http_client.get(
            f"{api_server_addr}/{self.GET_ALL_EX}",
            headers={"Authorization": "Bearer " + self.__token},
        )

        # Get the queues from the response
        return resp.json().get("data").get("queues")

    def __get_queue_simple_details_by_id(self, queue_id):
        queue = self.__client.queues.get_by_id(queue_id)
        # Convert queue to a dict object
        return queue

    def get_all_queue_names(self):
        # Iterate queues, get the queue names
        queues = self.__get_all_queues()
        queue_names = [queue.name for queue in queues]
        return queue_names

    def get_queue_simple_details(self, queue_name, queue_id=None):
        queues = self.__get_all_queues()
        for queue in queues:
            if queue.name == queue_name or queue.id == queue_id:
                return self.__get_queue_simple_details_by_id(queue.id)

    def get_available_queues(self):
        queues = self.__get_all_queues()
        # Filter out the queues that are not available, which means the queue.workers is an not an empty list
        return [queue for queue in queues if queue["workers"]]

    # def list_queues_as_table(self):
    # queue_detail_list = self.list_queues()

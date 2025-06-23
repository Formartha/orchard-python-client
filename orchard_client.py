import requests
import os
import json
import yaml
from requests.auth import HTTPBasicAuth


class OrchardClient:

    def __init__(self, base_url, user, password):
        """
        Initialize the OrchardClient.

        :param base_url: The base URL of the Orchard API.
        :param user: Username for authentication.
        :param password: Password for authentication.
        """
        self.base_url = f"{base_url}/v1"
        self.headers = {"Content-Type": "application/json"}
        self.auth = HTTPBasicAuth(user, password)

    def _parse_data(self, data):
        """
        Parses input data to a Python dictionary.
        Supports dict, JSON string, YAML string, or file path (.json/.yaml/.yml).

        :param data: dict, JSON/YAML string, or filename.
        :return: Parsed dictionary.
        """
        if isinstance(data, dict):
            return data

        if isinstance(data, str):
            # Check if it's a file
            if os.path.isfile(data):
                with open(data, 'r') as f:
                    if data.endswith(('.yaml', '.yml')):
                        return yaml.safe_load(f)
                    elif data.endswith('.json'):
                        return json.load(f)
                    else:
                        raise ValueError("Unsupported file extension. Use .json or .yaml/.yml")
            else:
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    try:
                        return yaml.safe_load(data)
                    except yaml.YAMLError:
                        raise ValueError("Invalid JSON or YAML string.")

        raise TypeError("Unsupported input type for data. Provide dict, JSON/YAML string, or path to a file.")


    def _request(self, method, endpoint, params=None, json=None):
        """
        Send an HTTP request.

        :param method: HTTP method (GET, POST, etc).
        :param endpoint: API endpoint to hit.
        :param params: URL parameters.
        :param json: JSON body.
        :return: Parsed JSON response or None.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, auth=self.auth, params=params, json=json, verify=False)
        response.raise_for_status()
        return response.json() if response.content else None

    def get_controller_info(self):
        """Get controller information."""
        return self._request("GET", "/controller/info")

    def get_cluster_settings(self):
        """Retrieve current cluster settings."""
        return self._request("GET", "/cluster-settings")

    def update_cluster_settings(self, settings):
        """Update cluster settings.

        :param settings: Dictionary of settings to update.
        """
        return self._request("PUT", "/cluster-settings", json=settings)

    def create_service_account(self, data):
        """Create a new service account.

        :param data: Service account data.
        """
        return self._request("POST", "/service-accounts", json=data)

    def list_service_accounts(self):
        """List all service accounts."""
        return self._request("GET", "/service-accounts")

    def get_service_account(self, name):
        """Retrieve a specific service account.

        :param name: Name of the service account.
        """
        return self._request("GET", f"/service-accounts/{name}")

    def update_service_account(self, name, data):
        """Update a service account.

        :param name: Name of the service account.
        :param data: Updated data.
        """
        return self._request("PUT", f"/service-accounts/{name}", json=data)

    def delete_service_account(self, name):
        """Delete a service account.

        :param name: Name of the service account.
        """
        self._request("DELETE", f"/service-accounts/{name}")

    def create_worker(self, data):
        """Create a new worker.

        :param data: Worker data.
        """
        return self._request("POST", "/workers", json=data)

    def list_workers(self):
        """List all workers."""
        return self._request("GET", "/workers")

    def get_worker(self, name):
        """Get details of a worker.

        :param name: Name of the worker.
        """
        return self._request("GET", f"/workers/{name}")

    def update_worker(self, name, data):
        """Update worker configuration.

        :param name: Name of the worker.
        :param data: New configuration.
        """
        return self._request("PUT", f"/workers/{name}", json=data)

    def delete_worker(self, name):
        """Delete a worker.

        :param name: Name of the worker.
        """
        self._request("DELETE", f"/workers/{name}")

    def create_vm(self, data):
        """Create a new virtual machine.

        :param data: VM configuration.
        """
        payload = self._parse_data(data)
        return self._request("POST", "/vms", json=payload)

    def list_vms(self):
        """List all virtual machines."""
        return self._request("GET", "/vms")

    def get_vm(self, name):
        """Retrieve VM details.

        :param name: Name of the VM.
        """
        return self._request("GET", f"/vms/{name}")

    def update_vm(self, name, data):
        """Update a VM's configuration.

        :param name: Name of the VM.
        :param data: Updated configuration.
        """
        return self._request("PUT", f"/vms/{name}", json=data)

    def delete_vm(self, name):
        """Delete a virtual machine.

        :param name: Name of the VM.
        """
        self._request("DELETE", f"/vms/{name}")

    def get_vm_events(self, name):
        """Get events related to a VM.

        :param name: Name of the VM.
        """
        return self._request("GET", f"/vms/{name}/events")

    def add_vm_events(self, name, events):
        """Add events to a VM.

        :param name: Name of the VM.
        :param events: Dictionary of events to add.
        """
        return self._request("POST", f"/vms/{name}/events", json=events)

    def resolve_vm_ip(self, name, wait=15):
        """Resolve a VM's IP address, optionally waiting for it.

        :param name: Name of the VM.
        :param wait: Time to wait for the IP (in seconds).
        """
        return self._request("GET", f"/vms/{name}/ip", params={"wait": wait})

    def create_vm_and_return_ip(self, data, retries=10, wait=15):
        """Create a VM and return its IP address.

        :param data: VM configuration.
        :param retries: Number of retries.
        :param wait: Cooldown between retries in seconds.
        """
        counter = 0
        name = self.create_vm(data)["name"]

        while counter <= retries:
            try:
                return {"ip": self.resolve_vm_ip(name, wait)["ip"], "name": name}
            except:
                counter += 1
        raise Exception("Failed to create VM")
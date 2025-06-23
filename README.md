<img src=".readme/orchard-python-client.png" alt="cover" width="220">

A lightweight Python client for interacting with the **Orchard Orchestration API**.  
Supports full CRUD operations for service accounts, workers, and virtual machines — with payloads in either **JSON** or **YAML** format.

---

## Installation

```bash 
pip install git+https://github.com/your-username/orchard-client.git
```

Or clone and install locally:

```bash
git clone https://github.com/your-username/orchard-client.git
cd orchard-client
pip install .
```

---

## Requirements

- Python 3.x
- `requests`
- `PyYAML`

These are automatically installed via `setup.py`.

---

## Features

- HTTP Basic Auth support
- Built-in methods for:
  - Service Accounts
  - Workers
  - Virtual Machines
  - Cluster Settings
  - Controller Info
- Accepts payloads as:
  - Python `dict`
  - `.json` or `.yaml` file
  - Raw JSON/YAML strings

---

## Usage

```python
from orchard_client import OrchardClient

client = OrchardClient(
    base_url="https://orchard.local:6120",
    user="admin",
    password="secret"
)

# Create VM from a YAML file
vm_info = client.create_vm_and_return_ip("vm_config.yaml")
print(vm_info)

# Get all workers
workers = client.list_workers()
print(workers)
```

---

## Supported Methods

### VMs
- `create_vm(data)`
- `list_vms()`
- `get_vm(name)`
- `update_vm(name, data)`
- `delete_vm(name)`
- `resolve_vm_ip(name, wait=15)`
- `create_vm_and_return_ip(data, retries=10, wait=15)`

### Workers
- `create_worker(data)`
- `list_workers()`
- `get_worker(name)`
- `update_worker(name, data)`
- `delete_worker(name)`

### Service Accounts
- `create_service_account(data)`
- `list_service_accounts()`
- `get_service_account(name)`
- `update_service_account(name, data)`
- `delete_service_account(name)`

### Cluster & Controller
- `get_controller_info()`
- `get_cluster_settings()`
- `update_cluster_settings(settings)`

---

## Example VM Config (YAML)

```yaml
name: "test-vm"
cpu: 2
memory: 4096
disk: 20
os: "ghcr.io/cirruslabs/macos-monterey-base:latest"
network:
  bridge: "orchard-net"
```

---

## License

[MIT](LICENSE)

---

## Author

**Mor Dabastany**  
📧 morpci@gmail.com

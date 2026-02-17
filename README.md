# QA Test Task

**The project is using Vagrant for the VM, Ansible for managing the VM, and Locust for testing.**

## Why were these tools chosen?

Vagrant:
* Easy to use
* No need for an extra IaC tool like Terraform
* Fast deployment

Ansible:
* One of the most popular tools
* Good documentation with lots of examples
* No need to deploy anything on the managed machine to manage it
* Easier to use than Salt

Locust:
* Written in Python, which is good because libvirt also has a Python library
* Easy to use
* It has a web UI and a command-line headless mode

> [!NOTE]
> Alternative option for testing what I would try out: Grafana k6

### Extra tools

Simple API:
* It is simple
* It has a Docker image
* No need to write your own API

## Manual or semi-automated steps

### Preparation

> [!NOTE]
> The following versions were used for development:
> OS: Ubuntu 24.04 LTS
> Vagrant: 2.4.9
> Ansible core: 2.20.2

#### Example how to install vagrant with libvirt

```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y vagrant

sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager nfs-common nfs-kernel-server

sudo adduser $USER libvirt

sudo apt install -y libvirt-dev ebtables libguestfs-tools ruby-fog-libvirt

vagrant plugin install vagrant-libvirt
```

> [!NOTE]
> It is possible that you should restart the OS to make vagrant and libvirt work.

#### Example how to install ansible

```bash
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible
```

### Example how to install Locust

> [!NOTE]
> An open source load testing tool.
> URL: https://locust.io/

```bash
sudo apt install python3-locust
```

### Clone the project

```bash
git clone https://github.com/norbertszivos/qa_test_task.git
```

### Start vagrant

```bash
cd qa_test_task/vm
vagrant up
```

### Install Simple API for testing

> [!NOTE]
> A simple REST API with Redis database built with Spring boot to learn Docker and Kubernetes.
> URL: https://hub.docker.com/r/jkaninda/simple-api

```bash
cd ../ansible
ansible-playbook -i inventory playbooks/load_test_system/main.yml
```

### Run tests

```bash
cd ../test
```

#### Using Locust web UI

```bash
locust
```

> [!NOTE]
> Open a browser and visit the website below.
> URL: http://localhost:8089
> Set the number of users, the spawn rate, and the host, then click on the start swarm button.

#### Using Locust headless mode

```bash
locust --headless --host http://localhost:8080 --users 100 --spawn-rate 10 --run-time 60

...

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /                                                                                188     0(0.00%) |     11       1      44      3 |    3.14        0.00
GET      /books                                                                           568     0(0.00%) |     28       8      80     28 |    9.48        0.00
POST     /books                                                                           391     0(0.00%) |     13       1      52      7 |    6.52        0.00
GET      /books/64f87e8c-3ecd-4411-978d-8f6381fa1c58                                      540     3(0.56%) |     10       0      55      4 |    9.01        0.05
PUT      /books/64f87e8c-3ecd-4411-978d-8f6381fa1c58                                      191     2(1.05%) |     13       1      49      7 |    3.19        0.03
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                      1878     5(0.27%) |     16       0      80     12 |   31.33        0.08

Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /                                                                                       3     12     18     21     41     42     43     44     44     44     44    188
GET      /books                                                                                 28     32     34     36     40     46     64     70     80     80     80    568
POST     /books                                                                                  7     12     18     23     40     43     45     47     52     52     52    391
GET      /books/64f87e8c-3ecd-4411-978d-8f6381fa1c58                                             4      7     14     18     30     42     43     45     55     55     55    540
PUT      /books/64f87e8c-3ecd-4411-978d-8f6381fa1c58                                             7     11     16     20     42     43     47     48     49     49     49    191
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                                             12     22     28     31     39     43     46     54     77     80     80   1878

Error report
# occurrences      Error
------------------|---------------------------------------------------------------------------------------------------------------------------------------------
3                  GET /books/64f87e8c-3ecd-4411-978d-8f6381fa1c58: BadStatusCode('http://localhost:8080/books/64f87e8c-3ecd-4411-978d-8f6381fa1c58', code=404)
2                  PUT /books/64f87e8c-3ecd-4411-978d-8f6381fa1c58: BadStatusCode('http://localhost:8080/books/64f87e8c-3ecd-4411-978d-8f6381fa1c58', code=404)
------------------|---------------------------------------------------------------------------------------------------------------------------------------------
```

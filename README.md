# QA Test Task

## Manual or semi-automated steps

### Preparation

> [!NOTE]
> OS: Ubuntu 24.04 LTS
> Vagrant: 2.4.9
> Ansible core: 2.20.2

**The project is using vagrant and ansible.**

#### Example how to install vagrant with libvirt

```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y vagrant

sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager

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

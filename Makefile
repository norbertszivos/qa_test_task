all: vagrant_plugin_install vagrant_up ansible_deploy locust_run_test

rebuild: vagrant_destroy vagrant_up ansible_deploy


# =============================================================================
# Prepare the machime.
# Install all application what we will need.
# !!! These recipes should run with sudo !!!
# =============================================================================

prepare: prepare_vagrant prepare_ansible prepare_locust

prepare_vagrant:
ifeq ("$(wildcard /usr/share/keyrings/hashicorp-archive-keyring.gpg)","")
	wget -O - https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
	echo "deb [arch=$(shell dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(shell grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
endif
	apt update && apt install -y vagrant
	apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager nfs-common nfs-kernel-server
	adduser ${USER} libvirt
	apt install -y libvirt-dev ebtables libguestfs-tools ruby-fog-libvirt

prepare_ansible:
	apt install software-properties-common
	add-apt-repository --yes --update ppa:ansible/ansible
	apt install -y ansible

prepare_locust:
	apt install -y python3-locust


# =============================================================================
# Manage the VM
# =============================================================================

vagrant_plugin_install:
	vagrant plugin install vagrant-libvirt

vagrant_up:
	cd vm && vagrant up

vagrant_ssh:
	cd vm && vagrant ssh

vagrant_destroy:
	cd vm && vagrant destroy


# =============================================================================
# Deploy the VM
# =============================================================================

ansible_deploy:
	cd ansible && ansible-playbook -i inventory playbooks/load_test_system/main.yml


# =============================================================================
# Run test
# =============================================================================

locust_run_test:
	cd test && locust --headless --host http://10.80.0.100:8080 --users 100 --spawn-rate 10 --run-time 60 --csv=stats/results

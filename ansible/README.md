# Ansible

Ansible is open-source technology that can perform virtually any IT task and remove complexity from workflows.


## Homepage

[https://docs.ansible.com](https://docs.ansible.com)

[https://docs.ansible.com/projects/ansible/latest](https://docs.ansible.com/projects/ansible/latest)


## Common commands

Deploy the VM:

```bash
ansible-playbook -i inventory playbooks/load_test_system/main.yml
```

Run only `apt update` in the VM:

```bash
ansible-playbook -i inventory playbooks/load_test_system/main.yml --tags vagrant_apt_update
```

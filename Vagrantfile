Python_install = <<EOF
sudo apt-get update
sudo apt-get install -y python-minimal
EOF

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 15672, host: 25672
  config.vm.provision :shell, inline: Python_install
  config.vm.provision :ansible,
    playbook: "playbooks/main.yml",
    sudo: true,
    verbose: "vv",
    raw_arguments: ["--diff"],
    extra_vars: { local_repository: "/vagrant" }
end

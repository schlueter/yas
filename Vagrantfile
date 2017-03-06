Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 15672, host: 25672
  ansible_extra_vars = {}
  ansible_extra_vars['local_repository'] = '/vagrant'
  ansible_extra_vars['log_level'] = ENV['LOG_LEVEL'] || 'INFO'

  if ENV.has_key? 'SLACK_APP_TOKEN'
    ansible_extra_vars['slack_app_token'] = ENV['SLACK_APP_TOKEN']
  end

  config.vm.provision :ansible,
    playbook: "playbooks/main.yml",
    sudo: true,
    verbose: "vv",
    raw_arguments: ["--diff"],
    extra_vars: ansible_extra_vars
end

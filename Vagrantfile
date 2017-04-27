Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 15672, host: 25672
  config.vm.synced_folder "../YasOpenStack", "/srv/YasOpenStack"
  config.vm.synced_folder "../YasExampleHandlers", "/srv/YasExampleHandlers"
  ansible_extra_vars = {}
  ansible_extra_vars['local_repository'] = '/vagrant'
  ansible_extra_vars['log_level'] = ENV['LOG_LEVEL'] || 'DEBUG'

  if ENV.has_key? 'SLACK_APP_TOKEN'
    ansible_extra_vars['slack_app_token'] = ENV['SLACK_APP_TOKEN']
  end

  if ENV.has_key? 'SLACK_APP_NAME'
    ansible_extra_vars['slack_app_name'] = ENV['SLACK_APP_NAME']
  end

  config.vm.provision :ansible,
    playbook: "playbooks/main.yml",
    sudo: true,
    verbose: "vv",
    raw_arguments: ["--diff"],
    extra_vars: ansible_extra_vars
end

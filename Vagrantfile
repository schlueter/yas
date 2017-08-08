Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/xenial64'

  %w(YasOpenStack YasExampleHandlers).each do |repo|
    local_path = '../' + repo
    remote_path = '/srv/' + repo
    if Dir.exists?(local_path)
      config.vm.synced_folder(local_path, remote_path)
    end
  end

  config.vm.provision :ansible,
    playbook: 'playbooks/main.yml',
    raw_arguments: %w(--diff -vv --become),
    groups: { yas: %w(default)},
    extra_vars: { local_repository: '/vagrant',
                  yas_repo_update: false }
end

# YAS
##### Yet Another Slackbot
A modular Slack bot framework.

## Deploying

Yas can be deployed with Ansible by using a custom hosts file and extra_vars. In order to include the extra_vars in a vcs, they may be stored in a json formatted file.

The hosts file must minimally include the target host of yas in a *yas* group:

    [yas]
    mybothost.mydomain.com

To deploy a functioning bot, the extra_vars must include a *slack_app_token* and a *bot_name* which may be created at https://my.slack.com/services/new/bot.

Additional variables are also available; this is an exhaustive example set of extra_vars:

    {
     "__comment": "See http://github.com/refinery29/yas/README.md#deploying for usage",
     "yas_repo": "https://github.com/refinery29/yas.git",
     "yas_repo_version": "feature-branch-or-tag",
     "slack_app_token": "xoxb-201647080420-go-make-one",
     "bot_name": "yas-tester",
     "log_level": "INFO",
     "handler_exception_message": "Womp, I caught an error on that:\n&gt;{exception}",
     "handler_packages": [
      "git+https://github.com/refinery29/YasOpenstack.git"
     ],
     "additional_handlers": [
      "yas_openstack.handler."
     ],
     "handler_config_templates": {
       "default-userdata.sh": "{{ inventory_dir }}/templates/instance-init.sh"
     },
     "handler_configs": [
      {
       "name": "openstack.yml",
       "content": {
        "__comment": "The contents will be output as pretty printed yaml to a file with the specified name in the yas config directory",
       }
      }
     ]
    }

With those two files in place the playbook in this repo may be invoked with the following to apply it to the target machine:

    ansible-playbook --inventory /path/to/hosts /path/to/yas/playbooks/main.yml --extra-vars "$(</path/to/yas-extra-vars.json)"

*Note that yas, and the yas playbooks use systemd for process management and logging. They have both been built against Ubuntu Xenial.


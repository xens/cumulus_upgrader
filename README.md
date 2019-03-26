#### Intro

Doing upgrades on lots of whitebox network boxes takes time and is prone to
errors, there's a lot of things to check and make sure of to avoid impacting
the data-plane.

This collection of Ansible playbooks tries to automate this process for a network
fabric composed of whitebox switches running Cumulus linux. The whole process is
based around ensuring that the infrastructure is consistent before and after an
upgrade and to make sure that it doesn't impact the dataplane during the operation.
It uses `apt` to do the packages upgrades, it doesn't support binary-images upgrades
(yet).

It supports both switches doing L2 and or L3.

#### Warning

These playbooks have been validated multiple time in production under a specific
setup:

  * Everything redundant top to bottom
  * Switches doing L2+L3
  * All Switches running CL >=3.4 with FRR

Depending on your setup you might want to add checks that are specific to your
infrastructure. Read the code before running it.

#### How it works

All the switches that you want to upgrade must be referenced inside the `hosts`
file. You can then run the `upgrade_fabric.yml` playbook using Ansible (>=2.5).
The playbook will go through a bunch of tests (OS version, BGP, MLAG) before
starting the upgrade (swuitch by switch), it'll also pause before upgrading the
each switch and ask your validation. If something goes wrong during this process,
like one switch not rebooting, or one test failing, the process will stop and
you'll need to manually investigate the issue before continuing the process.

#### Future work

* Add proper support for oob-switches upgrades (early playbook included in this
  repo).
* Support for binary-images upgrades

PR's welcome !

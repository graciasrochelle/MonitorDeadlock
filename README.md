# MonitorDeadlock
Monitor deadlock and send notification to slack. SLACK API: https://github.com/slackapi/python-slack-sdk

Commands:

`docker build . -t deadlock_monitor`

`docker run -it --rm --name deadlock_monitor --pid=container:deadlockapp deadlock_monitor`

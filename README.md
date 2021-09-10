Change afuploader.service so that ExecStart, WorkingDirectory and User reflect your setup

run ./service-install.sh to copy the service to systemd and enable it on startup
run ./service-uninstall.sh to remove the service and disable it

---

The service runs as root, which means all the log files and directories that are created are owned by root. The service will start by running qos-enable.sh which sets some caps on local and outbound traffic. Change the file so that it reflects your setup.

You can check that the bandwidth is limited by running a server on another machine (let's call it 10.0.2.2):
```
iperf3 -s -p 8080
```

Then run the following command on the bandwidth limited client, assuming the previous ip
```
iperf3 -c 10.0.2.2 -p 8080 -t 30
```

---

Follow the log and
create a few files to upload
```
tail -f ./log/autofill-upload.log
touch ./upload/test1.dat
touch ./upload/test2.dat
```

The uploader gets a notification when a file is created in the upload directory and adds it to an asynchronous queue. If there are files in the directory when the script starts they will be added first.

The main thread processed the async queue and (placeholder) uploads the file. No more than one file is uploaded at a time. After the upload completes the file is deleted and the next file in the queue will be uploaded.

The service uses a rotating log. Set the maximum log file size to a higher value than it is set for testing.

If the log or upload dir does not exist at startup, it will create them



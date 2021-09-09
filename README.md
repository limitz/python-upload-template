Change afuploader.service so that ExecStart, WorkingDirectory and User reflect your setup

run ./install.sh to copy the service to systemd and enable it on startup
run ./uninstall.sh to remove the service and disable it

follow the log
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



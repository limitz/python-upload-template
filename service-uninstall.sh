sudo systemctl stop afuploader
sudo systemctl disable afuploader
sudo rm /etc/systemd/system/afuploader.service
sudo ./qos-disable.sh

Here are our network config files (passwords are *******):

```console
photonvision@photonvision:/etc/systemd/system$ cat /etc/systemd/system/cadmia.service
[Unit]
Description=Cadmia
After=multi-user.target

[Service]
Type=idle
Restart=always

ExecStart=/home/photonvision/cadmia/start.sh
Environment="CADMIA_PATH=/home/photonvision/cadmia"

[Install]
WantedBy=multi-user.target
photonvision@photonvision:/etc/systemd/system$ sudo cat /etc/netplan/00-installer-config-wifi.yaml 
# This is the network config written by 'subiquity'
network:
  version: 2
  wifis:
    wlp1s0:
      access-points:
        STEM-Gym:
          password: *******
      dhcp4: true
photonvision@photonvision:/etc/systemd/system$ sudo cat /etc/netplan/00-installer-config.yaml 
# This is the network config written by 'subiquity'
network:
  version: 2
  renderer: networkd
  ethernets:
    enp2s0:
      dhcp4: no
      dhcp6: no
      addresses: [10.23.63.11/24]
      gateway4: 10.10.10.1
photonvision@photonvision:/etc/systemd/system$
```

Some error fixes:

bluetooth error:
sudo hciconfig hci0 piscan

bluez error:
1. Edit /etc/systemd/system/dbus-org.bluez.service and add '-C' after 'bluetoothd'.
2. Reboot.
3. sudo sdptool add SP
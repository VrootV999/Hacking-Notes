# Collecting Disk Image(Using dd)

- Extracting raw image
```bash
sudo dd if=/dev/sdX of=disk.img bs=4M status=progress conv=noerror,sync
```

- Better image extraction with logs and hash
```bash
sudo dc3dd if=/dev/sdX of=disk.img hash=sha256 log=acquire.log
```

- Verify hash
```bash
sha256sum disk.img
```

---

# Ram 

- Linux
`sudo LiME -f ram.lime -d /mnt/external/`

- MacOS
`sudo osxpmem.app/Contents/MacOS/osxpmem -o ram.raw`

- Windows

DumpIt
Magnet RAM Capture
Belkasoft RAM Capturer

- Android
```bash
dd if=/dev/mem of=ram.img
```

---

# Firware Image

```bash
sudo flashrom -p ch341a_spi -r firmware.bin
```

---

# Bios/UEFI Image

```bash
sudo flashrom -p internal -r bios.bin
```

---

# Mobile rom 

- using fastboot
```bash
fastboot boot recovery.img
adb pull /dev/block/by-name/system system.img
```

- using twrp
Enter boot recovery
Image partition via dd

- EDL Mode (Qualcomm)

---

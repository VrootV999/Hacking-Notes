forensic way to recover any type of file

# fdisk -l
> [!NOTE]
> Never run foremost on the same partition that is being used

```bash
sudo foremost -i (device name from foremost)
```

> [!NOTE]
> the files are stored at the cwd at output folder


# restrict search

sudo foremost -v -q -t png,zip,jpg -i /dev/name -o $HOME/Desktop/recover
`-v`    for verbose
`-t`    for type
`-q`    for quick mode

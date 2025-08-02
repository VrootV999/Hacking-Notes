forensic way to recover any type of file

# fdisk -l
// note never run foremost on the same partition that is being used

# sudo foremost -i (device name from foremost)
the files are stored at the cwd at output folder

# restrict search

sudo foremost -v -q -t png,zip,jpg -i /dev/name -o $HOME/Desktop/recover
-v    for verbose
-q    for quick mode
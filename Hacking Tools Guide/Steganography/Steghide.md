
# Syntax
embed -cf (file) -ef (secret)                Embed secret into a file
extract -sf (file)                                    Extract secret from a file
-P (password)                                       Specify passphrase

# Example:
steghide embed -cf image.jpg -ef secret.txt -P password

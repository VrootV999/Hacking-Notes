# Arguments

> [!NOTE]  Note
> ffmpeg supports audio, video and image manipulation

- `-1`          input File
- `-c`          codec to use
- `-q`         video quality(for avi) (lower number = higher quality and higher size)
- `-crf`       video quality(for mp4) (same as q) 
- `-c:v  (format)`              video format to be used 
- `-c:a  (format)`              audio format to be used
- `-b:v  (number)`              bitrate for video  (1500-5000)
- `-b:a (number)`               bitrate for audio   (128-320)
- `-r (number)`                 frame rate 
- `-s (resolution)`             change the resolution of the video output
- `-vf `                        for changing aspects of the output (filter graph)
    - `eq=brightness=(float value)`             for changing brightness  
    - `scale=length:width`                      for changing scale
- `-filter:a`                   add filters for audio
    - `volume=(multiplier value or float)`      change volume
    - `channelmap=0-0|1-0`                      input left to audio right and vise versa
- `-filter:v`                   add filter for video
    - `crop=w=width:h=height:x=value:y=value`   crop  (x and y for top left corners)
    > can also do arithmetics by consiering inh as height and in_w as width 

    > [!EXAMPLE]
    > `ffmpeg -i test.mp4 -filter:v "crop=w=2/3*in_w:h=2/3*in_h" testedited.mp4`

    - `scale=w=width:h=height`  scale the video
    - `rotate=YOURDEGREE*PI/180`rotate the video
# add subtitles

1. create an srt file
```srt
1
00:00:00,000 -->  00:00:01,000
welcome to my ffmpeg tutorial
```
2. Convert it to ASS file (advanced substation alpha) then add it in
```bash
ffmpeg -i file.srt subtitles.ass

# add it in the video
ffmpeg -i ffmpeg\ tutorial.mp4 -vf ass=subtitles.ass final.mp4
```


# For multiple input
> 1. create a txt file as following
> 2. -i as the file.txt
> 3. -f concat 
> 4. -c copy (codec)
```txt
file 'file1.mp4'
file 'file2.mp4'
```



# convert photos to video
```bash
#single photo
ffmpeg -loop 1 -f image2 -i img.png -t 1 out.mp4


```

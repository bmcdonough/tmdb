# summary
script to rename shows using the API of The Movie Database (TMDB)
## attribution
![alt text](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg "The Movie Database")
## create .env
- create **.env** file with the following contents, populated from your personal account:  [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
```shell
TMDB_API_KEY = "your api key here"
TMDB_ACCESS_TOKEN = "your api access token here"
```
## use
### requirements
```shell
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
### run
```shell
python3 rename_shows.py
Please enter a search string: sanford and son
```

# references
## mkvpropedit info
```shell
mkvpropedit --list-property-names info
All known property names and their meaning

Elements in the category 'Segment information' ('--edit info'):
title               | US | Title: The title for the whole movie.
date                | DT | Date: The date the file was created.
segment-filename    | US | Segment filename: The file name for this segment.
prev-filename       | US | Previous filename: An escaped filename corresponding to the previous segment.
next-filename       | US | Next filename: An escaped filename corresponding to the next segment.
segment-uid         | X  | Segment unique ID: A randomly generated unique ID to identify the current segment between many others (128 bits).
prev-uid            | X  | Previous segment's unique ID: A unique ID to identify the previous chained segment (128 bits).
next-uid            | X  | Next segment's unique ID: A unique ID to identify the next chained segment (128 bits).
muxing-application  | US | Multiplexing application: The name of the application or library used for multiplexing the file.
writing-application | US | Writing application: The name of the application or library used for writing the file.

Elements in the category 'Track headers' ('--edit track:...'):
track-number                     | UI | Track number: The track number as used in the Block Header.
track-uid                        | UI | Track UID: A unique ID to identify the Track. This should be kept the same when making a direct stream copy of the Track to another file.
flag-commentary                  | B  | "Commentary" flag: Can be set if the track contains commentary.
flag-default                     | B  | "Default track" flag: Set if that track (audio, video or subs) SHOULD be used if no language found matches the user preference.
flag-enabled                     | B  | "Track enabled" flag: Set if the track is used.
flag-forced                      | B  | "Forced display" flag: Can be set for tracks containing onscreen text or foreign-language dialog.
flag-hearing-impaired            | B  | "Hearing impaired" flag: Can be set if the track is suitable for users with hearing impairments.
flag-original                    | B  | "Original language" flag: Can be set if the track is in the content's original language (not a translation).
flag-text-descriptions           | B  | "Text descriptions" flag: Can be set if the track contains textual descriptions of video content suitable for playback via a text-to-speech system for a visually-impaired user.
flag-visual-impaired             | B  | "Visual impaired" flag: Can be set if the track is suitable for users with visual impairments.
min-cache                        | UI | Minimum cache: The minimum number of frames a player should be able to cache during playback. If set to 0, the reference pseudo-cache system is not used.
max-cache                        | UI | Maximum cache: The maximum number of frames a player should be able to cache during playback. If set to 0, the reference pseudo-cache system is not used.
default-duration                 | UI | Default duration: Number of nanoseconds (not scaled) per frame.
name                             | US | Name: A human-readable track name.
language                         | S  | Language: Specifies the language of the track.
language-ietf                    | S  | Language (IETF BCP 47): Specifies the language of the track in the form of a BCP 47 language tag.
codec-id                         | S  | Codec ID: An ID corresponding to the codec.
codec-name                       | US | Codec name: A human-readable string specifying the codec.
codec-delay                      | UI | Codec-inherent delay: Delay built into the codec during decoding in ns.
interlaced                       | UI | Video interlaced flag: Set if the video is interlaced.
pixel-width                      | UI | Video pixel width: Width of the encoded video frames in pixels.
pixel-height                     | UI | Video pixel height: Height of the encoded video frames in pixels.
display-width                    | UI | Video display width: Width of the video frames to display.
display-height                   | UI | Video display height: Height of the video frames to display.
display-unit                     | UI | Video display unit: Type of the unit for DisplayWidth/Height (0: pixels, 1: centimeters, 2: inches, 3: aspect ratio).
pixel-crop-left                  | UI | Video crop left: The number of video pixels to remove on the left of the image.
pixel-crop-top                   | UI | Video crop top: The number of video pixels to remove on the top of the image.
pixel-crop-right                 | UI | Video crop right: The number of video pixels to remove on the right of the image.
pixel-crop-bottom                | UI | Video crop bottom: The number of video pixels to remove on the bottom of the image.
aspect-ratio-type                | UI | Video aspect ratio type: Specify the possible modifications to the aspect ratio (0: free resizing, 1: keep aspect ratio, 2: fixed).
field-order                      | UI | Video field order: Field order (0, 1, 2, 6, 9 or 14, see documentation).
stereo-mode                      | UI | Video stereo mode: Stereo-3D video mode (0 - 14, see documentation).
colour-matrix-coefficients       | UI | Video: colour matrix coefficients: Sets the matrix coefficients of the video used to derive luma and chroma values from red, green and blue color primaries.
colour-bits-per-channel          | UI | Video: bits per colour channel: Sets the number of coded bits for a colour channel.
chroma-subsample-horizontal      | UI | Video: pixels to remove in chroma: The amount of pixels to remove in the Cr and Cb channels for every pixel not removed horizontally.
chroma-subsample-vertical        | UI | Video: pixels to remove in chroma: The amount of pixels to remove in the Cr and Cb channels for every pixel not removed vertically.
cb-subsample-horizontal          | UI | Video: pixels to remove in Cb: The amount of pixels to remove in the Cb channel for every pixel not removed horizontally. This is additive with chroma-subsample-horizontal.
cb-subsample-vertical            | UI | Video: pixels to remove in Cb: The amount of pixels to remove in the Cb channel for every pixel not removed vertically. This is additive with chroma-subsample-vertical.
chroma-siting-horizontal         | UI | Video: horizontal chroma siting: How chroma is sited horizontally.
chroma-siting-vertical           | UI | Video: vertical chroma siting: How chroma is sited vertically.
colour-range                     | UI | Video: colour range: Clipping of the color ranges.
colour-transfer-characteristics  | UI | Video: transfer characteristics: The colour transfer characteristics of the video.
colour-primaries                 | UI | Video: colour primaries: The colour primaries of the video.
max-content-light                | UI | Video: maximum content light: Maximum brightness of a single pixel in candelas per square meter (cd/mmax-frame-light                  | UI | Video: maximum frame light: Maximum frame-average light level in candelas per square meter (cd/mchromaticity-coordinates-red-x   | FP | Video: chromaticity red X: Red X chromaticity coordinate as defined by CIE 1931.
chromaticity-coordinates-red-y   | FP | Video: chromaticity red Y: Red Y chromaticity coordinate as defined by CIE 1931.
chromaticity-coordinates-green-x | FP | Video: chromaticity green X: Green X chromaticity coordinate as defined by CIE 1931.
chromaticity-coordinates-green-y | FP | Video: chromaticity green Y: Green Y chromaticity coordinate as defined by CIE 1931.
chromaticity-coordinates-blue-x  | FP | Video: chromaticity blue X: Blue X chromaticity coordinate as defined by CIE 1931.
chromaticity-coordinates-blue-y  | FP | Video: chromaticity blue Y: Blue Y chromaticity coordinate as defined by CIE 1931.
white-coordinates-x              | FP | Video: white point X: White colour chromaticity coordinate X as defined by CIE 1931.
white-coordinates-y              | FP | Video: white point Y: White colour chromaticity coordinate Y as defined by CIE 1931.
max-luminance                    | FP | Video: maximum luminance: Maximum luminance in candelas per square meter (cd/mmin-luminance                    | FP | Video: minimum luminance: Minimum luminance in candelas per square meter (cd/mprojection-type                  | UI | Video: projection type: Describes the projection used for this video track (0 projection-private               | X  | Video: projection-specific data: Private data that only applies to a specific projection.
projection-pose-yaw              | FP | Video: projection's yaw rotation: Specifies a yaw rotation to the projection.
projection-pose-pitch            | FP | Video: projection's pitch rotation: Specifies a pitch rotation to the projection.
projection-pose-roll             | FP | Video: projection's roll rotation: Specifies a roll rotation to the projection.
sampling-frequency               | FP | Audio sampling frequency: Sampling frequency in Hz.
output-sampling-frequency        | FP | Audio output sampling frequency: Real output sampling frequency in Hz.
channels                         | UI | Audio channels: Numbers of channels in the track.
bit-depth                        | UI | Audio bit depth: Bits per sample, mostly used for PCM.

Element types:
  SI: signed integer
  UI: unsigned integer
  B:  boolean (0 or 1)
  S:  string
  US: Unicode string
  X:  binary in hex
  FP: floating point number
  DT: date & time
```

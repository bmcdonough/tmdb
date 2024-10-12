from pymediainfo import MediaInfo

media_info = MediaInfo.parse('/home/wrmcd/01072fecf05d7f211b80ce74b9a225661c6446de756a7a92061bb02b15d3326b.mkv')
for track in media_info.tracks:
    if track.track_type == 'Video':
        print(f'Width: {track.width}, Height: {track.height}, Duration: {track.duration} ms')

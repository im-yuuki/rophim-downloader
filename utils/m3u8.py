import m3u8

def load_playlist(playlist_content: str) -> m3u8.M3U8:
    return m3u8.loads(playlist_content)

def get_variant_playlists(playlist: m3u8.M3U8) -> list:
    return playlist.playlists

def get_first_variant_playlist(playlist: m3u8.M3U8) -> m3u8.Playlist:
    variants = get_variant_playlists(playlist)
    if not variants:
        raise Exception("No variant playlists found")
    return variants[0]


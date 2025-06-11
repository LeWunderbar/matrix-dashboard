import spotipy
import os

class SpotifyModule:
    def __init__(self, config):
        self.invalid = False
        
        if config is not None and 'Spotify' in config and 'client_id' in config['Spotify'] \
            and 'client_secret' in config['Spotify'] and 'redirect_uri' in config['Spotify']:
            
            client_id = config['Spotify']['client_id']
            client_secret = config['Spotify']['client_secret']
            redirect_uri = config['Spotify']['redirect_uri']
            if client_id and client_secret and redirect_uri:
                try:
                    os.environ["SPOTIPY_CLIENT_ID"] = client_id
                    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
                    os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

                    scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
                    self.auth_manager = spotipy.SpotifyOAuth(scope=scope)
                    print(self.auth_manager.get_authorize_url())
                    self.sp = spotipy.Spotify(auth_manager=self.auth_manager, requests_timeout=10)
                    self.isPlaying = False
                except Exception as e:
                    print(e)
                    self.invalid = True
            else:
                print("[Spotify Module] Empty Spotify client id or secret")
                self.invalid = True
        else:
            print("[Spotify Module] Missing config parameters")
            self.invalid = True
    
    def isInvalid(self):
        return self.invalid

    def _get_active_device_id(self):
        try:
            devices = self.sp.devices().get('devices', [])
            active_devices = [d for d in devices if d.get('is_active', False)]
            return active_devices[0]['id'] if active_devices else None
        except Exception as e:
            print(f"Error getting devices: {e}")
            return None

    def getCurrentPlayback(self):
        if self.invalid:
            return None

        try:
            track = self.sp.current_user_playing_track()
            if track is None:
                return None

            if track.get('item') is None:
                return (None, None, None, False, 0, 0)

            artist = track['item']['artists'][0]['name']
            if len(track['item']['artists']) >= 2:
                artist += ", " + track['item']['artists'][1]['name']

            title = track['item']['name']
            if track['item'].get('album') and track['item']['album'].get('images'):
                art_url = track['item']['album']['images'][0]['url']
            else:
                art_url = None
            is_playing = track.get('is_playing', False)
            progress_ms = track.get('progress_ms', 0)
            duration_ms = track['item'].get('duration_ms', 0)

            return (artist, title, art_url, is_playing, progress_ms, duration_ms)
        except Exception as e:
            print(f"Error in getCurrentPlayback: {e}")
            return None

    def resume_playback(self):
        if self.invalid:
            return
        device_id = self._get_active_device_id()
        if not device_id:
            print("No active devices found")
            return
        try:
            self.sp.start_playback(device_id=device_id)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Playback error: {e}")

    def pause_playback(self):
        if self.invalid:
            return
        device_id = self._get_active_device_id()
        if not device_id:
            print("No active devices found")
            return
        try:
            self.sp.pause_playback(device_id=device_id)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Playback error: {e}")

    def next_track(self):
        if self.invalid:
            return
        device_id = self._get_active_device_id()
        if not device_id:
            print("No active devices found")
            return
        try:
            self.sp.next_track(device_id=device_id)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Playback error: {e}")

    def previous_track(self):
        if self.invalid:
            return
        device_id = self._get_active_device_id()
        if not device_id:
            print("No active devices found")
            return
        try:
            self.sp.previous_track(device_id=device_id)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Playback error: {e}")

    def increase_volume(self):
        if self.invalid or not self.isPlaying:
            return
        device_id = self._get_active_device_id()
        if not device_id:
            print("No active devices found")
            return
        try:
            devices = self.sp.devices().get('devices', [])
            if devices:
                curr_volume = devices[0].get('volume_percent', 50)
                self.sp.volume(min(100, curr_volume + 5), device_id=device_id)
        except Exception as e:
            print(f"Volume error: {e}")

    def decrease_volume(self):
        if self.invalid or not self.isPlaying:
            return
        device_id = self._get_active_device_id()
        if not device_id:
            print("No active devices found")
            return
        try:
            devices = self.sp.devices().get('devices', [])
            if devices:
                curr_volume = devices[0].get('volume_percent', 50)
                self.sp.volume(max(0, curr_volume - 5), device_id=device_id)
        except Exception as e:
            print(f"Volume error: {e}")

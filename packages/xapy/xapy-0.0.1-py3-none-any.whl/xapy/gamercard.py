# encoding: utf-8
class Gamercard:

    def __init__(self, gamertag: str, name: str, location: str, bio: str, gamerscore: int, tier: str, motto: str,
                 avatar_body_image_path: str, gamerpic_small_image_path: str, gamerpic_small_ssl_image_path: str,
                 gamerpic_large_image_path: str, gamerpic_large_ssl_image_path: str, avatar_manifest: str):
        self.gamertag = gamertag
        self.name = name
        self.location = location
        self.bio = bio
        self.gamerscore = gamerscore
        self.tier = tier
        self.motto = motto
        self.avatar_body_image_path = avatar_body_image_path
        self.gamerpic_small_image_path = gamerpic_small_image_path
        self.gamerpic_small_ssl_image_path = gamerpic_small_ssl_image_path
        self.gamerpic_large_image_path = gamerpic_large_image_path
        self.gamerpic_large_ssl_image_path = gamerpic_large_ssl_image_path
        self.avatar_manifest = avatar_manifest

    def __str__(self):
        return 'Gamercard for {}'.format(self.gamertag)

    @staticmethod
    def from_api_response(json_data):
        return Gamercard(
            json_data['gamertag'],
            json_data['name'],
            json_data['location'],
            json_data['bio'],
            json_data['gamerscore'],
            json_data['tier'],
            json_data['motto'],
            json_data['avatarBodyImagePath'],
            json_data['gamerpicSmallImagePath'],
            json_data['gamerpicLargeImagePath'],
            json_data['gamerpicSmallSslImagePath'],
            json_data['gamerpicLargeSslImagePath'],
            json_data['avatarManifest']
        )

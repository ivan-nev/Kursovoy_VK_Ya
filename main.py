import requests
import time
from pprint import pprint


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def user_foto(self, album, offset):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': album, 'extended': '1', 'photo_sizes': '1', 'offset': offset}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def foto_dict(self, list_album):
        dict_foto = {}
        for album in list_album:
            offset = 0
            while True:
                user_foto = self.user_foto(album, offset)
                # time.sleep(0.04)
                for item in user_foto['response']['items']:
                    like = item['likes']['count']
                    post_id = item['id']
                    max_size = 0
                    for foto in item['sizes']:
                        foto_size = int(foto['height']) * int(foto['width'])
                        if foto_size > max_size:
                            max_size = foto_size
                            dict_foto[f'like{like}_id{post_id}'] = [foto['url'], foto_size]
                offset += len(user_foto['response']['items'])
                print (offset)
                if offset >= user_foto['response']['count']:
                    break
        return dict_foto


if __name__ == '__main__':
    with open('token/tokenYA.txt', 'r', ) as fileYA:
        tokenYA = fileYA.read()
    with open('token/tokenVK.txt', 'r', ) as fileVK:
        tokenVK = fileVK.read()

    user_id1 = '2632492'
    vk1 = VK(tokenVK, user_id1)
    user_id2 = '19020548'
    vk2 = VK(tokenVK, user_id2)
    user_id3 = '-107913084'
    vk3 = VK(tokenVK, user_id3)

    print(vk3.users_info())
    # y = (vk3.user_foto(['wall'], 0))
    # pprint(y)
    z = vk3.foto_dict([ 'wall'])
    pprint(z)
    print(len(z))

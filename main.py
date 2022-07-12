import requests
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

   def user_foto(self):
       url = 'https://api.vk.com/method/photos.get'
       params = {'owner_id': self.id, 'album_id': 'wall', 'extended':'1','photo_sizes':'1'}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def foto_dict(self):
       dict_foto = {}
       for item in self.user_foto()['response']['items']:
           like = item['likes']['count']
           post_id = item['id']
           max_size = 0
           for foto in item['sizes']:
               foto_size = int(foto['height']) * int(foto['width'])
               if foto_size > max_size:
                   max_size = foto_size
                   dict_foto[f'like{like}_id{post_id}'] = [foto['url'], foto_size]
       return dict_foto




if __name__ == '__main__':
    with open('token/tokenYA.txt', 'r',) as fileYA:
        tokenYA = fileYA.read()
    with open('token/tokenVK.txt', 'r',) as fileVK:
        tokenVK = fileVK.read()

    # url = 'https://api.vk.com/method/photos.get'
    # params = {'access_token': tokenVK, 'v': '5.131', 'owner_id':'2632492', 'album_id':'profile', 'extended':'1','photo_sizes':'1'}
    # response = requests.get(url, params=params)
    # pprint(response.json())

    user_id = '2632492'
    user_id = '19020548'
    vk = VK(tokenVK, user_id)
    print(vk.users_info())
    # pprint(vk.user_foto())
    pprint(vk.foto_dict())




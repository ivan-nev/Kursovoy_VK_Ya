import requests
import time
import json
from pprint import pprint
# from progress.bar import IncrementalBar
import yadisk
from tqdm import tqdm



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

    def user_foto(self, album, offset=0):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': album, 'extended': '1', 'photo_sizes': '1', 'offset': offset}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def foto_dict(self, list_album): # словарь вида {like_id:[url,size(Wxh)]}
        dict_foto = {}
        for album in list_album: # альбомы на стене и в профайле
            offset = 0
            while True:   #
                user_foto = self.user_foto(album, offset)
                for item in (user_foto['response']['items']): # заходим в гр. одинаковых фотог.
                    like = item['likes']['count']
                    post_id = item['id']
                    max_size = 0
                    for foto in item['sizes']:
                        foto_size = int(foto['height']) * int(foto['width'])
                        if foto_size > max_size:  # выбираем самое большое из группы одинаковых
                            max_size = foto_size
                            dict_foto[f'like{like}_id{post_id}'] = [foto['url'], foto_size]

                offset += len(user_foto['response']['items'])
                if offset >= user_foto['response']['count']:
                    break
        return dict_foto

class My_Ya(yadisk.YaDisk):


    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def sort_dict(self, dict_foto): # сортировка словаря вида {key:[val1,val2]} по убыванию val2
        temp_d = {x: y[1] for x, y in dict_foto.items()}
        sorted_keys = sorted(temp_d, key=temp_d.get, reverse=True)
        return {x: dict_foto[x] for x in sorted_keys}

    def upload_file(self, dict_foto, path, num=5):
        path = (f'Py/Pictures_user_id{path}')
        try:
            self.remove(path)
            time.sleep(5)
        except yadisk.exceptions.PathNotFoundError:
            pass
        self.mkdir(path)
        time.sleep(0.5)
        count = 1
        for foto_name, url in tqdm(self.sort_dict(dict_foto).items()):
            # print (foto_name,url[0])
            if count > num:
                break
            self.upload_url(url[0], (f'{path}/{foto_name}.jpg'))
            count += 1

    def get_file_list(self,path):
        total = 1
        offset = 0
        list_total =[]
        while offset < total:
            path_full = (f'Py/Pictures_user_id{path}')
            headers = self.get_headers()
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
            params = {"path": path_full, 'offset':offset, "fields": "_embedded.items.name, "
                                                       "_embedded.items.size, _embedded.total"}
            response = requests.get(upload_url, params=params, headers=headers)
            list1 = response.json()['_embedded'] ['items']
            list_total.extend(list1)
            total = response.json()['_embedded'] ['total']
            offset = len(list_total)
            print (list1)
            print(len(list1))

        with open(f"id_{path}.json", "w") as write_file:
            json.dump(list_total, write_file)








if __name__ == '__main__':
    with open('token/tokenYA.txt', 'r', ) as fileYA:
        tokenYA = fileYA.read()
    with open('token/tokenVK.txt', 'r', ) as fileVK:
        tokenVK = fileVK.read()


    user_id1 = '2632492'
    user_id2 = '19020548'
    user_id3 = '-116129052'

    user = user_id3

    vk1 = VK(tokenVK, user)
    Ya = My_Ya(token=tokenYA)

    z = vk1.foto_dict([ 'wall', 'profile'])
    # pprint(z)
    print(len(z))
    num = int(input(f'Найдено {len(z)} фото. Сколько загрузить самых больших (WxH): '))
    Ya.upload_file(z, user, num)
    time.sleep(2)
    Ya.get_file_list(user)

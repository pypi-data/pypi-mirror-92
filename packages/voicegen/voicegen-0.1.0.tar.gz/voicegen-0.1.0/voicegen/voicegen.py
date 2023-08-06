# ##############################################################################
#  Copyright (c) 2021. Projects from AndreyM                                   #
#  The best encoder in the world!                                              #
#  email: muraig@ya.ru                                                         #
# ##############################################################################

# -*- coding: utf-8 -*-

""" Скрипт для создания голосового файла из запроса с параметрами.
Скрипт обращается к web серверу, поднятому
из пакета rhvoice-wrapper по адресу: http://192.168.1.204:8080

Вызывается так:
import voicegen
all_json = voicegen.read_data_str(all_data)
output = voicegen.TTS(all_json)
output.save(all_json['file_path'])
print(all_json['file_path'] + ' generated!')

где all_data - пары key:value:
{'data': {'url': 'http://192.168.1.204:8080', 'text': '3472.81'},
 'params': {'voice': 'artemiy', 'format': 'wav'},
 'opts': {'rate': '35', 'pitch': '25', 'volume': '200'},
 'outfile': {'outf': '3472.81', 'path': '/var/lib/asterisk/sounds/autodial/'}
}
"requests", "pytils", "sox", "os.path",
"""

import json
import sys
import requests
import pytils

import sox
import os.path


class Error(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


###############################
# Класс дл создания звуковых файлов
class TTS:
    TTS_URL = "{}/say"

    def __init__(self, all_json_):
        """ text, url=None, voice=None, format_=None, rate=None, pitch=None, volume=None """
        url = all_json_['url']
        self._url = self.TTS_URL.format(url)
        # print('self._url:', self._url);        sys.exit()
        self.__params = {
            'text': all_json_['text'],
            'voice': all_json_['voice'],
            'format': all_json_['format_'],
            'rate': all_json_['rate'],
            'pitch': all_json_['pitch'],
            'volume': all_json_['volume']
        }
        self._data = None
        self._generate()

    def _generate(self):
        try:
            rq = requests.get(self._url, params=self.__params, stream=False)
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            raise Error(code=1, msg=str(e))
        code = rq.status_code
        if code != 200:
            raise Error(code=code, msg='http code != 200')
        self._data = rq.iter_content()

    def save(self, file_path_):
        if self._data is None:
            raise Exception('There\'s nothing to save')

        with open(file_path_, 'wb') as f:
            for d in self._data:
                f.write(d)
        # Декодируем файл в 8000kGz
        sox_transformer(file_path_)
        return file_path_


def sox_transformer(file_path_):
    """Преобразуем файл в  8000kGz, иначе asterisk не примет"""
    file_new = file_path_.rsplit('.', maxsplit=1)[0] + '.mp3'
    os.rename(file_path_, file_new)
    fm = sox.Transformer()
    fm.set_output_format(file_type='wav', rate=8000, bits=16, channels=1, encoding='signed-integer')
    fm.build(file_new, file_path_)
    os.unlink(file_new)

    return file_path_


# =================================================#
# Вспомогательные функции

def is_float(s):
    try:
        float(s)
        return True
    except Error:
        return False


def float_to_worlds(text):
    text = float(text)
    """ Преобразуем float в строку: text = 'две тысячи двести двадцать два рубля двадать две копейки' """
    summa = pytils.numeral.rubles(text)  # Переводим это число в строку, состоящую из слов этой суммы
    return summa


def contract_to_worlds(text):
    text = int(text)
    """ Преобразуем float в строку: text = 'две тысячи двести двадцать два' """
    contract = pytils.numeral.in_words_int(text)  # Переводим это число в строку, состоящую из слов этой суммы
    return contract


def check_arguments():
    """Проверка на наличие необходимых параметров."""
    if len(sys.argv) < 2:
        print("""Вызываем скрипт с парметрами, например:
        %s
        {"data": {"url": "http://127.0.0.1:8080", "text": "тут просто текст"},
        "params": {"voice": "artemiy", "format": "wav"},"opts": {"rate": "35", "pitch": "25",
        "volume": "200"},"outfile": {"outfile": "text"}}""" % sys.argv[0])
        sys.exit(-1)
    else:
        x_ = sys.argv[1]
    return x_


# =================================================#
# основная функция обработки алгоритма скрипта
#


def read_data_str(x_):
    """ Из командкной строки получаем строку аргументов, где первый аргумент - имя вызываемого скрипта
    и проверяем количество параметров """
    x_ = json.loads(x_)
    # print(x_); sys.exit()
    """ Получаем данные и создаем переменные для организации вызова """
    url = x_['data']['url']
    text = x_['data']['text']
    formats = x_['params']['format']
    voice = x_['params']['voice']
    rate = x_['opts']['rate']
    pitch = x_['opts']['pitch']
    volume = x_['opts']['volume']
    outfile = x_['outfile']['outf']
    path = x_['outfile']['path']
    """Проверка: сумма или контракт"""
    if is_float(text):
        summa = float_to_worlds(text)
    else:
        contract = contract_to_worlds(text)
        summa = contract
    file_path = path + str(outfile) + '.' + formats
    all_key = ('text', 'file_path', 'url', 'voice', 'format_', 'rate', 'pitch', 'volume')
    all_data_ = (summa, file_path, url, voice, formats, rate, pitch, volume, path, outfile, text)
    all_json_ = dict(zip(all_key, all_data_))
    return all_json_


""" Для переноса файлов на астериск, монтируем с него папку /var/lib/asterisk/sounds/autodial
с указанием парметров в exports, вот так:
/var/lib/asterisk/sounds/autodial 192.168.xxx.xxx/24(rw,async,no_subtree_check,all_squash,anonuid=995,anongid=995)
"""

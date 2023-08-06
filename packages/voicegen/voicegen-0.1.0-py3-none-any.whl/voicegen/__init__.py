# ##############################################################################
#  Copyright (c) 2020. Projects from AndreyM                                   #
#  The best encoder in the world!                                              #
#  email: muraig@ya.ru                                                         #
# ##############################################################################
"""
Скрипт для создания аудио файлов, используемых в автообзвоне.
Andrey M
muraigtor@gmail.com
"""

from .voicegen import read_data_str, TTS, Error, is_float, float_to_worlds, contract_to_worlds

__all__ = ['read_data_str', 'TTS', 'Error', 'is_float', 'float_to_worlds', 'contract_to_worlds']

__version__ = '0.1.0'

__author__ = 'Andrey Murashev'

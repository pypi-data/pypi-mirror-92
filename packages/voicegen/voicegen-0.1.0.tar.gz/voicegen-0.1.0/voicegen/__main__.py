# ##############################################################################
#  Copyright (c) 2021. Projects from AndreyM                                   #
#  The best encoder in the world!                                              #
#  email: muraig@ya.ru                                                         #
# ##############################################################################

""" Для переноса файлов на астериск, монтируем с него папку /var/lib/asterisk/sounds/autodial
с указанием парметров в exports, вот так:
/var/lib/asterisk/sounds/autodial 192.168.7.0/24(rw,async,no_subtree_check,all_squash,anonuid=995,anongid=995)
"""

from .voicegen import check_arguments, read_data_str, TTS

x = check_arguments()
all_json = read_data_str(x)
output = TTS(all_json)
print('all_json:', all_json)
output.save(all_json['file_path'])
print(all_json['file_path'] + ' generated!')

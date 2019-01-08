import requests
import os
from db_lib import get_internal_id, get_file_type_size
import csv
import shutil


BASE_DIR = '/home/tiagoslg/projects/dspace-covemg/DSpace_COVEMG/'


def remove_caracter_especial(texto):
    d = {'À': 'A', 'Á': 'A', 'Ä': 'A', 'Â': 'A', 'Ã': 'A',
         'È': 'E', 'É': 'E', 'Ë': 'E', 'Ê': 'E',
         'Ì': 'I', 'Í': 'I', 'Ï': 'I', 'Î': 'I',
         'Ò': 'O', 'Ó': 'O', 'Ö': 'O', 'Ô': 'O', 'Õ': 'O',
         'Ù': 'U', 'Ú': 'U', 'Ü': 'U', 'Û': 'U',
         'à': 'a', 'á': 'a', 'ä': 'a', 'â': 'a', 'ã': 'a', 'ª': 'a',
         'è': 'e', 'é': 'e', 'ë': 'e', 'ê': 'e',
         'ì': 'i', 'í': 'i', 'ï': 'i', 'î': 'i',
         'ò': 'o', 'ó': 'o', 'ö': 'o', 'ô': 'o', 'õ': 'o', 'º': 'o', '°': 'o',
         'ù': 'u', 'ú': 'u', 'ü': 'u', 'û': 'u',
         'Ç': 'C', 'ç': 'c',
         ':': '_', '(': '', ')': ''}
    novo_texto = ''

    for c in range(0, len(texto)):
        novo_caracter = texto[c]
        try:
            novo_caracter = d[texto[c]]
        except KeyError:
            pass

        novo_texto = novo_texto + novo_caracter

    return novo_texto


def get_session_cookie():
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/login'
    data = {'email': '<email>',
            'password': '<senha>'}
    r = requests.post(url,
                      data=data)

    return r.cookies


def get_response(url):
    cookies = SESSION_COOKIES if SESSION_COOKIES else get_session_cookie()
    return requests.get(url, cookies=cookies)


def os_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_hierarchy():
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/hierarchy'
    return get_response(url)


SESSION_COOKIES = get_session_cookie()
HIE_JSON = get_hierarchy().json()


def get_top_level_communities():
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/communities/top-communities'
    resp = get_response(url)
    return resp


def get_community(community_id):
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/communities/{}'.format(community_id)
    resp = get_response(url)
    return resp


def get_community_collections(community_id):
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/communities/{}/collections'.format(community_id)
    resp = get_response(url)
    return resp


def get_community_communities(community_id):
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/communities/{}/communities'.format(community_id)
    resp = get_response(url)
    return resp


def get_collection_items(collection_id):
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/collections/{}/items'.format(collection_id)
    resp = get_response(url)
    return resp


def get_item_bitstreams(item_id):
    url = 'http://www.comissaodaverdade.mg.gov.br/rest/items/{}/bitstreams'.format(item_id)
    resp = get_response(url)
    return resp


def create_dirs():
    """
    Cria estrutura de diretórios com até dois níveis de subcomunidades
    A escolha por limitar o número de níveis foi feita em função de termos apenas a comunidade
    12. Repressão ao movimento estudantil, com mais de 2 níveis
    """
    hie_json = HIE_JSON
    os.chdir(BASE_DIR)
    os_makedirs(hie_json['name'])
    os.chdir(hie_json['name'])
    for com in hie_json['community']:
        os.chdir('{}/{}'.format(BASE_DIR, hie_json['name']))
        os_makedirs(com['name'])
        os.chdir(com['name'])
        com_path = os.getcwd()
        for col in com['collection']:
            os_makedirs(col['name'])
        for sub_com in com['community']:
            os.chdir(com_path)
            os_makedirs(sub_com['name'])
            os.chdir(sub_com['name'])
            for col in sub_com['collection']:
                os_makedirs(col['name'])


def create_file_list():
    """
    Cria a lista de arquivos com até dois níveis de subcomunidades
    A escolha por limitar o número de níveis foi feita em função de termos apenas a comunidade
    12. Repressão ao movimento estudantil, com mais de 2 níveis
    """
    hie_json = HIE_JSON
    base_path_list = [BASE_DIR]
    file_list = []
    for com in hie_json['community']:
        com_path = []
        com_path.extend(base_path_list)
        com_path.append(com['name'].replace('/', ''))
        for sub_com in com['community']:
            sub_com_path = []
            sub_com_path.extend(com_path)
            sub_com_path.append(sub_com['name'].replace('/', ''))
            for col in sub_com['collection']:
                col_path = []
                col_path.extend(sub_com_path)
                col_path.append(col['name'].replace('/', ''))
                items = get_collection_items(col['id']).json()
                for item in items:
                    item_path = []
                    item_path.extend(col_path)
                    item_path.append(item['name'].replace('/', ''))
                    bitstreams = get_item_bitstreams(item['uuid']).json()
                    for bitstream in bitstreams:
                        internal_id = get_internal_id(bitstream['uuid'])[0]
                        type_size = get_file_type_size(internal_id)
                        path = '/'.join(item_path).replace('//', '/')
                        path = remove_caracter_especial('_'.join(path.split()))
                        bitstream_dict = {
                            'path': path,
                            'name': remove_caracter_especial('_'.join(bitstream['name'].split())),
                            'internal_id': internal_id,
                            'relative_path': '{}/{}/{}'.format(internal_id[:2],
                                                               internal_id[2:4],
                                                               internal_id[4:6]),
                            'type': type_size[0],
                            'size': type_size[1]
                        }
                        file_list.append(bitstream_dict)
                        print(file_list.__len__())
        for col in com['collection']:
            col_path = []
            col_path.extend(com_path)
            col_path.append(col['name'].replace('/', ''))
            items = get_collection_items(col['id']).json()
            for item in items:
                item_path = []
                item_path.extend(col_path)
                item_path.append(item['name'].replace('/', ''))
                bitstreams = get_item_bitstreams(item['uuid']).json()
                for bitstream in bitstreams:
                    internal_id = get_internal_id(bitstream['uuid'])[0]
                    type_size = get_file_type_size(internal_id)
                    path = '/'.join(item_path).replace('//', '/')
                    path = remove_caracter_especial('_'.join(path.split()))
                    bitstream_dict = {
                        'path': path,
                        'name': remove_caracter_especial('_'.join(bitstream['name'].split())),
                        'internal_id': internal_id,
                        'relative_path': '{}/{}/{}'.format(internal_id[:2],
                                                           internal_id[2:4],
                                                           internal_id[4:6]),
                            'type': type_size[0],
                            'size': type_size[1]
                    }
                    file_list.append(bitstream_dict)
                    print(file_list.__len__())
    com = hie_json['community'][10]
    sub_com = com['community'][0]
    sub_com_2 = sub_com['community'][0]
    com_path = []
    com_path.extend(base_path_list)
    com_path.append(com['name'])
    sub_com_path = []
    sub_com_path.extend(com_path)
    sub_com_path.append(sub_com['name'].replace('/', ''))
    sub_com_path.append(sub_com_2['name'].replace('/', ''))
    for col in sub_com_2['collection']:
        col_path = []
        col_path.extend(sub_com_path)
        col_path.append(col['name'].replace('/', ''))
        items = get_collection_items(col['id']).json()
        for item in items:
            item_path = []
            item_path.extend(col_path)
            item_path.append(item['name'].replace('/', ''))
            bitstreams = get_item_bitstreams(item['uuid']).json()
            for bitstream in bitstreams:
                internal_id = get_internal_id(bitstream['uuid'])[0]
                type_size = get_file_type_size(internal_id)
                path = '/'.join(item_path).replace('//', '/')
                path = remove_caracter_especial('_'.join(path.split()))
                bitstream_dict = {
                    'path': path,
                    'name': remove_caracter_especial('_'.join(bitstream['name'].split())),
                    'internal_id': internal_id,
                    'relative_path': '{}/{}/{}'.format(internal_id[:2],
                                                       internal_id[2:4],
                                                       internal_id[4:6]),
                    'type': type_size[0],
                    'size': type_size[1]
                }
                file_list.append(bitstream_dict)
                print(file_list.__len__())
    return file_list


def list_to_csv(list):
    keys = list[0].keys()
    with open('file_list.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list)


def reorder_files():
    with open('file_list.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            os.makedirs(row['path'], exist_ok=True)
            shutil.copy2('/home/tiagoslg/Documentos/assetstore/{}/{}'.format(row['relative_path'],
                                                                             row['internal_id']),
                         '{}/{}'.format(row['path'], row['name']))

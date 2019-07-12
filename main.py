import requests as r
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime, timezone
import os
from glob import glob
from urllib.parse import unquote as decode_uri
import json

def get_filename(url):
    return url.split('?')[0].split('#')[0].split('/')[-1]

def convert_date(date):
    # ''' Exemplo de data: 'Tue, 02 Apr 2019 07:52:22 GMT'
    return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=timezone.utc).astimezone()

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.now(timezone.utc).astimezone().tzinfo).astimezone()

def get_properties(url):
    props = {
        'name': None,
        'date': None,
        'length': None,
        'url': None
    }

    with r.get(url, stream=True) as c:
        props['url'] = c.url
        props['length'] = int(c.headers['content-length'])
        props['date'] = convert_date(c.headers['last-modified'])
        try:
            props['name'] = re.search('filename=\"?(.+?)(?:\"|;|$)', c.headers['content-disposition']).group(1)
        except (KeyError, AttributeError):
            props['name'] = get_filename(c.url)

    return props

def get_downloadurl(url, search_type=None, search=None, ssl_verify=True):
    """
    Procura e retorna a URL de download direto do programa.

    :param url: URL da página onde será realizada na pesquisa. Caso já seja um link direto, o mesmo será retornado.

    :param search_type: Tipo de pesquisa. As opções disponíveis são select, select_re e find.

    :param search: Um dict cujo conteúdo depende de search_type.

    :returns: URL encontrada, que corresponde ao link de download direto.

    Se search_type for selector, o parâmetro search deve conter a chave selector.\n
    Exemplo: {'selector': 'a.external-link[target=_self]'}

    Se search_type for selector_re, o parâmetro search deve conter as chaves selector, attr e pattern.
    onde attr é o atributo onde será feita a pesquisa e pattern é uma expressão regular para pesquisa do texto do conteúdo da tag.\n
    Exemplo: {'selector': 'a.external-link[target=_self]', 'attr': 'href', 'pattern': 'Receitanet-[0-9]\\\.[0-9][0-9]\\\.exe'}
    
    Se search_type for find, o parâmetro search deve conter os filtros de pesquisa do BeautifulSoup.\n
    Exemplo: {'name': 'a', 'string': '\\nWindows Off-line'}
    """
    with r.get(url, stream=True, verify=ssl_verify) as rs:
        if rs.headers['content-type'].startswith('application'):
            return url

        if not rs.headers['content-type'].startswith('text') or search_type is None or search is None:
            return None
        
        site = bs(rs.content, features='html.parser')

        if search_type == 'selector':
            for s in site.select(search['selector']):
                if s.has_attr('href'):
                    return s['href']
            # return [s['href'] for s in site.select(search) if s.has_attr('href')]
        elif search_type == 'selector_re':
            # m = []
            for result in site.select(search['selector']):
                if search['attr'] in ('text', 'string'):
                    val = result.string
                else:
                    val = result[search['attr']]
                if re.search(search['pattern'], val):
                    return result['href']
                    # m.append(result['href'])
            # return m
        elif search_type == 'find':
            # return [s['href'] for s in site.find_all(**search) if s.has_attr('href')]
            for s in site.find_all(**search):
                if s.has_attr('href'):
                    return s['href']

    return None

def find_update(current_file, update_url):
    update_props = get_properties(update_url)
    if update_props is None:
        raise Exception("URL de atualização não disponível")

    files = sorted(glob(current_file), key=os.path.getmtime, reverse=True)
    if len(files) == 0:
        return {
            'current': None,
            'update': update_props
        }

    current_file_length = os.path.getsize(files[0])
    current_file_date = convert_timestamp_to_date(os.path.getmtime(files[0]))
    if update_props['date'] > current_file_date or (update_props['date'] <= current_file_date and update_props['length'] != current_file_length):
        return {
            'current': {
                'name': files[0],
                'date': current_file_date,
                'length': current_file_length
            },
            'update': update_props
        }
    
    return {
        'current': {
            'name': files[0],
            'date': current_file_date,
            'length': current_file_length
        },
        'update': None
    }

def check_update(name, file, update_page, search_url_type = None, search_url_params = None, ssl_verify=True):
    if name is not None:
        print('Verificando ' + name)
    d_url = get_downloadurl(update_page, search_url_type, search_url_params, ssl_verify)
    d_url = d_url if re.search(r'(?:https?|ftp):\/\/.+', d_url) else update_page + '/' + d_url
    try:
        upd = find_update(file, d_url)
    except Exception as e:
        print('ERRO: ' + str(e))
        return None

    if upd['current'] is None and upd['update'] is None:
        print('Algo de errado não está certo')
        return None

    if upd['current'] is not None:
        print('Programa encontrado: {}, {}, {}'.format(upd['current']['name'], upd['current']['date'].strftime("%d/%m/%Y %H:%M:%S"), upd['current']['length']))
    else:
        print('Programa não encontrado')
    
    if upd['update'] is not None:
        print('Atualização disponível: {}, {}, {}, {}'.format(decode_uri(upd['update']['name']), upd['update']['date'].strftime("%d/%m/%Y %H:%M:%S"), upd['update']['length'], upd['update']['url']))
    elif upd['current'] is not None:
        print('Programa atualizado')

    print()


# ''' MAIN '''
with open('programs.json', 'r') as f:
    updates_to_check = json.load(f)

for uc in updates_to_check['programs']:
    try:
        ssl_verify = uc['ssl_verify']
    except KeyError:
        ssl_verify = True

    check_update(
        uc['name'],
        updates_to_check['root_directory'] + '/' + uc['file'],
        uc['url'],
        uc['search_type'],
        uc['search_params'],
        ssl_verify
    )


print('Verificando LibreOffice')
upd_page = get_downloadurl(
    'https://tdf.c3sl.ufpr.br/libreoffice/stable/',
    'selector_re',
    {
        'selector': 'tr:nth-last-child(2) > td:nth-child(2) > a',
        'attr': 'href',
        'pattern': r'([0-9]?)\.([0-9]?)\.([0-9]?)'
    }
)
if upd_page is None:
    print('URL de atualização não disponível')
else:
    upd_page = "https://tdf.c3sl.ufpr.br/libreoffice/stable/" + upd_page + "win/x86"
    check_update(
        None,
        updates_to_check['root_directory'] + '/LibreOffice/LibreOffice_*_Win_x86.msi',
        upd_page,
        'selector_re',
        {
            'selector': 'a',
            'attr': 'href',
            'pattern': r'Win_x86.msi$'
        }
    )

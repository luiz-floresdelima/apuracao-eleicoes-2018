import requests
import xml.etree.ElementTree as ET
import time
import zipfile
import io

def pegar_ultimosarq_presi():
    url = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/295/config/br/br-e000295-i.xml"
    r = requests.get(url)
    tree = ET.fromstring(r.content)

    arquivos_fixos_presi = []
    arquivos_fixos_geral = []
    arquivos_variaveis_presi = []
    arquivos_variaveis_geral = []
    arquivos_outros = []

    todos_arquivos = []

    for i in tree:
        if "-f.zip" in i.attrib['nome']:
            if "br-e000295-" in i.attrib['nome']:
                arquivos_fixos_geral.append(i.attrib['nome'])
            elif "br-c0001-e000295-" in i.attrib['nome']:
                arquivos_fixos_presi.append(i.attrib['nome'])
        elif "-v.zip" in i.attrib['nome']:
            if "br-e000295-" in i.attrib['nome']:
                arquivos_variaveis_geral.append(i.attrib['nome'])
            elif "br-c0001-e000295-" in i.attrib['nome']:
                arquivos_variaveis_presi.append(i.attrib['nome'])
        else:
            arquivos_outros.append(i.attrib['nome'])

    arquivos_fixos_presi = sorted(arquivos_fixos_presi)
    arquivos_fixos_geral = sorted(arquivos_fixos_geral)
    arquivos_variaveis_presi = sorted(arquivos_variaveis_presi)
    arquivos_variaveis_geral = sorted(arquivos_variaveis_geral)
    arquivos_outros = sorted(arquivos_outros)

    todos_arquivos.append(arquivos_fixos_presi[-1])
    todos_arquivos.append(arquivos_fixos_geral[-1])
    todos_arquivos.append(arquivos_variaveis_presi[-1])
    todos_arquivos.append(arquivos_variaveis_geral[-1])
    #todos_arquivos += arquivos_outros
    return todos_arquivos

def total_apuracao_presi():
    lista = pegar_ultimosarq_presi()
    for i in lista:
        if "br-c0001-e000295-" in i:
            if "-f.zip" in i:
                url_fixo = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/295/distribuicao/br/" + i
                x = i[:-3] + "xml"
            elif "-v.zip" in i:
                url_vari = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/295/distribuicao/br/" + i
                y = i[:-3] + "xml"

    r1 = requests.get(url_fixo)
    r2 = requests.get(url_vari)

    file1 = zipfile.ZipFile(io.BytesIO(r1.content))
    file2 = zipfile.ZipFile(io.BytesIO(r2.content))

    tree1 = ET.fromstring(file1.read(x))
    tree2 = ET.fromstring(file2.read(y))

    if int(tree1[0].attrib['eleitorado']) != 0:
        porcentagem_apuracao = (100 * float(tree2[0].attrib['eleitoradoApurado'])) / float(tree1[0].attrib['eleitorado'])
        porcentagem_apuracao = round(porcentagem_apuracao, 1)
    else:
        porcentagem_apuracao = 0

    return porcentagem_apuracao

def total_apuracao_gover():
    estados = {'Distrito Federal': 'df'}

    apur_estados = {}

    for x in estados:
        url_vari_estado = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/297/config/" + estados[x] + "/" + estados[x] + "-e000297-i.xml"
        r = requests.get(url_vari_estado)
        tree = ET.fromstring(r.content)

        arquivos_fixos_presi = []
        arquivos_fixos_geral = []
        arquivos_variaveis_presi = []
        arquivos_variaveis_geral = []
        arquivos_outros = []

        todos_arquivos = []

        for i in tree:
            if "-f.zip" in i.attrib['nome']:
                if (estados[x] + "-e000297-") in i.attrib['nome']:
                    arquivos_fixos_geral.append(i.attrib['nome'])
                elif (estados[x] + "-c0003-e000297-") in i.attrib['nome']:
                    arquivos_fixos_presi.append(i.attrib['nome'])
            elif "-v.zip" in i.attrib['nome']:
                if (estados[x] + "-e000297-") in i.attrib['nome']:
                    arquivos_variaveis_geral.append(i.attrib['nome'])
                elif (estados[x] + "-c0003-e000297-") in i.attrib['nome']:
                    arquivos_variaveis_presi.append(i.attrib['nome'])
            else:
                arquivos_outros.append(i.attrib['nome'])

        arquivos_fixos_presi = sorted(arquivos_fixos_presi)
        arquivos_fixos_geral = sorted(arquivos_fixos_geral)
        arquivos_variaveis_presi = sorted(arquivos_variaveis_presi)
        arquivos_variaveis_geral = sorted(arquivos_variaveis_geral)
        arquivos_outros = sorted(arquivos_outros)

        todos_arquivos.append(arquivos_fixos_presi[-1])
        todos_arquivos.append(arquivos_fixos_geral[-1])
        todos_arquivos.append(arquivos_variaveis_presi[-1])
        todos_arquivos.append(arquivos_variaveis_geral[-1])

        lista = todos_arquivos
        for i in lista:
            if ( estados[x] + "-c0003-e000297-") in i:
                if "-f.zip" in i:
                    url_fixo = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/297/distribuicao/"+ estados[x] + "/" + i
                    r = i[:-3] + "xml"
                elif "-v.zip" in i:
                    url_vari = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/297/distribuicao/" + estados[x] + "/" + i
                    s = i[:-3] + "xml"

        r1 = requests.get(url_fixo)
        r2 = requests.get(url_vari)

        file1 = zipfile.ZipFile(io.BytesIO(r1.content))
        file2 = zipfile.ZipFile(io.BytesIO(r2.content))

        tree1 = ET.fromstring(file1.read(r))
        tree2 = ET.fromstring(file2.read(s))

        if int(tree1[0][0].attrib['eleitorado']) != 0:
            porcentagem_apuracao = (100 * float(tree2[0].attrib['eleitoradoApurado'])) / float(tree1[0][0].attrib['eleitorado'])
            porcentagem_apuracao = round(porcentagem_apuracao, 1)
        else:
            porcentagem_apuracao = 0

        apur_estados[x] = porcentagem_apuracao

    return apur_estados

def classificacao_gover_estado():
    #estados = ['ac','al','ap','am','ba','ce','df','es','go','ma','mt','ms','mg','pa','pb','pr','pe','pi','rj','rn','rs','ro','rr','sc','sp','se','to']

    estados = {'Distrito Federal': 'df'}

    top_3_estados = {}
    top_3_estados_list = []

    for x in estados:
        url_vari_estado = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/297/config/" + estados[x] + "/" + estados[x] + "-e000297-i.xml"
        r = requests.get(url_vari_estado)
        tree = ET.fromstring(r.content)

        arquivos_fixos_presi = []
        arquivos_fixos_geral = []
        arquivos_variaveis_presi = []
        arquivos_variaveis_geral = []
        arquivos_outros = []

        todos_arquivos = []

        for i in tree:
            if "-f.zip" in i.attrib['nome']:
                if (estados[x] + "-e000297-") in i.attrib['nome']:
                    arquivos_fixos_geral.append(i.attrib['nome'])
                elif (estados[x] + "-c0003-e000297-") in i.attrib['nome']:
                    arquivos_fixos_presi.append(i.attrib['nome'])
            elif "-v.zip" in i.attrib['nome']:
                if (estados[x] + "-e000297-") in i.attrib['nome']:
                    arquivos_variaveis_geral.append(i.attrib['nome'])
                elif (estados[x] + "-c0003-e000297-") in i.attrib['nome']:
                    arquivos_variaveis_presi.append(i.attrib['nome'])
            else:
                arquivos_outros.append(i.attrib['nome'])

        arquivos_fixos_presi = sorted(arquivos_fixos_presi)
        arquivos_fixos_geral = sorted(arquivos_fixos_geral)
        arquivos_variaveis_presi = sorted(arquivos_variaveis_presi)
        arquivos_variaveis_geral = sorted(arquivos_variaveis_geral)
        arquivos_outros = sorted(arquivos_outros)

        todos_arquivos.append(arquivos_fixos_presi[-1])
        todos_arquivos.append(arquivos_fixos_geral[-1])
        todos_arquivos.append(arquivos_variaveis_presi[-1])
        todos_arquivos.append(arquivos_variaveis_geral[-1])

        lista = todos_arquivos
        for i in lista:
            if ( estados[x] + "-c0003-e000297-") in i:
                if "-f.zip" in i:
                    url_fixo = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/297/distribuicao/"+ estados[x] + "/" + i
                    r = i[:-3] + "xml"
                elif "-v.zip" in i:
                    url_vari = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/297/distribuicao/" + estados[x] + "/" + i
                    s = i[:-3] + "xml"

        r1 = requests.get(url_fixo)
        r2 = requests.get(url_vari)

        file1 = zipfile.ZipFile(io.BytesIO(r1.content))
        file2 = zipfile.ZipFile(io.BytesIO(r2.content))

        tree1 = ET.fromstring(file1.read(r))
        tree2 = ET.fromstring(file2.read(s))

        lista_presi = []

        for i in tree1[1]:
            presidentes = {}
            presidentes['cod_col'] = i.attrib['numero']
            presidentes['partido'] = i.attrib['composicao']
            for j in i:
                presidentes['numero_partido'] = j.attrib['numero']
                for k in j:
                    presidentes['nome'] = k.attrib['nomeUrna']
                    presidentes['cod_foto'] = k.attrib['seqCand']
                    for l in k:
                        presidentes['vice'] = l.attrib['nomeUrna']
                        for m in tree2[0]:
                            if m.tag == "VotoColigacao":
                                if m.attrib['numeroColigacao'] == presidentes['cod_col']:
                                    presidentes['total_nominais'] = m.attrib['totalVotosNominais']
                                    presidentes['total_legenda'] = m.attrib['totalVotosLegenda']
                            if m.tag == "VotoCandidato":
                                if m.attrib['numeroCandidato'] == presidentes['numero_partido']:
                                    presidentes['classificacao'] = m.attrib['classificacao']
                                    presidentes['total_votos'] = m.attrib['totalVotos']
                                    if int(tree2[0].attrib['eleitoradoApurado']) != 0:
                                        presidentes['porcento_votos'] = str(round((100 * float(presidentes['total_votos'])) / (float(tree2[0].attrib['votosTotalizados']) - float(tree2[0].attrib['votosEmBranco']) - float(tree2[0].attrib['votosNulos']) - float(tree2[0].attrib['votosAnulados'])),2))
                                    else:
                                        presidentes['porcento_votos'] = "0"
                        lista_presi.append(presidentes)

        lista_presi = sorted(lista_presi, key=lambda k: int(k['classificacao']))
        top_3_estados[x] = lista_presi[0:3]
        for i in lista_presi[0:3]:
            top_3_estados_list.append(i)

    return top_3_estados_list

def classificacao_presi_geral():
    lista = pegar_ultimosarq_presi()
    for i in lista:
        if "br-c0001-e000295-" in i:
            if "-f.zip" in i:
                url_fixo = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/295/distribuicao/br/" + i
                x = i[:-3] + "xml"
            elif "-v.zip" in i:
                url_vari = "http://interessados.divulgacao.tse.jus.br/2018/divulgacao/oficial/295/distribuicao/br/" + i
                y = i[:-3] + "xml"

    r1 = requests.get(url_fixo)
    r2 = requests.get(url_vari)

    file1 = zipfile.ZipFile(io.BytesIO(r1.content))
    file2 = zipfile.ZipFile(io.BytesIO(r2.content))

    tree1 = ET.fromstring(file1.read(x))
    tree2 = ET.fromstring(file2.read(y))

    lista_presi = []

    for i in tree1[1]:
        presidentes = {}
        presidentes['cod_col'] = i.attrib['numero']
        presidentes['partido'] = i.attrib['composicao']
        for j in i:
            presidentes['numero_partido'] = j.attrib['numero']
            for k in j:
                presidentes['nome'] = k.attrib['nomeUrna']
                presidentes['cod_foto'] = k.attrib['seqCand']
                for l in k:
                    presidentes['vice'] = l.attrib['nomeUrna']
                    for m in tree2[0]:
                        if m.tag == "VotoColigacao":
                            if m.attrib['numeroColigacao'] == presidentes['cod_col']:
                                presidentes['total_nominais'] = m.attrib['totalVotosNominais']
                                presidentes['total_legenda'] = m.attrib['totalVotosLegenda']
                        if m.tag == "VotoCandidato":
                            if m.attrib['numeroCandidato'] == presidentes['numero_partido']:
                                presidentes['classificacao'] = m.attrib['classificacao']
                                presidentes['total_votos'] = m.attrib['totalVotos']
                                if int(tree2[0].attrib['eleitoradoApurado']) != 0:
                                    presidentes['porcento_votos'] = str(round((100 * float(presidentes['total_votos'])) / (float(tree2[0].attrib['votosTotalizados']) - float(tree2[0].attrib['votosEmBranco']) - float(tree2[0].attrib['votosNulos']) - float(tree2[0].attrib['votosAnulados'])),2))
                                else:
                                    presidentes['porcento_votos'] = "0"
                    lista_presi.append(presidentes)

    lista_presi = sorted(lista_presi, key=lambda k: int(k['classificacao']))

    return lista_presi[0:3]

# -*- coding: utf-8 -*-
"""
lexicon_perea.py — comparanda LOKONO de Perea y Alonso 1942 (Fraseario).

GENERADO por `curiana_sim/minar_perea.py`. No se edita a mano.

Fase 1 de D11 (#39): rebalancear la comparanda hacia el eje lokono-taíno.
Propuesta completa y método en `6-fusion/lokono_perea_1942.yaml`.

⚠️  ESTE MÓDULO NO SE IMPORTA DESDE `curiana_lexicon`, Y ES A PROPÓSITO.

    `palabras_activas()` devuelve TODAS las claves de VOCABULARIO_BASE sin
    filtrar por `fuente`, y `score_linguistico()` cuenta como arahuaco
    cualquier token que esté ahí. `detectar_uso_vocabulario()` además casa
    por SUBCADENA. Meter estas voces en VOCABULARIO_BASE movería la métrica
    insignia del proyecto y rompería la comparabilidad con los runs ya
    publicados — el mismo motivo por el que D3 dejó `normalizar_por_dialecto`
    sin cablear. Y sería peor que en abstracto: entre estas raíces hay
    homógrafos del español (`dia`, `uma`, `sica`, `iri`, `baha`, `adi`) que
    con el match por subcadena casarían con «día», «estudia», «medía»...

    Estas voces son COMPARANDA: sirven para comparar de qué lengua se
    reconstruye el caquetío. No son vocabulario que los agentes hablen.

Etiqueta: `atestiguado` en LOKONO — no en caquetío. Cada acepción trae la
página impresa de Perea y, cuando el ejemplo lo permitía, el capítulo y
versículo de los Hechos de los Apóstoles en la versión de Schultz (1802),
que es el texto que Perea vació. Las citas abreviadas del tipo «-24» (mismo
capítulo, otro versículo) se descartan: sin capítulo no son ancla.
"""

OBRA = "perea-alonso-1942"
LENGUA = "lokono"
ESTRATO = "lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje"


# forma -> {acepciones: [{glosa, pagina, hechos?, atestaciones}], total}
COMPARANDA_LOKONO: dict[str, dict] = {
    'dia': {"total": 28, "acepciones": [
        {"glosa": 'decir', "pagina": 280, "atestaciones": 9},
        {"glosa": 'palabra', "pagina": 75, "hechos": '2-22', "atestaciones": 7},
        {"glosa": 'lengua, idioma', "pagina": 57, "hechos": '2-4', "atestaciones": 5},
        {"glosa": 'voz', "pagina": 104, "hechos": '7-31', "atestaciones": 2},
        {"glosa": 'conferir', "pagina": 262, "hechos": '4-15', "atestaciones": 1},
    ]},
    'haca': {"total": 22, "acepciones": [
        {"glosa": 'testificar', "pagina": 468, "hechos": '1-8', "atestaciones": 6},
        {"glosa": 'hablar', "pagina": 342, "hechos": '1-1', "atestaciones": 5},
        {"glosa": 'anunciar', "pagina": 234, "hechos": '8-4', "atestaciones": 2},
        {"glosa": 'despedazar', "pagina": 300, "hechos": '23-10', "atestaciones": 2},
        {"glosa": 'disputar', "pagina": 303, "hechos": '17-2', "atestaciones": 2},
    ]},
    'makua': {"total": 22, "acepciones": [
        {"glosa": 'todo', "pagina": 215, "hechos": '2-4', "atestaciones": 16},
        {"glosa": 'cada uno', "pagina": 211, "hechos": '2-3', "atestaciones": 2},
        {"glosa": 'público', "pagina": 125, "hechos": '16-37', "atestaciones": 2},
        {"glosa": 'cualquiera', "pagina": 218, "hechos": '3-23', "atestaciones": 1},
    ]},
    'dumma': {"total": 17, "acepciones": [
        {"glosa": 'porque', "pagina": 531, "hechos": '4-3', "atestaciones": 12},
        {"glosa": 'causar', "pagina": 253, "hechos": '10-21', "atestaciones": 3},
        {"glosa": 'fe', "pagina": 45, "hechos": '3-16', "atestaciones": 1},
        {"glosa": 'modo', "pagina": 322, "hechos": '4-9', "atestaciones": 1},
    ]},
    'ditti': {"total": 16, "acepciones": [
        {"glosa": 'hijo', "pagina": 51, "hechos": '1-13', "atestaciones": 10},
        {"glosa": 'entender', "pagina": 313, "hechos": '7-25', "atestaciones": 2},
        {"glosa": 'afirmar', "pagina": 227, "hechos": '9-22', "atestaciones": 1},
        {"glosa": 'concernir', "pagina": 260, "hechos": '28-23', "atestaciones": 1},
        {"glosa": 'conocer', "pagina": 265, "hechos": '3-10', "atestaciones": 1},
    ]},
    'iyuhu': {"total": 16, "acepciones": [
        {"glosa": 'multitud', "pagina": 69, "hechos": '2-6', "atestaciones": 8},
        {"glosa": 'gente', "pagina": 47, "hechos": '4-25', "atestaciones": 3},
        {"glosa": 'número', "pagina": 72, "hechos": '1-15', "atestaciones": 3},
        {"glosa": 'conjurar', "pagina": 264, "hechos": '23-13', "atestaciones": 1},
        {"glosa": 'aumentar', "pagina": 246, "hechos": '16-5', "atestaciones": 1},
    ]},
    'sica': {"total": 16, "acepciones": [
        {"glosa": 'servir', "pagina": 462, "hechos": '7-6', "atestaciones": 4},
        {"glosa": 'obedecer', "pagina": 398, "hechos": '4-19', "atestaciones": 3},
        {"glosa": 'pecar', "pagina": 411, "hechos": '5-31', "atestaciones": 3},
        {"glosa": 'piadoso, pío', "pagina": 123, "hechos": '8-2', "atestaciones": 2},
        {"glosa": 'asentir', "pagina": 243, "hechos": '28-24', "atestaciones": 1},
    ]},
    'uma': {"total": 15, "acepciones": [
        {"glosa": 'con', "pagina": 502, "hechos": '1-14', "atestaciones": 13},
        {"glosa": 'acompañar', "pagina": 222, "hechos": '9-30', "atestaciones": 2},
    ]},
    'iri': {"total": 14, "acepciones": [
        {"glosa": 'nombrar', "pagina": 395, "hechos": '2-38', "atestaciones": 14},
    ]},
    'tatta': {"total": 13, "acepciones": [
        {"glosa": 'mandar', "pagina": 381, "hechos": '4-15', "atestaciones": 2},
        {"glosa": 'virtud, fuerza, poder', "pagina": 102, "hechos": '1-8', "atestaciones": 2},
        {"glosa": 'voto, promesa', "pagina": 104, "hechos": '21-23', "atestaciones": 2},
        {"glosa": 'afirmar', "pagina": 228, "hechos": '3-7', "atestaciones": 1},
        {"glosa": 'amenazar', "pagina": 232, "hechos": '9-1', "atestaciones": 1},
    ]},
    'uria': {"total": 12, "acepciones": [
        {"glosa": 'de', "pagina": 505, "hechos": '2-10', "atestaciones": 5},
        {"glosa": 'apartar', "pagina": 238, "hechos": '7-39', "atestaciones": 3},
        {"glosa": '\'uera', "pagina": 515, "hechos": '7-58', "atestaciones": 2},
        {"glosa": 'entre', "pagina": 514, "hechos": '1-22', "atestaciones": 2},
    ]},  # homografo de una clave del lexicon
    'hidda': {"total": 11, "acepciones": [
        {"glosa": 'así', "pagina": 497, "hechos": '1-11', "atestaciones": 9},
        {"glosa": 'tal', "pagina": 128, "hechos": '1-19', "atestaciones": 1},
    ]},
    'huda': {"total": 11, "acepciones": [
        {"glosa": 'morir', "pagina": 390, "hechos": '3-15', "atestaciones": 7},
        {"glosa": 'resucitar', "pagina": 440, "hechos": '1-22', "atestaciones": 3},
        {"glosa": 'espirar', "pagina": 325, "hechos": '12-23', "atestaciones": 1},
    ]},
    'llua': {"total": 11, "acepciones": [
        {"glosa": 'corazón', "pagina": 23, "hechos": '2-26', "atestaciones": 9},
        {"glosa": 'alma; espíritu, ánimo, corazón', "pagina": 8, "hechos": '2-27', "atestaciones": 2},
    ]},
    'abbu': {"total": 10, "acepciones": [
        {"glosa": 'por', "pagina": 528, "hechos": '1-2', "atestaciones": 6},
        {"glosa": 'con', "pagina": 501, "atestaciones": 4},
    ]},
    'adi': {"total": 10, "acepciones": [
        {"glosa": 'sobre', "pagina": 536, "hechos": '2-3', "atestaciones": 8},
        {"glosa": 'delante', "pagina": 507, "hechos": '20-16', "atestaciones": 1},
        {"glosa": 'sobrepujar', "pagina": 463, "hechos": '26-13', "atestaciones": 1},
    ]},
    'baha': {"total": 10, "acepciones": [
        {"glosa": 'caso', "pagina": 491, "hechos": '2-7', "atestaciones": 9},
        {"glosa": 'quizás', "pagina": 533, "atestaciones": 1},
    ]},
    'baddia': {"total": 8, "acepciones": [
        {"glosa": 'y', "pagina": 538, "hechos": '1-7', "atestaciones": 4},
        {"glosa": 'aun', "pagina": 498, "hechos": '5-16', "atestaciones": 2},
        {"glosa": 'asimismo', "pagina": 498, "hechos": '11-30', "atestaciones": 1},
        {"glosa": 'también', "pagina": 537, "hechos": '6-7', "atestaciones": 1},
    ]},
    'cuttu': {"total": 8, "acepciones": [
        {"glosa": 'ayunar', "pagina": 247, "hechos": '10-30', "atestaciones": 4},
        {"glosa": 'comer', "pagina": 258, "hechos": '10-10', "atestaciones": 2},
        {"glosa": 'gustar', "pagina": 339, "hechos": '20-11', "atestaciones": 1},
        {"glosa": 'menester', "pagina": 386, "hechos": '3-21', "atestaciones": 1},
    ]},
    'hamma': {"total": 8, "acepciones": [
        {"glosa": 'por qué ?', "pagina": 530, "hechos": '3-12', "atestaciones": 7},
        {"glosa": 'temer', "pagina": 466, "hechos": '5-5', "atestaciones": 1},
    ]},
    'mùn': {"total": 8, "acepciones": [
        {"glosa": 'a', "pagina": None, "hechos": '1-3', "atestaciones": 3},
        {"glosa": 'para', "pagina": 527, "hechos": '1-25', "atestaciones": 3},
        {"glosa": 'en', "pagina": 511, "hechos": '1-8', "atestaciones": 1},
        {"glosa": 'haber', "pagina": 339, "hechos": '2-45', "atestaciones": 1},
    ]},
    'sikua': {"total": 8, "acepciones": [
        {"glosa": 'casa', "pagina": 19, "hechos": '2-2', "atestaciones": 8},
    ]},
    'ya-luccu': {"total": 8, "acepciones": [
        {"glosa": 'contra', "pagina": 503, "hechos": '4-14', "atestaciones": 8},
    ]},
    'boa': {"total": 7, "acepciones": [
        {"glosa": 'crimen, delito', "pagina": 26, "hechos": '25-5', "atestaciones": 2},
        {"glosa": 'invocar', "pagina": 361, "hechos": '2-21', "atestaciones": 2},
        {"glosa": 'malo', "pagina": 117, "hechos": '17-5', "atestaciones": 2},
        {"glosa": 'mal', "pagina": 519, "hechos": '24-20', "atestaciones": 1},
    ]},
    'ddiki': {"total": 7, "acepciones": [
        {"glosa": 'ver', "pagina": 479, "hechos": '2-17', "atestaciones": 4},
        {"glosa": 'mirar', "pagina": 389, "hechos": '1-11', "atestaciones": 2},
        {"glosa": 'postrero, último', "pagina": 124, "hechos": '2-17', "atestaciones": 1},
    ]},
    'halli-kebbe': {"total": 7, "acepciones": [
        {"glosa": 'gozar', "pagina": 336, "hechos": '2-28', "atestaciones": 3},
        {"glosa": 'alegrar', "pagina": 231, "hechos": '2-26', "atestaciones": 1},
        {"glosa": 'confiar', "pagina": 262, "hechos": '18-26', "atestaciones": 1},
        {"glosa": 'consentir', "pagina": 266, "hechos": '8-1', "atestaciones": 1},
        {"glosa": 'dichoso', "pagina": 112, "hechos": '26-2', "atestaciones": 1},
    ]},
    'hitte': {"total": 7, "acepciones": [
        {"glosa": 'más', "pagina": 520, "hechos": '5-14', "atestaciones": 4},
        {"glosa": 'mucho', "pagina": 322, "hechos": '6-7', "atestaciones": 2},
        {"glosa": 'erseverar', "pagina": 415, "hechos": '12-16', "atestaciones": 1},
    ]},
    'ikisi': {"total": 7, "acepciones": [
        {"glosa": 'escoger', "pagina": 321, "hechos": '8-24', "atestaciones": 3},
        {"glosa": 'acordar', "pagina": 224, "hechos": '21-25', "atestaciones": 1},
        {"glosa": 'contar, enumerar', "pagina": 269, "hechos": '8-33', "atestaciones": 1},
        {"glosa": 'determinar', "pagina": 301, "hechos": '2-23', "atestaciones": 1},
        {"glosa": 'prometer', "pagina": 428, "hechos": '13-23', "atestaciones": 1},
    ]},
    'isibu': {"total": 7, "acepciones": [
        {"glosa": 'puerta', "pagina": 85, "hechos": '3-2', "atestaciones": 3},
        {"glosa": 'cara, faz, rostro', "pagina": 17, "hechos": '6-15', "atestaciones": 2},
        {"glosa": 'rostro', "pagina": 88, "hechos": '6-15', "atestaciones": 2},
    ]},
    'malli-cutta': {"total": 7, "acepciones": [
        {"glosa": 'enseñar', "pagina": 311, "hechos": '4-2', "atestaciones": 4},
        {"glosa": 'doctrina', "pagina": 38, "hechos": '2-42', "atestaciones": 2},
        {"glosa": 'instruír', "pagina": 360, "hechos": '18-25', "atestaciones": 1},
    ]},
    'muniru': {"total": 7, "acepciones": [
        {"glosa": 'hasta', "pagina": 516, "hechos": '1-2', "atestaciones": 7},
    ]},
    'wabu-ruccu': {"total": 7, "acepciones": [
        {"glosa": 'camino', "pagina": 16, "hechos": '10-9', "atestaciones": 7},
    ]},
    'wunabu': {"total": 7, "acepciones": [
        {"glosa": 'tierra, ( la, el mundo :', "pagina": 95, "hechos": '1-8', "atestaciones": 4},
        {"glosa": 'mundo, tierra, siglo, humanidad', "pagina": 70, "hechos": '17-24', "atestaciones": 2},
        {"glosa": 'tierra, suelo', "pagina": 96, "hechos": '9-4', "atestaciones": 1},
    ]},
    'bara': {"total": 6, "acepciones": [
        {"glosa": 'mar', "pagina": 65, "hechos": '7-36', "atestaciones": 6},
    ]},  # homografo de una clave del lexicon
    'bura': {"total": 6, "acepciones": [
        {"glosa": 'padre', "pagina": 123, "hechos": '2-33', "atestaciones": 5},
        {"glosa": 'patria', "pagina": 78, "hechos": '28-17', "atestaciones": 1},
    ]},
    'ibikiddu-lli-a': {"total": 6, "acepciones": [
        {"glosa": 'mancebo', "pagina": 63, "hechos": '2-17', "atestaciones": 6},
    ]},
    'manswa': {"total": 6, "acepciones": [
        {"glosa": 'maravilla', "pagina": 66, "hechos": '2-11', "atestaciones": 2},
        {"glosa": 'milagro', "pagina": 67, "hechos": '5-12', "atestaciones": 2},
        {"glosa": 'grande', "pagina": 114, "hechos": '4-33', "atestaciones": 1},
        {"glosa": 'prodigio', "pagina": 83, "hechos": '2-19', "atestaciones": 1},
    ]},
    'nsi': {"total": 6, "acepciones": [
        {"glosa": 'discipulo', "pagina": 36, "hechos": '6-1', "atestaciones": 3},
        {"glosa": 'amar', "pagina": 232, "hechos": '15-25', "atestaciones": 1},
        {"glosa": 'amigo', "pagina": 8, "hechos": '19-31', "atestaciones": 1},
        {"glosa": 'voluntad', "pagina": 102, "hechos": '13-36', "atestaciones": 1},
    ]},
    'putti': {"total": 6, "acepciones": [
        {"glosa": 'salir', "pagina": 448, "hechos": '4-15', "atestaciones": 6},
    ]},
    'rubu-ùn': {"total": 6, "acepciones": [
        {"glosa": 'sólo, solamente', "pagina": 536, "hechos": '19-26', "atestaciones": 4},
        {"glosa": 'sino', "pagina": 535, "hechos": '10-41', "atestaciones": 2},
    ]},
    'sacca-bbu': {"total": 6, "acepciones": [
        {"glosa": 'día', "pagina": None, "hechos": '1-2', "atestaciones": 3},
        {"glosa": 'tiempo', "pagina": 94, "hechos": '1-7', "atestaciones": 3},
    ]},
    'waria': {"total": 6, "acepciones": [
        {"glosa": 'desde', "pagina": 508, "hechos": '1-11', "atestaciones": 6},
    ]},
    'benna': {"total": 5, "acepciones": [
        {"glosa": 'cuando', "pagina": 504, "hechos": '5-23', "atestaciones": 5},
    ]},
    'ccabbu': {"total": 5, "acepciones": [
        {"glosa": 'mano', "pagina": 63, "hechos": '3-7', "atestaciones": 5},
    ]},
    'cuya': {"total": 5, "acepciones": [
        {"glosa": 'rogar', "pagina": 442, "hechos": '10-48', "atestaciones": 3},
        {"glosa": 'demandar', "pagina": 294, "hechos": '9-2', "atestaciones": 2},
    ]},
    'cuya-bua': {"total": 5, "acepciones": [
        {"glosa": 'orar', "pagina": 404, "hechos": '1-14', "atestaciones": 3},
        {"glosa": 'adorar', "pagina": 227, "hechos": '8-27', "atestaciones": 2},
    ]},
    'ipil': {"total": 5, "acepciones": [
        {"glosa": 'príncipe ; [ cf. n : pilli ]', "pagina": 82, "hechos": '3-17', "atestaciones": 4},
        {"glosa": 'pontífice', "pagina": 81, "hechos": '5-24', "atestaciones": 1},
    ]},
    'kkürkùa': {"total": 5, "acepciones": [
        {"glosa": 'linaje', "pagina": 59, "hechos": '7-13', "atestaciones": 2},
        {"glosa": 'nación, pueblo, familia', "pagina": 70, "hechos": '2-5', "atestaciones": 1},
        {"glosa": 'simiente', "pagina": 16, "hechos": '3-25', "atestaciones": 1},
        {"glosa": 'tribu', "pagina": 98, "hechos": '13-21', "atestaciones": 1},
    ]},
    'siki': {"total": 5, "acepciones": [
        {"glosa": 'dar', "pagina": 278, "hechos": '2-4', "atestaciones": 2},
        {"glosa": 'entregar', "pagina": 317, "hechos": '3-13', "atestaciones": 2},
        {"glosa": 'exponer', "pagina": 332, "hechos": '15-26', "atestaciones": 1},
    ]},
    'tti': {"total": 5, "acepciones": [
        {"glosa": 'que', "pagina": 199, "hechos": '2-7', "atestaciones": 4},
        {"glosa": 'beber', "pagina": 250, "hechos": '9-9', "atestaciones": 1},
    ]},
    'tuhu': {"total": 5, "acepciones": [
        {"glosa": 'aquel, aquella, aquello, aquellos, aquellas', "pagina": 197, "hechos": '1-15', "atestaciones": 2},
        {"glosa": 'ello, lo', "pagina": 187, "hechos": '4-24', "atestaciones": 2},
        {"glosa": 'éste , ésta, esto, éstos, éstas', "pagina": 148, "hechos": '1-5', "atestaciones": 1},
    ]},
    'usa': {"total": 5, "acepciones": [
        {"glosa": 'arremeter', "pagina": 241, "hechos": '6-12', "atestaciones": 1},
        {"glosa": 'austro', "pagina": 12, "hechos": '27-13', "atestaciones": 1},
        {"glosa": 'comenzar', "pagina": 257, "hechos": '2-4', "atestaciones": 1},
        {"glosa": 'completar', "pagina": 259, "hechos": '3-16', "atestaciones": 1},
        {"glosa": 'tentar, probar', "pagina": 468, "hechos": '19-13', "atestaciones": 1},
    ]},
    'wiyua': {"total": 5, "acepciones": [
        {"glosa": 'año', "pagina": 10, "hechos": '4-22', "atestaciones": 5},
    ]},
    'abba-waria': {"total": 4, "acepciones": [
        {"glosa": 'extranjero', "pagina": 44, "hechos": '2-10', "atestaciones": 4},
    ]},
    'abbu-coa': {"total": 4, "acepciones": [
        {"glosa": 'juntar', "pagina": 364, "hechos": '1-6', "atestaciones": 2},
        {"glosa": 'unánime', "pagina": 130, "hechos": '1-14', "atestaciones": 2},
    ]},
    'adi-acu': {"total": 4, "acepciones": [
        {"glosa": 'encima', "pagina": 513, "hechos": '6-6', "atestaciones": 4},
    ]},
    'biama-cutti-hi': {"total": 4, "acepciones": [
        {"glosa": 'doce', "pagina": 112, "hechos": '6-2', "atestaciones": 4},
    ]},
    'bulle': {"total": 4, "acepciones": [
        {"glosa": 'echar', "pagina": 306, "hechos": '13-50', "atestaciones": 2},
        {"glosa": 'alijar', "pagina": 231, "hechos": '27-18', "atestaciones": 1},
        {"glosa": 'aliviar', "pagina": 232, "hechos": '27-38', "atestaciones": 1},
    ]},
    'catti': {"total": 4, "acepciones": [
        {"glosa": 'mes', "pagina": 66, "hechos": '7-20', "atestaciones": 3},
        {"glosa": 'luna', "pagina": 60, "hechos": '2-20', "atestaciones": 1},
    ]},
    'cumu': {"total": 4, "acepciones": [
        {"glosa": 'no', "pagina": 524, "hechos": '4-12', "atestaciones": 3},
        {"glosa": 'sin', "pagina": 535, "hechos": '5-26', "atestaciones": 1},
    ]},
    'cun-te': {"total": 4, "acepciones": [
        {"glosa": 'ir', "pagina": 362, "hechos": '5-20', "atestaciones": 4},
    ]},
    'daiya': {"total": 4, "acepciones": [
        {"glosa": 'señor', "pagina": 90, "hechos": '2-20', "atestaciones": 4},
    ]},
    'dannu': {"total": 4, "acepciones": [
        {"glosa": 'hoy', "pagina": 517, "hechos": '19-40', "atestaciones": 4},
    ]},
    'hamma-talli': {"total": 4, "acepciones": [
        {"glosa": 'cosa', "pagina": 25, "hechos": '1-1', "atestaciones": 4},
    ]},
    'ipilli': {"total": 4, "acepciones": [
        {"glosa": 'sumo', "pagina": 128, "hechos": '23-4', "atestaciones": 2},
        {"glosa": 'alto', "pagina": None, "hechos": '7-48', "atestaciones": 1},
        {"glosa": 'prepósito', "pagina": 81, "hechos": '18-8', "atestaciones": 1},
    ]},
    'irei': {"total": 4, "acepciones": [
        {"glosa": 'mujer, esposa', "pagina": 69, "hechos": '5-1', "atestaciones": 4},
    ]},
    'kia': {"total": 4, "acepciones": [
        {"glosa": 'después', "pagina": 508, "hechos": '9-37', "atestaciones": 4},
    ]},
    'kusa': {"total": 4, "acepciones": [
        {"glosa": 'ni', "pagina": 523, "hechos": '2-27', "atestaciones": 2},
        {"glosa": 'o', "pagina": 526, "hechos": '3-12', "atestaciones": 2},
    ]},
    'lesi': {"total": 4, "acepciones": [
        {"glosa": 'leer', "pagina": 369, "hechos": '8-28', "atestaciones": 4},
    ]},
    'meyu': {"total": 4, "acepciones": [
        {"glosa": 'navegar', "pagina": 394, "hechos": '14-26', "atestaciones": 3},
        {"glosa": 'barco, buque, nave, navío', "pagina": 12, "hechos": '20-13', "atestaciones": 1},
    ]},
    'onna': {"total": 4, "acepciones": [
        {"glosa": 'responder', "pagina": 438, "hechos": '3-12', "atestaciones": 2},
        {"glosa": 'tomar', "pagina": 470, "hechos": '5-6', "atestaciones": 2},
    ]},
    'pahia': {"total": 4, "acepciones": [
        {"glosa": 'atónito', "pagina": 108, "hechos": '3-11', "atestaciones": 2},
        {"glosa": 'atontar', "pagina": 245, "hechos": '2-7', "atestaciones": 1},
        {"glosa": 'entontecerse', "pagina": 315, "hechos": '13-41', "atestaciones": 1},
    ]},
    'sa-kebe': {"total": 4, "acepciones": [
        {"glosa": 'santo', "pagina": 126, "hechos": '1-2', "atestaciones": 4},
    ]},
    'seme': {"total": 4, "acepciones": [
        {"glosa": 'mágico, mago', "pagina": 62, "hechos": '8-9', "atestaciones": 2},
        {"glosa": 'exorcizar', "pagina": 332, "hechos": '19-13', "atestaciones": 1},
        {"glosa": 'mosto', "pagina": 67, "hechos": '2-13', "atestaciones": 1},
    ]},
    'statuta': {"total": 4, "acepciones": [
        {"glosa": 'ley', "pagina": 58, "hechos": '6-13', "atestaciones": 2},
        {"glosa": 'decretar', "pagina": 292, "hechos": '17-7', "atestaciones": 1},
        {"glosa": 'ordenar', "pagina": 406, "hechos": '6-14', "atestaciones": 1},
    ]},
    'sucusa': {"total": 4, "acepciones": [
        {"glosa": 'bautizar', "pagina": 248, "hechos": '1-5', "atestaciones": 4},
    ]},
    'tuyucu': {"total": 4, "acepciones": [
        {"glosa": 'anciano', "pagina": 9, "hechos": '4-5', "atestaciones": 4},
    ]},
    'uttiki': {"total": 4, "acepciones": [
        {"glosa": 'hallar', "pagina": 352, "hechos": '5-22', "atestaciones": 3},
        {"glosa": 'evitar', "pagina": 331, "hechos": '27-21', "atestaciones": 1},
    ]},
    'yu-mùn': {"total": 4, "acepciones": [
        {"glosa": 'allí', "pagina": 493, "hechos": '10-18', "atestaciones": 4},
    ]},
    'abbu-mùn': {"total": 3, "acepciones": [
        {"glosa": 'debajo', "pagina": 507, "hechos": '2-5', "atestaciones": 2},
        {"glosa": 'bajo', "pagina": 499, "hechos": '2-5', "atestaciones": 1},
    ]},
    'bien': {"total": 3, "acepciones": [
        {"glosa": 'bien', "pagina": 499, "hechos": '10-33', "atestaciones": 3},
    ]},
    'canna': {"total": 3, "acepciones": [
        {"glosa": 'oír', "pagina": 399, "hechos": '1-4', "atestaciones": 3},
    ]},
    'cui-kitta': {"total": 3, "acepciones": [
        {"glosa": 'arrepentirse', "pagina": 241, "hechos": '2-38', "atestaciones": 3},
    ]},
    'cullu-siba-ttoa': {"total": 3, "acepciones": [
        {"glosa": 'rodilla', "pagina": 88, "hechos": '9-40', "atestaciones": 3},
    ]},
    'cun': {"total": 3, "acepciones": [
        {"glosa": 'nacer', "pagina": 393, "hechos": '7-20', "atestaciones": 3},
    ]},
    'cuyoa': {"total": 3, "acepciones": [
        {"glosa": 'volver', "pagina": 486, "hechos": '5-22', "atestaciones": 3},
    ]},
    'disia': {"total": 3, "acepciones": [
        {"glosa": 'acostumbrar', "pagina": 225, "hechos": '17-2', "atestaciones": 2},
        {"glosa": 'soler', "pagina": 464, "hechos": '16-13', "atestaciones": 1},
    ]},
    'hada-cuttu': {"total": 3, "acepciones": [
        {"glosa": 'informar', "pagina": 359, "hechos": '25-26', "atestaciones": 2},
        {"glosa": 'inquirir', "pagina": 360, "hechos": '12-19', "atestaciones": 1},
    ]},
    'huki': {"total": 3, "acepciones": [
        {"glosa": 'hermano', "pagina": 49, "hechos": '1-13', "atestaciones": 3},
    ]},
    'ibiti': {"total": 3, "acepciones": [
        {"glosa": 'cerca', "pagina": 500, "hechos": '1-12', "atestaciones": 3},
    ]},
    'icca': {"total": 3, "acepciones": [
        {"glosa": 'entonces', "pagina": 513, "hechos": '7-1', "atestaciones": 2},
        {"glosa": 'pero', "pagina": 528, "hechos": '5-25', "atestaciones": 1},
    ]},
    'ikitta': {"total": 3, "acepciones": [
        {"glosa": 'guardar', "pagina": 337, "atestaciones": 2},
        {"glosa": 'honrar', "pagina": 356, "hechos": '18-13', "atestaciones": 1},
    ]},
    'ima': {"total": 3, "acepciones": [
        {"glosa": 'enemigo', "pagina": 39, "hechos": '2-35', "atestaciones": 2},
        {"glosa": 'resentir', "pagina": 437, "hechos": '4-2', "atestaciones": 1},
    ]},
    'iribé': {"total": 3, "acepciones": [
        {"glosa": 'inmundo', "pagina": 117, "hechos": '8-7', "atestaciones": 3},
    ]},
    'iya': {"total": 3, "acepciones": [
        {"glosa": 'espíritu', "pagina": 40, "hechos": '1-2', "atestaciones": 2},
        {"glosa": 'compungirse', "pagina": 260, "hechos": '2-37', "atestaciones": 1},
    ]},
    'iyucana': {"total": 3, "acepciones": [
        {"glosa": 'vender', "pagina": 474, "hechos": '3-45', "atestaciones": 3},
    ]},
    'iyuru': {"total": 3, "acepciones": [
        {"glosa": 'traer', "pagina": 471, "hechos": '4-34', "atestaciones": 3},
    ]},
    'kia-hanna': {"total": 3, "acepciones": [
        {"glosa": 'así', "pagina": 498, "hechos": '3-19', "atestaciones": 3},
    ]},
    'maiyana-ttoa': {"total": 3, "acepciones": [
        {"glosa": 'notorio', "pagina": 120, "hechos": '4-10', "atestaciones": 2},
        {"glosa": 'eferir', "pagina": 435, "hechos": '15-4', "atestaciones": 1},
    ]},
    'malli': {"total": 3, "acepciones": [
        {"glosa": 'encender', "pagina": 308, "hechos": '28-2', "atestaciones": 1},
        {"glosa": 'imposible', "pagina": 116, "hechos": '2-24', "atestaciones": 1},
        {"glosa": 'osar', "pagina": 406, "hechos": '5-13', "atestaciones": 1},
    ]},
    'mulli': {"total": 3, "acepciones": [
        {"glosa": 'aparentar', "pagina": 237, "hechos": '27-30', "atestaciones": 1},
        {"glosa": 'mentir', "pagina": 387, "hechos": '5-3', "atestaciones": 1},
        {"glosa": 'usar', "pagina": 474, "hechos": '7-19', "atestaciones": 1},
    ]},
    'nda': {"total": 3, "acepciones": [
        {"glosa": 'sobrevenir', "pagina": 464, "hechos": '4-1', "atestaciones": 2},
        {"glosa": 'descender, bajar', "pagina": 297, "hechos": '7-15', "atestaciones": 1},
    ]},
    'onaica': {"total": 3, "acepciones": [
        {"glosa": 'tribulación', "pagina": 98, "hechos": '7-10', "atestaciones": 3},
    ]},
    'sa-maria': {"total": 3, "acepciones": [
        {"glosa": 'derecha', "pagina": 28, "hechos": '2-25', "atestaciones": 3},
    ]},
    'sura': {"total": 3, "acepciones": [
        {"glosa": 'sala', "pagina": 82, "hechos": '9-37', "atestaciones": 2},
        {"glosa": 'azotea', "pagina": 12, "hechos": '10-9', "atestaciones": 1},
    ]},
    'ttene-nnua': {"total": 3, "acepciones": [
        {"glosa": 'primero', "pagina": 124, "hechos": '7-12', "atestaciones": 2},
        {"glosa": 'vez', "pagina": 102, "hechos": '7-12', "atestaciones": 1},
    ]},
    'ttiki': {"total": 3, "acepciones": [
        {"glosa": 'concitar', "pagina": 260, "hechos": '13-50', "atestaciones": 1},
        {"glosa": 'incitar', "pagina": 359, "hechos": '14-2', "atestaciones": 1},
        {"glosa": 'sobornar', "pagina": 463, "hechos": '12-20', "atestaciones": 1},
    ]},
    'ttùdda': {"total": 3, "acepciones": [
        {"glosa": 'huir', "pagina": 357, "hechos": '7-29', "atestaciones": 3},
    ]},
    'ñaden': {"total": 3, "acepciones": [
        {"glosa": 'gracia', "pagina": 48, "hechos": '4-33', "atestaciones": 3},
    ]},
    'ùsanu-wai': {"total": 3, "acepciones": [
        {"glosa": 'glorificar', "pagina": 335, "hechos": '3-13', "atestaciones": 3},
    ]},
    'awa': {"total": 2, "acepciones": [
        {"glosa": 'mismo', "pagina": 118, "hechos": '1-11', "atestaciones": 2},
    ]},  # homografo de una clave del lexicon
    'balla': {"total": 2, "acepciones": [
        {"glosa": 'crucificar', "pagina": 276, "hechos": '2-23', "atestaciones": 1},
        {"glosa": 'sonda', "pagina": 92, "hechos": '27-28', "atestaciones": 1},
    ]},
    'balti': {"total": 2, "acepciones": [
        {"glosa": 'sentarse', "pagina": 454, "hechos": '2-2', "atestaciones": 2},
    ]},
    'bbuku': {"total": 2, "acepciones": [
        {"glosa": 'recibir', "pagina": 432, "hechos": '1-8', "atestaciones": 2},
    ]},
    'bbuna': {"total": 2, "acepciones": [
        {"glosa": 'paralítico', "pagina": 77, "hechos": '8-7', "atestaciones": 2},
    ]},
    'bele': {"total": 2, "acepciones": [
        {"glosa": 'cojo', "pagina": 23, "hechos": '3-2', "atestaciones": 1},
        {"glosa": 'fervor', "pagina": 45, "hechos": '18-25', "atestaciones": 1},
    ]},
    'bia': {"total": 2, "acepciones": [
        {"glosa": 'in', "pagina": 515, "hechos": '3-26', "atestaciones": 1},
        {"glosa": 'que', "pagina": 533, "hechos": '1-25', "atestaciones": 1},
    ]},
    'boa-hù-dda': {"total": 2, "acepciones": [
        {"glosa": 'asolar', "pagina": 244, "hechos": '8-3', "atestaciones": 1},
        {"glosa": 'ruina', "pagina": 88, "hechos": '15-16', "atestaciones": 1},
    ]},
    'bulita': {"total": 2, "acepciones": [
        {"glosa": 'scribir', "pagina": 321, "hechos": '1-20', "atestaciones": 2},
    ]},
    'bura-mùn': {"total": 2, "acepciones": [
        {"glosa": 'antes', "pagina": 496, "hechos": '1-16', "atestaciones": 2},
    ]},
    'cani': {"total": 2, "acepciones": [
        {"glosa": 'partir', "pagina": None, "hechos": '20-7', "atestaciones": 2},
    ]},
    'cubu-ruccu': {"total": 2, "acepciones": [
        {"glosa": 'ánimo', "pagina": 10, "hechos": '14-22', "atestaciones": 2},
    ]},
    'cubu-ruccu-a-monnua': {"total": 2, "acepciones": [
        {"glosa": 'permitir', "pagina": 414, "hechos": '21-39', "atestaciones": 2},
    ]},
    'cudu-cutta': {"total": 2, "acepciones": [
        {"glosa": 'llevar', "pagina": 378, "hechos": '15-10', "atestaciones": 2},
    ]},
    'cun-du': {"total": 2, "acepciones": [
        {"glosa": 'desierto', "pagina": 28, "hechos": '1-20', "atestaciones": 2},
    ]},
    'dikki': {"total": 2, "acepciones": [
        {"glosa": 'sembrar', "pagina": 454, "hechos": '3-25', "atestaciones": 2},
    ]},
    'dina': {"total": 2, "acepciones": [
        {"glosa": 'ante', "pagina": 495, "hechos": '25-10', "atestaciones": 1},
        {"glosa": 'poner', "pagina": 418, "atestaciones": 1},
    ]},
    'dinamu-kitta': {"total": 2, "acepciones": [
        {"glosa": 'presentar', "pagina": 425, "hechos": '2-28', "atestaciones": 2},
    ]},
    'ditti-kitta': {"total": 2, "acepciones": [
        {"glosa": 'convencer', "pagina": 270, "hechos": '18-28', "atestaciones": 1},
        {"glosa": 'suerte', "pagina": 92, "hechos": '1-26', "atestaciones": 1},
    ]},
    'ehé': {"total": 2, "acepciones": [
        {"glosa": 'sí', "pagina": 534, "hechos": '5-8', "atestaciones": 2},
    ]},
    'ella': {"total": 2, "acepciones": [
        {"glosa": 'ella', "pagina": 185, "hechos": '12-14', "atestaciones": 2},
    ]},
    'ellos': {"total": 2, "acepciones": [
        {"glosa": 'les , a ellos', "pagina": 178, "hechos": '4-8', "atestaciones": 2},
    ]},
    'emelia': {"total": 2, "acepciones": [
        {"glosa": 'nuevo', "pagina": 121, "hechos": '17-18', "atestaciones": 2},
    ]},
    'halli': {"total": 2, "acepciones": [
        {"glosa": 'cuanto', "pagina": 505, "hechos": '9-16', "atestaciones": 1},
        {"glosa": 'término', "pagina": 94, "hechos": '17-26', "atestaciones": 1},
    ]},
    'huyuru': {"total": 2, "acepciones": [
        {"glosa": 'provincia', "pagina": 83, "hechos": '13-49', "atestaciones": 2},
    ]},
    'ibe': {"total": 2, "acepciones": [
        {"glosa": 'llenar', "pagina": 378, "hechos": '4-8', "atestaciones": 2},
    ]},
    'ikira': {"total": 2, "acepciones": [
        {"glosa": 'cercar', "pagina": 255, "hechos": '9-3', "atestaciones": 1},
        {"glosa": 'lágrima', "pagina": 56, "hechos": '20-19', "atestaciones": 1},
    ]},
    'ime': {"total": 2, "acepciones": [
        {"glosa": 'enviar', "pagina": 318, "hechos": '3-20', "atestaciones": 2},
    ]},
    'iribe': {"total": 2, "acepciones": [
        {"glosa": 'común', "pagina": 110, "hechos": '10-14', "atestaciones": 1},
        {"glosa": 'violar', "pagina": 484, "hechos": '24-6', "atestaciones": 1},
    ]},
    'iyaca-ttoa': {"total": 2, "acepciones": [
        {"glosa": 'encubrir', "pagina": 309, "hechos": '16-37', "atestaciones": 1},
        {"glosa": 'rincón', "pagina": 87, "hechos": '26-26', "atestaciones": 1},
    ]},
    'iyaha-dda': {"total": 2, "acepciones": [
        {"glosa": 'conversar', "pagina": 270, "hechos": '23-1', "atestaciones": 1},
        {"glosa": 'pasar', "pagina": 410, "hechos": '8-40', "atestaciones": 1},
    ]},
    'iyaon': {"total": 2, "acepciones": [
        {"glosa": 'uzgar', "pagina": 367, "hechos": '3-13', "atestaciones": 2},
    ]},
    'iyula': {"total": 2, "acepciones": [
        {"glosa": 'afrentar', "pagina": 228, "hechos": '14-5', "atestaciones": 1},
        {"glosa": 'castigar', "pagina": 253, "hechos": '4-21', "atestaciones": 1},
    ]},
    'iyumu': {"total": 2, "acepciones": [
        {"glosa": 'persuadir', "pagina": 416, "hechos": '13-43', "atestaciones": 2},
    ]},
    'kia-hann': {"total": 2, "acepciones": [
        {"glosa": 'pues', "pagina": 532, "hechos": '2-8', "atestaciones": 2},
    ]},
    'llamado': {"total": 2, "acepciones": [
        {"glosa": 'llamar', "pagina": 373, "hechos": '4-18', "atestaciones": 2},
    ]},
    'lle-ruccu': {"total": 2, "acepciones": [
        {"glosa": 'boca', "pagina": 13, "hechos": '8-35', "atestaciones": 2},
    ]},
    'lluccu-waria': {"total": 2, "acepciones": [
        {"glosa": 'sacar', "pagina": 446, "hechos": '5-9', "atestaciones": 2},
    ]},
    'los': {"total": 2, "acepciones": [
        {"glosa": 'los, a ellos', "pagina": 180, "hechos": '4-3', "atestaciones": 2},
    ]},
    'malli-t-a-coa': {"total": 2, "acepciones": [
        {"glosa": 'ídolo', "pagina": 54, "hechos": '21-25', "atestaciones": 2},
    ]},
    'mehli': {"total": 2, "acepciones": [
        {"glosa": 'pan', "pagina": 77, "hechos": '2-42', "atestaciones": 2},
    ]},
    'mei-cuxu': {"total": 2, "acepciones": [
        {"glosa": 'eunuco', "pagina": 43, "hechos": '8-27', "atestaciones": 2},
    ]},
    'mmayu-n-ni-hùa': {"total": 2, "acepciones": [
        {"glosa": 'librar', "pagina": 272, "hechos": '7-10', "atestaciones": 2},
    ]},
    'muda': {"total": 2, "acepciones": [
        {"glosa": 'orar', "pagina": 389, "hechos": '1-13', "atestaciones": 1},
        {"glosa": 'subir', "pagina": 465, "hechos": '2-34', "atestaciones": 1},
    ]},
    'mùn-hitti': {"total": 2, "acepciones": [
        {"glosa": 'limosna', "pagina": 59, "hechos": '9-36', "atestaciones": 2},
    ]},
    'nnebe-ttoa': {"total": 2, "acepciones": [
        {"glosa": 'esparcir', "pagina": 324, "hechos": '8-1', "atestaciones": 2},
    ]},
    'nuestros': {"total": 2, "acepciones": [
        {"glosa": 'nuestros', "pagina": 147, "hechos": '3-13', "atestaciones": 2},
    ]},
    'oaya': {"total": 2, "acepciones": [
        {"glosa": 'ahogar', "pagina": 229, "hechos": '15-29', "atestaciones": 2},
    ]},
    'platta': {"total": 2, "acepciones": [
        {"glosa": 'dinero', "pagina": 32, "hechos": '7-16', "atestaciones": 1},
        {"glosa": 'plata, dinero', "pagina": 80, "hechos": '17-29', "atestaciones": 1},
    ]},
    'pucu': {"total": 2, "acepciones": [
        {"glosa": 'diferencia', "pagina": 32, "hechos": '15-9', "atestaciones": 1},
        {"glosa": 'separar', "pagina": 455, "hechos": '19-9', "atestaciones": 1},
    ]},
    'raiya-ttoa': {"total": 2, "acepciones": [
        {"glosa": 'aparecer', "pagina": 236, "hechos": '1-3', "atestaciones": 2},
    ]},
    'rule': {"total": 2, "acepciones": [
        {"glosa": 'luz', "pagina": 61, "hechos": '9-3', "atestaciones": 2},
    ]},
    'saturdaca': {"total": 2, "acepciones": [
        {"glosa": 'sábado', "pagina": 82, "hechos": '13-14', "atestaciones": 2},
    ]},
    'señal': {"total": 2, "acepciones": [
        {"glosa": 'señalar', "pagina": 455, "hechos": '1-23', "atestaciones": 2},
    ]},
    'sica-n-doa': {"total": 2, "acepciones": [
        {"glosa": 'rebelarse', "pagina": 432, "hechos": '26-19', "atestaciones": 1},
        {"glosa": 'rebelde', "pagina": 86, "hechos": '26-19', "atestaciones": 1},
    ]},
    'sica-ni-coa': {"total": 2, "acepciones": [
        {"glosa": 'incredulo', "pagina": 55, "hechos": '14-2', "atestaciones": 1},
        {"glosa": 'incredulo :', "pagina": 116, "hechos": '14-2', "atestaciones": 1},
    ]},
    'sima': {"total": 2, "acepciones": [
        {"glosa": 'alaridos (dar', "pagina": 230, "hechos": '19-28', "atestaciones": 1},
        {"glosa": 'clamar', "pagina": 256, "hechos": '7-60', "atestaciones": 1},
    ]},  # homografo de una clave del lexicon
    'sima-sima': {"total": 2, "acepciones": [
        {"glosa": 'gritar', "pagina": 336, "hechos": '19-32', "atestaciones": 2},
    ]},
    'ttenna': {"total": 2, "acepciones": [
        {"glosa": 'sangre', "pagina": 82, "hechos": '2-19', "atestaciones": 2},
    ]},
    'ttica-ha': {"total": 2, "acepciones": [
        {"glosa": 'dañar', "pagina": 277, "hechos": '21-10', "atestaciones": 1},
        {"glosa": 'escapar', "pagina": 321, "atestaciones": 1},
    ]},
    'ttu': {"total": 2, "acepciones": [
        {"glosa": 'cual', "pagina": 205, "hechos": '1-12', "atestaciones": 1},
        {"glosa": 'hija', "pagina": 51, "hechos": '2-17', "atestaciones": 1},
    ]},
    'tturku': {"total": 2, "acepciones": [
        {"glosa": 'desechar', "pagina": 299, "hechos": '7-39', "atestaciones": 1},
        {"glosa": 'rempujar', "pagina": 436, "hechos": '7-27', "atestaciones": 1},
    ]},
    'tullu-du': {"total": 2, "acepciones": [
        {"glosa": 'abrir', "pagina": 220, "hechos": '5-10', "atestaciones": 2},
    ]},
    'vosotros': {"total": 2, "acepciones": [
        {"glosa": 'vosotros, vosotras', "pagina": 165, "hechos": '1-8', "atestaciones": 2},
    ]},
    'wacaiya': {"total": 2, "acepciones": [
        {"glosa": 'maldecir', "pagina": 380, "hechos": '23-4', "atestaciones": 2},
    ]},
    'wadu-lli': {"total": 2, "acepciones": [
        {"glosa": 'viento', "pagina": 102, "hechos": '2-2', "atestaciones": 2},
    ]},
    'wurebu': {"total": 2, "acepciones": [
        {"glosa": 'fornicar', "pagina": 333, "hechos": '15-20', "atestaciones": 2},
    ]},
    'wùseica-da-hitti': {"total": 2, "acepciones": [
        {"glosa": 'paz', "pagina": 78, "hechos": '7-26', "atestaciones": 2},
    ]},
    'yaha': {"total": 2, "acepciones": [
        {"glosa": 'aquí', "pagina": 496, "hechos": '16-28', "atestaciones": 2},
    ]},
    'yuhu': {"total": 2, "acepciones": [
        {"glosa": 'generación', "pagina": 47, "hechos": '2-40', "atestaciones": 1},
        {"glosa": 'pariente :', "pagina": 77, "hechos": '7-3', "atestaciones": 1},
    ]},
    'ùsanu-wa-i': {"total": 2, "acepciones": [
        {"glosa": 'alabar', "pagina": 229, "hechos": '2-47', "atestaciones": 2},
    ]},
}

# Raices cuya forma coincide con una clave YA existente en VOCABULARIO_BASE.
# No son necesariamente el mismo morfema: se listan para que la fusion las
# mire a mano. (Perea avisa en su p. 546 de la alternancia r/l que hace
# colisionar -ruccu ~ -luccu con luccu «hombre».)
HOMOGRAFOS_CON_EL_LEXICON = ['awa', 'bara', 'sima', 'uria']


def resumen() -> str:
    n = len(COMPARANDA_LOKONO)
    ac = sum(len(e["acepciones"]) for e in COMPARANDA_LOKONO.values())
    at = sum(e["total"] for e in COMPARANDA_LOKONO.values())
    return (f"Perea 1942 — {n} raices lokono, {ac} acepciones, "
            f"{at} atestaciones; {len(HOMOGRAFOS_CON_EL_LEXICON)} homografos")


if __name__ == "__main__":
    import io as _io, sys as _sys
    if hasattr(_sys.stdout, "buffer"):
        _sys.stdout = _io.TextIOWrapper(_sys.stdout.buffer, encoding="utf-8",
                                        errors="replace")
    print(resumen())

import requests

url = 'http://0.0.0.0:5001/edc/hersteller/dataplane/pred/'

body = [{
    "ListeKomponenten": ["K000055", "K000057"],  # id or material name
    "Massenanteile": [0.75, 0.25],  # unit g/g
    "Flächenanteilmodifiziert": 0,  # unit %
    "Geometrie": "Quader",  # unit: list of types
    "Kopfraumatmosphäre": None,  # unit list of (pa)
    "Masse": None,  # unit g
    "Verpackungstyp": "Folie",  # type
    "CAD": None,  # link to CAD file
    "RauheitRa": 0.08966666666666667,  # unit µm
    "RauheitRz": 0.7366666666666667,  # unit µm
    "Trübung": 176.6,  # unit HLog
    "Glanz": 39,  # unit GE
    "Dicke": 769.6666666666666,  # unit µm
    "Emodul": 878.7979886112262,  # unit MPa
    "MaximaleZugspannung": 37.156951742990245,  # unit MPa
    "MaximaleLängenänderung": 19.73276680651324,  # unit %
    # Quality Labels
    "Ausformung": 6,
    "Kaltverfo": 3,
},
    {
        "ListeKomponenten": ["K000055", "K000057"],  # id or material name
        "Massenanteile": [0.75, 0.25],  # unit g/g
        "Flächenanteilmodifiziert": 0,  # unit %
        "Geometrie": "Quader",  # unit: list of types
        "Kopfraumatmosphäre": None,  # unit list of (pa)
        "Masse": None,  # unit g
        "Verpackungstyp": "Folie",  # type
        "CAD": None,  # link to CAD file
        "RauheitRa": 0.08966666666666667,  # unit µm
        "RauheitRz": 0.7366666666666667,  # unit µm
        "Trübung": 176.6,  # unit HLog
        "Glanz": 39,  # unit GE
        "Dicke": 769.6666666666666,  # unit µm
        "Emodul": 878.7979886112262,  # unit MPa
        "MaximaleZugspannung": 37.156951742990245,  # unit MPa
        "MaximaleLängenänderung": 19.73276680651324,  # unit %
        # Quality Labels
        "Ausformung": 6,
        "Kaltverfo": 3,
    }
]

if __name__ == '__main__':
    response = requests.post(url, json=body)
    print(response.json())
    print(type(response.json()))
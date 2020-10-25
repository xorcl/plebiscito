from config import *
import requests
import hashlib
import time
import datetime
import json
import email.utils as eut
from img_constants import READABLE_DATE
import logging

def get_servel_data(conf):
    constitucion = requests.get(conf["constitucion"])
    organo = requests.get(conf["organo"])
    return {
        "constitucion": servel_to_state(constitucion),
        "organo": servel_to_state(organo)
    }

def servel_to_state(req):
    data = req.json()
    date = (eut.parsedate_to_datetime(req.headers["last-modified"]) - datetime.timedelta(hours=3)).strftime(READABLE_DATE)
    state = {
        "fecha": date,
        "resultados": {},
        "mesas": {},
        "votos": {},
        "invalidos": {},
    }
    # Resultados
    for v in data["data"]:
        state["resultados"][v["a"].lower()] = {
            "votos": v["c"],
            "porcentaje": v["d"],
            "ganadora": v["f"]
        }
    for v in data["resumen"]:
        if v["a"].lower() in ("válidamente emitidos", "total votación"):
            state["votos"][v["a"].lower()] = {
                "votos": v["c"],
                "porcentaje": v["d"]
            }
        elif v["a"].lower() in ("votos nulos", "votos en blanco"):
            state["invalidos"][v["a"].lower()] = {
                "votos": v["c"],
                "porcentaje": v["d"]
            }
    state["mesas"] = {
        "total": data["totalMesas"],
        "escrutadas": data["mesasEscrutadas"],
        "porcentaje": data["totalMesasPorcent"],
    }
    return state


def data_changed(data):
    # Load state
    data_hash = hashlib.sha512(json.dumps(data).encode()).hexdigest()
    state = load_state()
    state_hash = hashlib.sha512(json.dumps(state).encode()).hexdigest()
    save_state(data)
    return data_hash != state_hash

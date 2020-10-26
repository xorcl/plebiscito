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
    newest_data = {}
    try:
        state = load_state()
        save_state(data)
        data_date_1 = datetime.datetime.strptime(data["constitucion"]["fecha"], READABLE_DATE)
        state_date_1 = datetime.datetime.strptime(state["constitucion"]["fecha"], READABLE_DATE)
        if data_date_1 > state_date_1:
            newest_data["constitucion"] = data["constitucion"]
        else:
            newest_data["constitucion"] = state["constitucion"]
        data_date_2 = datetime.datetime.strptime(data["organo"]["fecha"], READABLE_DATE)
        state_date_2 = datetime.datetime.strptime(state["organo"]["fecha"], READABLE_DATE)
        if data_date_1 > state_date_1:
            newest_data["organo"] = data["organo"]
        else:
            newest_data["organo"] = state["organo"]        
        return max(state_date_1, state_date_2) > max(data_date_1, data_date_2), newest_data
    except Exception:
        # No state:
        return True, data
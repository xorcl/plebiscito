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
    return servel_to_state(requests.get(conf["url"]))

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
            "ganadora": v["f"],
            "candidatos": {},
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
        data_date = datetime.datetime.strptime(data["fecha"], READABLE_DATE)
        state_date = datetime.datetime.strptime(state["fecha"], READABLE_DATE)
        newest_data_date = max(data_date, state_date)
        if data_date > state_date:
            newest_data = data
        else:
            newest_data = state
        save_state(newest_data)
        logging.info(f"newest_date={newest_data_date.strftime(READABLE_DATE)}, state_date={state_date.strftime(READABLE_DATE)}")
        return state_date < newest_data_date, newest_data
    except Exception:
        # No state:
        save_state(data)
        return True, data

def same_data(d1, d2):
    da = d1.copy()
    db = d2.copy()
    del da["fecha"]
    del db["fecha"]
    return da == db
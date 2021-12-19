from img_constants import *
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import os

def generate_image(data):
    # Fechas
    date = datetime.strptime(data["fecha"], READABLE_DATE)
    # Abrir imagen
    img_in = Image.open("template.png")
    draw = ImageDraw.Draw(img_in)
    # Fonts
    time_font = ImageFont.truetype(SECONDARY_FONT, UPDATE_TIME_FONT_SIZE)
    const_perc_font = ImageFont.truetype(PRIMARY_FONT, MAIN_PERC_FONT_SIZE)
    total_votes_font = ImageFont.truetype(PRIMARY_FONT, MAIN_VOTES_FONT_SIZE)
    details_font = ImageFont.truetype(SECONDARY_FONT, DETAIL_FONT_SIZE)
    # Agregar timestamp
    draw.text((UPDATE_TIME_X, UPDATE_TIME_Y),date.strftime(READABLE_DATE),WHITE,font=time_font)


    # Constitución
    ## Porcentajes
    draw.text((PERC_X, FIRST_PERC_Y),data["resultados"]["1. gabriel boric font"]["porcentaje"],WHITE,font=const_perc_font)
    w, _ = draw.textsize(data["resultados"]["2. jose antonio kast rist"]["porcentaje"], font=const_perc_font)
    draw.text((img_in.width - PERC_X - w, FIRST_PERC_Y),data["resultados"]["2. jose antonio kast rist"]["porcentaje"],WHITE,font=const_perc_font)
    ## Votos Totales
    draw.text((TOTAL_VOTES_X, FIRST_TOTAL_VOTES_Y),data["resultados"]["1. gabriel boric font"]["votos"],GREY,font=total_votes_font)
    w, _ = draw.textsize(data["resultados"]["2. jose antonio kast rist"]["votos"], font=total_votes_font)
    draw.text((img_in.width - TOTAL_VOTES_X - w, FIRST_TOTAL_VOTES_Y),data["resultados"]["2. jose antonio kast rist"]["votos"],GREY,font=total_votes_font)
    ## Gráfico
    first_perc_float_left = float(data["resultados"]["1. gabriel boric font"]["porcentaje"].strip("%").replace(",","."))
    arc_left = (180 + (first_perc_float_left * 180) / 100)
    draw.arc(FIRST_DONUT, 180, arc_left, RED, 142)
    first_perc_float_right = float(data["resultados"]["2. jose antonio kast rist"]["porcentaje"].strip("%").replace(",","."))
    arc_left = (first_perc_float_right * 180 / 100)
    draw.arc(FIRST_DONUT, 360 - arc_left, 360, BLUE, 142)
    ## Tabla de detalles
    ### Mesas
    table_escrutada_first = "{:.2f}".format(int(data["mesas"]["escrutadas"].replace(".","")) / int(data["mesas"]["total"].replace(".","")) * 100)
    draw.text((BOXES_DETAIL_X, FIRST_DETAIL1_Y),"{} ({}% totales)".format(data["mesas"]["escrutadas"],table_escrutada_first),WHITE,font=details_font)
    draw.text((BOXES_DETAIL_X, FIRST_DETAIL2_Y),data["mesas"]["total"],WHITE,font=details_font)
    ### Votos
    perc_total_first = "{:.2f}".format(int(data['votos']['válidamente emitidos']['votos'].replace(".","")) / TOTAL_VOTANTES * 100)
    draw.text((VOTES_DETAIL_X, FIRST_DETAIL1_Y),f"{data['votos']['válidamente emitidos']['votos']} ({data['votos']['válidamente emitidos']['porcentaje']} totales)",WHITE,font=details_font)
    draw.text((VOTES_DETAIL_X, FIRST_DETAIL2_Y),f"{data['votos']['total votación']['votos']} ({perc_total_first}% padrón)",WHITE,font=details_font)
    ### Inválidos
    draw.text((INVALID_DETAIL_X, FIRST_DETAIL1_Y),f"{data['invalidos']['votos nulos']['votos']} ({data['invalidos']['votos nulos']['porcentaje']} totales)",WHITE,font=details_font)
    draw.text((INVALID_DETAIL_X, FIRST_DETAIL2_Y),f"{data['invalidos']['votos en blanco']['votos']} ({data['invalidos']['votos en blanco']['porcentaje']} totales)",WHITE,font=details_font)


    ## Devolver nombre de nueva imagen
    generada = f"img/resultados_{date}.png"
    # Guardar imagen
    os.makedirs("img/", exist_ok=True)
    img_in.save(generada)
    return generada
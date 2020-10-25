from img_constants import *
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import os

def generate_image(data):
    # Fechas
    date1 = datetime.strptime(data["organo"]["fecha"], READABLE_DATE)
    date2 = datetime.strptime(data["constitucion"]["fecha"], READABLE_DATE)
    date = max(date1, date2)
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
    draw.text((PERC_X, FIRST_PERC_Y),data["constitucion"]["resultados"]["apruebo"]["porcentaje"],WHITE,font=const_perc_font)
    w, _ = draw.textsize(data["constitucion"]["resultados"]["rechazo"]["porcentaje"], font=const_perc_font)
    draw.text((img_in.width - PERC_X - w, FIRST_PERC_Y),data["constitucion"]["resultados"]["rechazo"]["porcentaje"],WHITE,font=const_perc_font)
    ## Votos Totales
    draw.text((TOTAL_VOTES_X, FIRST_TOTAL_VOTES_Y),data["constitucion"]["resultados"]["apruebo"]["votos"],GREY,font=total_votes_font)
    w, _ = draw.textsize(data["constitucion"]["resultados"]["rechazo"]["votos"], font=total_votes_font)
    draw.text((img_in.width - TOTAL_VOTES_X - w, FIRST_TOTAL_VOTES_Y),data["constitucion"]["resultados"]["rechazo"]["votos"],GREY,font=total_votes_font)
    ## Gráfico
    first_perc_float_left = float(data["constitucion"]["resultados"]["apruebo"]["porcentaje"].strip("%").replace(",","."))
    arc_left = (180 + (first_perc_float_left * 180) / 100)
    draw.arc(FIRST_DONUT, 180, arc_left, RED, 142)
    first_perc_float_right = float(data["constitucion"]["resultados"]["rechazo"]["porcentaje"].strip("%").replace(",","."))
    arc_left = (first_perc_float_right * 180 / 100)
    draw.arc(FIRST_DONUT, 360 - arc_left, 360, BLUE, 142)
    ## Tabla de detalles
    ### Mesas
    draw.text((BOXES_DETAIL_X, FIRST_DETAIL1_Y),data["constitucion"]["mesas"]["escrutadas"],WHITE,font=details_font)
    draw.text((BOXES_DETAIL_X, FIRST_DETAIL2_Y),data["constitucion"]["mesas"]["total"],WHITE,font=details_font)
    ### Votos
    perc_total_first = "{:.2f}".format(int(data['constitucion']['votos']['válidamente emitidos']['votos'].replace(".","")) / TOTAL_VOTANTES * 100)
    draw.text((VOTES_DETAIL_X, FIRST_DETAIL1_Y),f"{data['constitucion']['votos']['válidamente emitidos']['votos']} ({data['constitucion']['votos']['válidamente emitidos']['porcentaje']} totales)",WHITE,font=details_font)
    draw.text((VOTES_DETAIL_X, FIRST_DETAIL2_Y),f"{data['constitucion']['votos']['total votación']['votos']} ({perc_total_first}% padrón)",WHITE,font=details_font)
    ### Inválidos
    draw.text((INVALID_DETAIL_X, FIRST_DETAIL1_Y),f"{data['constitucion']['invalidos']['votos nulos']['votos']} ({data['constitucion']['invalidos']['votos nulos']['porcentaje']} totales)",WHITE,font=details_font)
    draw.text((INVALID_DETAIL_X, FIRST_DETAIL2_Y),f"{data['constitucion']['invalidos']['votos en blanco']['votos']} ({data['constitucion']['invalidos']['votos en blanco']['porcentaje']} totales)",WHITE,font=details_font)

    # Órgano
    draw.text((PERC_X, SECOND_PERC_Y),data["organo"]["resultados"]["convención mixta constitucional"]["porcentaje"],WHITE,font=const_perc_font)
    w, _ = draw.textsize(data["organo"]["resultados"]["convención constitucional"]["porcentaje"], font=const_perc_font)
    draw.text((img_in.width - PERC_X - w, SECOND_PERC_Y),data["organo"]["resultados"]["convención constitucional"]["porcentaje"],WHITE,font=const_perc_font)
    ## Votos Totales
    draw.text((TOTAL_VOTES_X, SECOND_TOTAL_VOTES_Y),data["organo"]["resultados"]["convención mixta constitucional"]["votos"],GREY,font=total_votes_font)
    w, _ = draw.textsize(data["organo"]["resultados"]["convención constitucional"]["votos"], font=total_votes_font)
    draw.text((img_in.width - TOTAL_VOTES_X - w, SECOND_TOTAL_VOTES_Y),data["organo"]["resultados"]["convención constitucional"]["votos"],GREY,font=total_votes_font)
    ## Gráfico
    second_perc_float_left = float(data["organo"]["resultados"]["convención mixta constitucional"]["porcentaje"].strip("%").replace(",","."))
    arc = (180 + (second_perc_float_left * 180) / 100)
    draw.arc(SECOND_DONUT, 180, arc, RED, 142)
    
    second_perc_float_right = float(data["organo"]["resultados"]["convención constitucional"]["porcentaje"].strip("%").replace(",","."))
    arc_left = (second_perc_float_right * 180 / 100)
    draw.arc(SECOND_DONUT, 360 - arc_left, 360, BLUE, 142)


    ## Tabla de detalles
    draw.text((BOXES_DETAIL_X, SECOND_DETAIL1_Y),data["organo"]["mesas"]["escrutadas"],WHITE,font=details_font)
    draw.text((BOXES_DETAIL_X, SECOND_DETAIL2_Y),data["organo"]["mesas"]["total"],WHITE,font=details_font)
    ### Votos

    perc_total_second = "{:.2f}".format(int(data['organo']['votos']['válidamente emitidos']['votos'].replace(".","")) / TOTAL_VOTANTES * 100)
    draw.text((VOTES_DETAIL_X, SECOND_DETAIL1_Y),f"{data['organo']['votos']['válidamente emitidos']['votos']} ({data['organo']['votos']['válidamente emitidos']['porcentaje']} totales)",WHITE,font=details_font)
    draw.text((VOTES_DETAIL_X, SECOND_DETAIL2_Y),f"{data['organo']['votos']['total votación']['votos']} ({perc_total_second}% padrón)",WHITE,font=details_font)
    ### Inválidos
    draw.text((INVALID_DETAIL_X, SECOND_DETAIL1_Y),f"{data['organo']['invalidos']['votos nulos']['votos']} ({data['organo']['invalidos']['votos nulos']['porcentaje']} totales)",WHITE,font=details_font)
    draw.text((INVALID_DETAIL_X, SECOND_DETAIL2_Y),f"{data['organo']['invalidos']['votos en blanco']['votos']} ({data['organo']['invalidos']['votos en blanco']['porcentaje']} totales)",WHITE,font=details_font)
    ## Devolver nombre de nueva imagen
    generada = f"img/resultados_{date}.png"
    # Guardar imagen
    os.makedirs("img/", exist_ok=True)
    img_in.save(generada)
    return generada
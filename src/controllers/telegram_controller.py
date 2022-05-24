##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: telegram_controller.py
# Capitulo: Estilo Microservicios
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Febrero 2022
# Descripción:
#
#   Ésta clase define el controlador del microservicio API.
#   Implementa la funcionalidad y lógica de negocio del Microservicio.
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |     send_message()     |         Ninguno          |  - Procesa el mensaje |
#           |                        |                          |    recibido en la     |
#           |                        |                          |    petición y ejecuta |
#           |                        |                          |    el envío a         |
#           |                        |                          |    Telegram.          |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
from flask import request, jsonify
from configparser import ConfigParser
import telepot
import json
from os import remove
import requests

class TelegramController:

    @staticmethod
    def send_message():
        data = json.loads(request.data)
        if not data:
            return jsonify({"msg": "invalid request"}), 400
        msg = data["message"]

        bot, chat_id, url = TelegramController.init_telegram()
        if msg == '/policies/policy.pdf':
            files = {'document': open(msg, 'rb')}
            resp = requests.post(url, files = files)
            remove("/policies/policy.pdf")
            if resp == 200:
                return jsonify({"msg": "success"}), 200
            else:
                return jsonify({"msg": "failure"}), 500
        else:
            if bot.sendMessage(chat_id, msg):
                return jsonify({"msg": "success"}), 200
            else:
                return jsonify({"msg": "failure"}), 500

    @staticmethod
    def init_telegram():
        configur = ConfigParser()
        configur.read('/notifier/settings.ini')
        token = configur.get('TELEGRAM', 'TOKEN')
        chat_id = configur.get('TELEGRAM', 'CHAT_ID')
        bot = telepot.Bot(token)
        url = 'https://api.telegram.org/bot'+token+'/sendDocument?chat_id='+chat_id
        return bot, chat_id, url

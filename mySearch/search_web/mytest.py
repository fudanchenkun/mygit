#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import csv
import time
import requests
from bs4 import BeautifulSoup

from P2pClass import P2P,PaiPaiDai

html=requests.get('http://invest.ppdai.com/loan/list_safe_s0_p1?OldVersion=0&Rate=0')._content
print BeautifulSoup(html,"lxml").find('title').text

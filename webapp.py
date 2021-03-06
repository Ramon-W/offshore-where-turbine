from flask import Flask, redirect, Markup, url_for, session, request, jsonify
from flask import render_template

import pprint
import os
import json
import sys
from datetime import datetime, date, timedelta
from pytz import timezone
import pytz

app = Flask(__name__)

@app.route('/') 
def render_main():
  grid = []
  with open('windturbine.json') as d:
    data = json.load(d)
  grid_code = ''
  grid_code_basic = ''
  row = 0    
  square = 0
  while row < 15:
    grid_code += '<tr>'
    grid_code_basic += '<tr>'
    while square < 24:
      grid_code += '<td>'
      grid_code_basic += '<td>'
      point = chr(row + 65) + str(square + 1)
      if point in data:
        value = ''
        if row == 0 and square == 0:
          value = 'A1'
        elif row == 0:
          value = str(square + 1)
        elif square == 0:
          value = chr(row + 65)
        green = (((1 / float((data[point]['200wind'] + data[point]['150wind'] + data[point]['100wind'])/3) - 0.125) * 165) / (0.1667 - 0.125))
        grid_code += ('<a style="background-color:rgba(255,' + str(green) + ', 0, 0.75);" class="square-button ' + chr(row + 65) + str(square + 1) + '" data-html="true" data-placement="auto right" title="<strong>' +
                      data[point]['coordinates'] + '</strong>" data-toggle="popover" data-trigger="focus" data-content="<b>Wind Speed 200m (m/s):</b> ' +
                      str(data[point]['200wind']) + '<br><b>Wind Speed 150m (m/s):</b> ' + str(data[point]['150wind']) + '<br><b>Wind Speed 100m (m/s):</b> ' + 
                      str(data[point]['100wind']) + '<br><b>Depth (m):</b> ' + str(data[point]['depth']) +
                      '"tabindex="0" role="button">' + value + '</a></td>')
        grid_code_basic += ('<a style="background-color: transparent;" class="square-button ' + chr(row + 65) + str(square + 1) + '" data-html="true" data-placement="auto right" title="<strong>' +
                            data[point]['coordinates'] + '</strong>" data-toggle="popover" data-trigger="focus" data-content="<b>Wind Speed 200m (m/s):</b> ' +
                            str(data[point]['200wind']) + '<br><b>Wind Speed 150m (m/s):</b> ' + str(data[point]['150wind']) + '<br><b>Wind Speed 100m (m/s):</b> ' + 
                            str(data[point]['100wind']) + '<br><b>Depth (m):</b> ' + str(data[point]['depth']) +
                            '"tabindex="0" role="button">' + value + '</a></td>')
      else:
        value = ''
        if row == 0 and square == 0:
          value = 'A1'
        elif row == 0:
          value = str(square + 1)
        elif square == 0:
          value = chr(row + 65)
        grid_code += value + '</td>'
        grid_code_basic += value + '</td>'
      square += 1
    grid_code += '</tr>'
    grid_code_basic += '</tr>'
    square = 0
    row += 1
  return render_template('main.html', wind_grid = Markup(grid_code), basic_grid = Markup(grid_code_basic))

if __name__ == "__main__":
    app.run()

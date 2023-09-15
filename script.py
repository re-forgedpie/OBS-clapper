# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Created by Re-ForgedPie

import obspython as obs
import os
import csv
import datetime
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Define CSV file path
csv_file_path = os.path.join(os.path.dirname(__file__), "recording_data.csv")

# Define the base directory for recordings
BASE_DIR = ''
SESSION_DIR = ""
SHOT_LIST_FILE = "shot_list.json"
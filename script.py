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

class FilmSettings:
    def __init__(self):
        self.scene_number = 1
        self.shot_number = 1
        self.take_number = 1

    def load_from_shot_list(self):
        return
        # TODO
        # shot_list_path = os.path.join(SESSION_DIR, SHOT_LIST_FILE)
        # if os.path.exists(shot_list_path):
        #     with open(shot_list_path, 'r') as f:
        #         shot_list = json.load(f)
        #         self.scene_number = shot_list['scene_number']
        #         self.shot_number = shot_list['shot_number']
        #         self.take_number = shot_list['take_number']

    def save_to_shot_list(self):
        return
        # TODO
        # shot_list_path = os.path.join(SESSION_DIR, SHOT_LIST_FILE)
        # shot_list = {
        #     'scene_number': self.scene_number,
        #     'shot_number': self.shot_number,
        #     'take_number': self.take_number
        # }
        # with open(shot_list_path, 'w') as f:
        #     json.dump(shot_list, f)

film = FilmSettings()
film.load_from_shot_list()

# Hotkey functions
def modify_scene(pressed, increment=True):
    if pressed:
        film.scene_number += 1 if increment else -1
        film.take_number = 1
        film.shot_number = 1
        film.save_to_shot_list()
        obs.script_log(obs.LOG_INFO, f"modify scene hotkey pressed {film.scene_number} | {film.shot_number} take {film.take_number}")

def modify_shot(pressed, increment=True):
    if pressed:
        film.shot_number += 1 if increment else -1
        film.take_number = 1
        film.save_to_shot_list()
        obs.script_log(obs.LOG_INFO, f"modify shot hotkey pressed| {film.scene_number} | {film.shot_number} take {film.take_number}")

def modify_take(pressed, increment=True):
    if pressed:
        film.take_number += 1 if increment else -1
        film.save_to_shot_list()
        obs.script_log(obs.LOG_INFO, f"modify take hotkey pressed {film.scene_number} | {film.shot_number} take {film.take_number}")

# HTTP server classes
class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if "increase_scene" in self.path:
            modify_scene(True, True)
        elif "decrease_scene" in self.path:
            modify_scene(True, False)
        elif "increase_shot" in self.path:
            modify_shot(True, True)
        elif "decrease_shot" in self.path:
            modify_shot(True, False)
        elif "increase_take" in self.path:
            modify_take(True, True)
        elif "decrease_take" in self.path:
            modify_take(True, False)
        self.wfile.write(f"Scene: {film.scene_number}, Shot: {film.shot_number}, Take: {film.take_number}".encode())

def run_server():
    httpd = HTTPServer(("localhost", 8000), SimpleRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_server).start()

class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id
        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = "Hotkey " + str(self._id)
        self.hotkey_id = obs.obs_hotkey_register_frontend(
            self._id, description, self.callback
        )
        obs.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = obs.obs_data_get_array(self.obs_data, self._id)
        obs.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = obs.obs_hotkey_save(self.hotkey_id)
        obs.obs_data_set_array(self.obs_data, self._id, self.hotkey_saved_key)
        obs.obs_data_array_release(self.hotkey_saved_key)

# Remaining unchanged code

def script_description():
    return "OBS Script for renaming recordings based on Scene Number, Shot, Take numbers and appending to a CSV file."

def rename_and_append_to_csv(file_path):
    global film, SESSION_DIR
    file_extension = os.path.splitext(file_path)[1]
    hour = datetime.datetime.now().strftime('%d_%H')
    new_file_name = f"{hour}__Scene{film.scene_number}_S{film.shot_number}_T{film.take_number}{file_extension}"
    new_file_path = os.path.join(SESSION_DIR, new_file_name)

    if BASE_DIR != "":
        os.rename(file_path, new_file_path)
    else:
        obs.script_log(obs.LOG_ERROR, "No Base directory defined. Could not save file")


    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([film.scene_number, film.shot_number, film.take_number, new_file_name])

    obs.script_log(obs.LOG_INFO, f"Renamed {file_path} to {new_file_path} and appended data to CSV.")
    modify_take(True)

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        latest_recording = obs.obs_frontend_get_last_recording()
        rename_and_append_to_csv(latest_recording)

scene_hotkey = None
shot_hotkey = None
take_hotkey = None
user_code = None

def script_load(settings):
    global scene_hotkey, shot_hotkey, take_hotkey, BASE_DIR, user_code, SESSION_DIR, film

    BASE_DIR = obs.obs_data_get_string(settings, "base_dir")  # Get the directory from settings
    user_code = obs.obs_data_get_string(settings, "user_code")

    SESSION_DIR = os.path.join(BASE_DIR, user_code)
    film.take_number = obs.obs_data_get_int(settings, "take_number")
    film.shot_number = obs.obs_data_get_int(settings, "shot_number")
    film.scene_number = obs.obs_data_get_int(settings, "scene_number")

    if BASE_DIR != "":
        if not os.path.exists(SESSION_DIR):
            os.makedirs(SESSION_DIR)
    else:
        obs.script_log(obs.LOG_WARNING, "No Base directory defined.")

    obs.obs_frontend_add_event_callback(on_event)
    scene_hotkey = Hotkey(modify_scene, settings, "scene_key")
    shot_hotkey = Hotkey(modify_shot, settings, "shot_key")
    take_hotkey = Hotkey(modify_take, settings, "take_key")
    decrement_scene_hotkey = Hotkey(lambda pressed: modify_scene(pressed, False), settings, "decrement_scene_key")
    decrement_shot_hotkey = Hotkey(lambda pressed: modify_shot(pressed, False), settings, "decrement_shot_key")
    decrement_take_hotkey = Hotkey(lambda pressed: modify_take(pressed, False), settings, "decrement_take_key")

def script_save(settings):
    global user_code, BASE_DIR

    # scene_hotkey.save_hotkey()
    # shot_hotkey.save_hotkey()
    # take_hotkey.save_hotkey()

    obs.obs_data_set_string(settings, "base_dir", BASE_DIR)

    obs.obs_data_set_string(settings, "user_code", user_code)

def script_update(settings):
    global scene_hotkey, shot_hotkey, take_hotkey, BASE_DIR, user_code, SESSION_DIR, film

    BASE_DIR = obs.obs_data_get_string(settings, "base_dir")  # Get the directory from settings
    user_code = obs.obs_data_get_string(settings, "user_code")

    SESSION_DIR = os.path.join(BASE_DIR, user_code)
    film.take_number = obs.obs_data_get_int(settings, "take_number")
    film.shot_number = obs.obs_data_get_int(settings, "shot_number")
    film.scene_number = obs.obs_data_get_int(settings, "scene_number")

    # Prevent Script crashing/erroring when no base DIR is specified. (Tries to write in root dir)
    if BASE_DIR != "":
        if not os.path.exists(SESSION_DIR):
            os.makedirs(SESSION_DIR)
    else:
        obs.script_log(obs.LOG_WARNING, "No Base directory defined.")

def script_properties():
    global user_code, BASE_DIR
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "user_code", "Categorisation Code", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_path(props, "base_dir", "Base Directory for Recordings", obs.OBS_PATH_DIRECTORY, "",
                                BASE_DIR)

    obs.obs_properties_add_text(props, "user_code", "Categorisation Code", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "scene_number", "Scene Number+", 1, 1000, 1)
    obs.obs_properties_add_int(props, "shot_number", "Shot Number+", 1, 1000, 1)
    obs.obs_properties_add_int(props, "take_number", "Take Number+", 1, 1000, 1)
    return props

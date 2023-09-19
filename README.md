# OBS-Clapper: Automated File Renaming for Filmmakers

Easily manage your OBS recordings with Scene, Shot, and Take metadata.

## Overview

`OBS-Clapper` is an OBS script tailored for filmmakers and video content creators. Its inception roots in the challenges I faced in managing complex shot lists during video creation. By automating the renaming of files to include Scene, Shot, and Take numbers, this script drastically simplifies the post-production workflow. What else? Integration capabilities with tools like Stream Deck using HTTP endpoints.

## Core Features

- **Organized Filenames with Scene, Shot, and Take**: No more confusion when sorting through multiple clips from a single shooting session.

- **Intuitive HTTP Endpoints**: Set up custom buttons on tools like Stream Deck to control your shot details via simple HTTP requests.

- **Automatic Take Increment**: Whenever you're ready for the next take, OBS-Clapper has got you covered. The Take number auto-increments, allowing you to focus on the content.

- **Seamless Integration with Stream Deck**: The endpoints' design guarantees an enhanced user experience for Stream Deck users.

## HTTP Endpoints

Invoke these via `http://localhost:8000/{end_point}`:

- **Increase Scene**: `/increase_scene`
  
- **Decrease Scene**: `/decrease_scene`
  
- **Increase Shot**: `/increase_shot`
  
- **Decrease Shot**: `/decrease_shot`
  
- **Increase Take**: `/increase_take`
  
- **Decrease Take**: `/decrease_take`

*Response:* A successful request will return a 200 OK status.

## Setting It Up

### Installation

1. Download the script.
2. Move it to your OBS's script directory.
3. Fire up OBS and navigate to `Tools` > `Scripts`.
4. Add the script using the `+` button.

### Configuration

![Configuration Image](https://github.com/re-forgedpie/OBS-clapper/assets/97791696/0c058bc2-ed38-4380-a667-523b5e152922)

1. The "Categorization code" is a unique string identifier, helping differentiate recording sessions or group scenes.
   
2. "Base Directory for recordings" denotes the directory for your renamed files. A structured folder hierarchy is adopted for clarity: Base dir/Categorization code/Date recorded_Scene_Shot_Take.

4. Adjust the Scene, Shot, and Take numbers manually if needed. (Doesn't display current Shot/Scene number)

### Stream Deck Integration

1. On your Stream Deck, create a button to invoke the specific HTTP GET request from the above endpoints.
   
2. Once configured, the button press adjusts the respective scene, shot, or take numbers in OBS.
   
   ![Stream Deck Image](https://github.com/re-forgedpie/OBS-clapper/assets/97791696/6ef946fe-2548-4514-88c1-cbe033f4d4ef)

## Limitations

- **Feature Completion**: Some sections in `FilmSettings` class aren't fully functional yet. Navigating back to a previous scene or shot doesn't revert to the last known shot or take number.
  
- **HTTP Port Configuration**: The script binds to `localhost:8000`. Ensure no other service occupies this port, or consider modifying the script to use a different one.
  
- **Stream Deck UI Update**: The current scene, shot, or take numbers aren't displayed on the Stream Deck. Rely on memory or the "script log" for now.
  
- **Decrease Shortcut Limitation**: Shortcuts only exist for incrementing scene/shot/take. Decreasing is solely possible via the local webserver.

## Important Reminder

Before diving in, take a moment to back up your OBS settings and any vital data. It's always wise to prepare for unforeseen events.

## Licensing

`OBS-Clapper` is open-sourced under the GNU General Public License v3.0. Dive into the `LICENSE` file for all the details.

# img_viewer.py

import PySimpleGUI as sg
import os

# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Film:"),
        sg.In(size = (25, 1), enable_events = True, key = "-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events = True, size=(40, 5), key = "-FILE LIST-"
        )
    ],
    [
        sg.Text("Wybrany film:"),
        sg.Text(size = (40, 1), key = "-TOUT-")
    ],
    [
        sg.Text("Nazwa nowego pliku:"),
        sg.InputText(size = (22, 1), enable_events = True, key = '-NFNAME-'),
    ],    
    [
        sg.Text('Początek fragmentu:', size = (20, 1), key = '-START-'), 
        sg.InputText(size = (2, 1), enable_events = True, key = '-SHOUR-'),
        sg.Text(':'),
        sg.InputText(size = (2, 1), enable_events = True, key = '-SMINUTE-'),
        sg.Text(':'),
        sg.InputText(size = (2, 1), enable_events = True, key = '-SSECOND-'),
    ],
    [
        sg.Text('Koniec fragmentu:', size = (20, 1), key = '-END-'), 
        sg.InputText(size = (2, 1), enable_events = True, key = '-EHOUR-'),
        sg.Text(':'),
        sg.InputText(size = (2, 1), enable_events = True, key = '-EMINUTE-'),
        sg.Text(':'),
        sg.InputText(size = (2, 1), enable_events = True, key = '-ESECOND-'),
    ],
    [
        sg.Button('Wytnij fragment', size = (20, 1), key = '-CUT-')
    ],
    [
        sg.Text('', size = (40, 1), key = '-ERROR-')
    ]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
    ]
]

videoLengthSec = 0
videoLengthMin = 0
videoLengthHour = 0
fnames = []

def getVideoLength(filepath):
    command = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ' + filepath
    length = os.popen(command).read()
    length = float(length)
    length = int(length)
    return length

def updateTime(input):
    text = values[input]
    text = text[:2]
    try:
        number = float(text)
        if number > 59:
            text = '59'
        window['-ERROR-'].update('')
        return window[input].update(value = text)
    except:
        window['-ERROR-'].update('')
        window[input].update(value = text[:-1])
        
def updateFileName():
    folderpath = values["-FOLDER-"]
    filename = values["-FILE LIST-"][0]
    filepath = '"' + folderpath + '/' + filename + '"'
    window['-ERROR-'].update('')
    return filepath

def updateFilelist(folder):
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except:
        file_list = []
        
    fnames = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith((".mp4"))
        
    ]
    window['-ERROR-'].update('')
    return fnames

window = sg.Window("Program do cięcia filmów", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED: break
    
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        fnames = updateFilelist(values["-FOLDER-"])

        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filepath = updateFileName()
            window["-TOUT-"].update(filepath)
        except:
            pass
    elif event == "-SHOUR-":
        updateTime('-SHOUR-')
    elif event == "-SMINUTE-":
        updateTime('-SMINUTE-')
    elif event == "-SSECOND-":
        updateTime('-SSECOND-')
    elif event == "-EHOUR-":
        updateTime('-EHOUR-')
    elif event == "-EMINUTE-":
        updateTime('-EMINUTE-')
    elif event == "-ESECOND-":
        updateTime('-ESECOND-')
    elif event == "-CUT-":
        try:
            filepath = updateFileName()
            fileNewName = values['-NFNAME-']
            if fileNewName == '':
                raise Exception('Nie podano nazwy pliku')
            for f in fnames:
                if f == fileNewName + '.mp4':
                    raise Exception('Nazwa pliku już istnieje')
            start = values['-SHOUR-'] + ':' + values['-SMINUTE-'] + ':' + values['-SSECOND-']
            end = values['-EHOUR-'] + ':' + values['-EMINUTE-'] + ':' + values['-ESECOND-']
            os.system('ffmpeg -i ' + filepath + ' -ss ' + start + ' -to ' + end + ' -c copy ' + '"' + values['-FOLDER-'] + '/' + fileNewName + '.mp4"')
            fnames = updateFilelist(values["-FOLDER-"])
            window["-FILE LIST-"].update(fnames)
        except Exception as e:
            if e.args[0] == 'Nie podano nazwy pliku':
                error = "Nie podano nazwy pliku"
                window['-ERROR-'].update(error)
            elif e.args[0] == 'Nazwa pliku już istnieje':
                error = "Nazwa pliku już istnieje"
                window['-ERROR-'].update(error)
            elif e.args[0] == 'list index out of range':
                error = "Nie wybrano filmu"
                window['-ERROR-'].update(error)
            

window.close()
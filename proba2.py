import PySimpleGUI as sg

font = ('Courier New', 16)
text = '\n'.join(chr(i) * 50 for i in range(65, 250))
column = [[sg.Text(text, font=font)]]

layout = [
    [sg.Column(column, size=(800, 300), scrollable=True, key="Column")],
    [sg.OK(), sg.Button('Up', key="up"), sg.Button('Down', key="down")],
]

window = sg.Window('Demo', layout, finalize=True)
pos = 0.0
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "down":
        window['Column'].Widget.canvas.yview_moveto(1.0)
    elif event == "up":
        window['Column'].Widget.canvas.yview_moveto(0.0)

window.close()
'''
event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "down":
        pos += 0.1
        if pos > 0.9:
            pos = 0.9
        window['Column'].Widget.set_vscroll_position(pos)
    elif event == "up":
        pos -= 0.1
        if pos < 0:
            pos = 0.0
        window['Column'].Widget.canvas.yview_moveto(pos)
'''
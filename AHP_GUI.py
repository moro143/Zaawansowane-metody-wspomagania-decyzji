import PySimpleGUI as sg
import numpy as np

def change(a, i,j, n):
    a[i][j]=n
    a[j][i]=1/n

def ahp(pheromone_list):
    a = np.ones([len(pheromone_list),len(pheromone_list)])
    names = ['High stared atraction', 'High category preferences', 'Low price', 'High popularity']
    maxlen = 0
    for i in names:
        if len(i)>maxlen:
            maxlen=len(i)
    layout = [[sg.Text('Criteria preferences')]]
    text = []
    text1 = []
    text2 = []
    ij = []
    for i in range(len(names)-1):
        for j in range(i,len(names)):
            if i!=j:
                text1.append(names[i])
                text2.append(names[j])
                text.append(names[i]+names[j])
                ij.append([i,j])
    for i in range(len(text1)):
        layout.append([sg.Text(text1[i], size=(maxlen, 1)), sg.Slider((-100,100), key=text[i], orientation='h', enable_events=True, disable_number_display=True, default_value=0), sg.Text(text2[i], size=(maxlen, 1))])
    layout.append([sg.Button('Done')])
    window = sg.Window('Criteria preferences', layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Done':
            c=0
            for i in text:
                x = values[i]
                flag = True
                if x<0:
                    x = -x
                    flag = False
                x = x/100*8+1
                if flag:
                    change(a, ij[c][1], ij[c][0], x)
                else:
                    change(a, ij[c][1], ij[c][0], 1/x)
                c+=1
            window.close()
            return a

        

    
    

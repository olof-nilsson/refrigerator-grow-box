from tkinter import  Button
def keyPressed(keyWindow,button_width,button_height,key,entry,font,caps):
    if (key == 'Back'):
        entry.delete(entry.index("end") - 1)
    elif (key == 'Enter'):
        keyWindow.destroy()
    elif (key == 'Space'):
        entry.insert(len(entry.get())," ")
    elif (key == 'Capslock'):
        for o in keyWindow.winfo_children():
            o.destroy()
        createKeyBoard(keyWindow,button_width,button_height,font,entry,not caps)
    else:
        entry.insert(len(entry.get()),key)

def createKeyBoard(keyWindow,button_width,button_height,font,entry,caps):   
    keys=""
    if not caps:
        keys="1234567890+´" + chr(8) + chr(10)
        keys=keys+"qwertyuiopå^" + chr(10)
        keys=keys + "asdfghjklöä'" + chr(12) + chr(10)
        keys=keys+"<>zxcvbnm,.-" + chr(15)    + chr(10)
    else:
        keys="!" + chr(34) + "#¤%&/()=?`" + chr(8) + chr(10)
        keys=keys+"QWERTYUIOPÅ~" + chr(10)
        keys=keys + "ASDFGHJKLÖÄ*" + chr(12) + chr(10)
        keys=keys+"<>ZXCVBNM;:_" + chr(15)    + chr(10)

    keys=keys+chr(32)
    y=1
    x=0
    extra = 0
    lastbuttonY=0
    for p in range(len(keys)):
        x=x+1
        c=keys[p]
        if (keys[p]==chr(10)):
            y=y+1
            x=0
        else:
            if (keys[p]==chr(8)):
                c="Back"
                extra = 3
            if (keys[p]==chr(12)):
                c="Enter"
                extra = 3
            if (keys[p]==chr(15)):
                c="Capslock"
                extra = 5
            if (keys[p]==chr(32)):
                c="Space"
                extra=button_width * 18
                space=Button(keyWindow, text=c, command=lambda c=c:keyPressed(keyWindow,button_width,button_height,c,entry,font,caps), width = button_width + extra, height = button_height,font=font)
                space.place(x=10, y=y*(button_height*35))
            else:
                Button(keyWindow, text=c, command=lambda c=c:keyPressed(keyWindow,button_width,button_height,c,entry,font,caps), width = button_width + extra, height = button_height,font=font).grid(row = y, column=x,padx=0, pady=0)
            extra=0
import tkinter as tk
from mail import *
# Creating a class that will encase our GUI application
class HDDHealth(tk.Tk):
    '''
    The constructor defines all the main elements of our application such as-
    the window size, the title, all the frames that are a part of the application, 
    and initializing all these frames.
    '''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        self.allDevices = None

        h = '480'
        w = '360'
        self.geometry('{}x{}'.format(h,w))
        self.title('HDD Health')


        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        
        self.frames = {} 

        frameList = [PromptPage, DescriptionPage]

        for F in frameList:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.rowconfigure(0,weight=1)
            frame.columnconfigure(0,weight=1)
        
        self.showFrame(PromptPage)

    '''
    the below function raises the frame above all the other frames so that it becomes the primary frame 
    which the user can interact with.
    '''
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

'''
The classes shown below define each frame in our application which we initialized in the constructor of
HDDHealth. 
'''

class PromptPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mainLabel = tk.Label(self, text = "Click the button to get your hard drive's status.")
        scanButton = tk.Button(self, text="Get status", command=lambda:controller.main1())

        mainLabel.grid(row=0, column=0)
        scanButton.grid(row=1,column=0, pady=50)


class DescriptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        parent.allDevices = script.main()
        scrollbar = tk.Scrollbar(self)
        infoList = tk.Listbox(self,width=70,height=20, yscrollcommand = scrollbar.set)  


        for device in parent.allDevices.keys():
            infoList.insert(tk.END, str(device))

            infoList.insert(tk.END, 'Device information:')
            for field,value in parent.allDevices[device][0].items():
                infoList.insert(tk.END, str(field) + ' : '+ str(value))
            
            infoList.insert(tk.END, '')
            infoList.insert(tk.END, str(parent.allDevices[device][1]))

            infoList.insert(tk.END, '')
            infoList.insert(tk.END, 'Device attributes:')
            infoList.insert(tk.END, 'ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH')
            for field,value in parent.allDevices[device][2].items():
                infoList.insert(tk.END, "   ".join(str(el) for el in value[:6]))

            infoList.insert(tk.END, '')
            infoList.insert(tk.END, '')
        
        scrollbar.grid(row=0, column=1)
        infoList.grid(row=0, column=0)
        
# Creating an instance of our application class and then running it when the program runs.
if __name__ == '__main__':
    app = HDDHealth()
    app.mainloop()

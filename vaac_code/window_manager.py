'''This is the window manager module for vaac.'''
from collections import defaultdict
import ast
import subprocess
class WindowManager():
    def __init__(self,name_of_app_running_vaac):        
        print(name_of_app_running_vaac)
        self.id_of_app_running_vaac = (subprocess.getoutput("wmctrl -l | grep '"+name_of_app_running_vaac+"'")).split()[0]
        print("id",self.id_of_app_running_vaac)

        self.dims = {'gedit':['0','0','1450','618'],'firefox':['0','0','1366','519'],'vaac_terminal':['0','594','1366','174']}
        self.setdims()

        self.window_pointers = dict() #keeps pointers to window ids
        self.update_open_applications()
        #print("wm:",self.open_apps_dict)      
        
    def setdims(self):
        self.root_width = subprocess.getoutput("xwininfo -root | awk '/Width/'").split()[1]
        self.root_height= subprocess.getoutput("xwininfo -root | awk '/Height/'").split()[1]
        self.dims['vaac_terminal_height'] = '8'
        self.dims['vaac_terminal_width'] = '150'
        self.resize_vaac_terminal()

        vaac_window_x = subprocess.getoutput("xwininfo -id " + self.id_of_app_running_vaac + " | awk '/Absolute upper-left X/'").split()[-1]
        vaac_window_y = subprocess.getoutput("xwininfo -id " + self.id_of_app_running_vaac + " | awk '/Absolute upper-left Y/'").split()[-1]
        vaac_window_height = subprocess.getoutput("xwininfo -id " + self.id_of_app_running_vaac + " | awk '/Height/'").split()[-1]
        vaac_window_width = subprocess.getoutput("xwininfo -id " + self.id_of_app_running_vaac + " | awk '/Width/'").split()[-1]

        print("root width,height",self.root_width,self.root_height)
        print("vaac_window_width",vaac_window_width,vaac_window_height)
        print("vaac_window_x,y",vaac_window_x,vaac_window_y)
        
        #self.dims['gedit_height'] = str(int(self.root_height) - int(vaac_window_height)+12)
        #self.dims['gedit_width'] = str(int(self.root_width)+74)
        #self.dims['firefox_height'] = str(int(self.root_height) - int(vaac_window_height) -87)
        #self.dims['firefox_width'] = self.root_width
        #self.dims['gedit_height'] = '79.8%'
        #self.dims['gedit_width'] = '110%'
        #self.dims['firefox_height'] = '66.95%'
        #self.dims['firefox_width'] = '100%'
        
        self.dims['gedit_height'] = str(((float(self.root_height)-float(vaac_window_height))/float(self.root_height))*100+2)+"%"
        self.dims['gedit_width'] = '110%'
        self.dims['firefox_height'] = str(((float(self.root_height)-float(vaac_window_height))/float(self.root_height) - 0.11)*100)+"%"
        self.dims['firefox_width'] = '100%'
        
        print("self.dims",self.dims)

    def update_open_applications(self):
        self.setdims()
        print("In VaacWindowManager.update_open_applications() :Updating vaac.wm values.")
        string = ast.literal_eval(subprocess.getoutput("./vaac_code/running_apps.sh").lower())
        open_apps_dict = defaultdict(list)           
        for item in string:
            open_apps_dict[item['key']].append(item['value'])                        
        self.open_apps_dict = open_apps_dict

        add = set(self.open_apps_dict.keys()) - set(self.window_pointers.keys())
        remove =  set(self.window_pointers.keys()) - set(self.open_apps_dict.keys())
        for item in add:
            self.window_pointers[item] = 0
        for item in remove:
            del self.window_pointers[item]

    def resize_vaac_terminal(self):
        subprocess.run(['wmctrl', '-ir', self.id_of_app_running_vaac, '-b', 'remove,maximized_vert,maximized_horz'])
        subprocess.run(['xdotool','windowsize','--usehints',self.id_of_app_running_vaac,self.dims['vaac_terminal_width'],self.dims['vaac_terminal_height']])
        subprocess.run(['xdotool', 'windowmove', self.id_of_app_running_vaac, 'x', self.root_height])

    def resize_all(self):
        print("Resizing all windows.")
        window_currently_focused = (subprocess.getoutput("xdotool getactivewindow"))
        self.update_open_applications()
        for item in self.open_apps_dict.keys():
            for id in self.open_apps_dict[item]:
                #print("working on",item,id,str(self.id_of_app_running_vaac))
                if id != str(self.id_of_app_running_vaac):
                    if item in ['gedit','nautilus']:
                        subprocess.run(['wmctrl', '-ir', id, '-b', 'remove,maximized_vert,maximized_horz'])
                        subprocess.run(['xdotool', 'windowmove', id,'0','0','windowsize',id,self.dims['gedit_width'],self.dims['gedit_height']])
                    else:
                        subprocess.run(['wmctrl', '-ir', id, '-b', 'remove,maximized_vert,maximized_horz'])
                        subprocess.run(['xdotool', 'windowmove', id,'0','0', 'windowsize', id,self.dims['firefox_width'],self.dims['firefox_height']])
                else:
                    self.resize_vaac_terminal()
                    
        subprocess.run(["xdotool", "windowactivate",window_currently_focused])
    
    def focus(self,s):
        #self.update_open_applications()
        if s in self.open_apps_dict:
            subprocess.run(['xdotool', 'windowactivate',str(self.open_apps_dict[s][self.window_pointers[s]])])
            #self.update_index(s)
        else:
            print("WindowManager:",s,"is not open to be focused.")

    def update_index(self, string):
        self.window_pointers[string] += 1
        if self.window_pointers[string] == len(self.open_apps_dict[string]):
            self.window_pointers[string] = 0
    
    def check_if_open(self,s):
        self.update_open_applications()
        return s in self.open_apps_dict.keys()            

    def get_open_apps(self):
        self.update_open_applications()
        return self.open_apps_dict.keys()

    def get_window_ids(self,s):
        return self.open_apps_dict[s]
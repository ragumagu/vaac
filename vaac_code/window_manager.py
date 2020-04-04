#Eighty characters*************************************************************#
'''This is the window manager module for vaac.'''
from collections import defaultdict
import ast
import subprocess
import time
class WindowManager():
    def __init__(self,vaac_window_title):
        self.vaac_window_id = self.get_vaac_window_id(vaac_window_title)
        print("Vaac window id",self.vaac_window_id)
        self.vaac_terminal_width = '150'
        self.vaac_terminal_height = '8'

        # Ssd - server side decorations
        # Ssd applications have borders drawn by the host window manager.
        self.ssd_applications = ['code','firefox','gnome-terminal']
        self.ssd_app_width = '100%'
        
        # Csd - client side decorations
        # Csd applications provide their own borders; csd and ssd window
        # height calculations need to be separated.
        self.csd_applications = ['gedit','nautilus']
        self.csd_app_width = '110%'
        
        # You can fine tune the errors to optimize window heights.
        self.ssd_app_error_percent = -11
        self.csd_app_error_percent = 2

        self.window_pointers = dict() #keeps pointers to window ids
        self.update_apps_windows()
        self.set_root_window_dims()        
        self.find_target_dims()
        self.window_dims = self.get_window_dims_dict()
        
        
        #self.update_window_pointers()

    def cycle_index(self, app):
        self.window_pointers[app] += 1
        if self.window_pointers[app] == len(self.apps_windows_dict[app]):
            self.window_pointers[app] = 0

    def check_if_open(self,app):
        self.update_apps_windows() #Possible spaghetti
        return app in self.apps_windows_dict.keys()

    def get_open_apps(self):
        self.update_apps_windows() #Possible spaghetti
        return self.apps_windows_dict.keys()

    def get_window_ids(self,s):
        return self.apps_windows_dict[s]

    def get_vaac_window_id(self,name_of_app_running_vaac):
        command = "wmctrl -l | grep '"+name_of_app_running_vaac+"'"
        output = subprocess.getoutput(command)
        id = output.split()[0]
        return id

    def update_apps_windows(self):
        print("WindowManager:Updating wm values.")
        command = "./vaac_code/running_apps.sh"
        #time.sleep(0.5) #Remove this
        output_string = subprocess.getoutput(command).lower()
        print("wm.update_apps_windows got output_string",flush=True)
        print(output_string)
        output_string = output_string.split("\n")[-1]
        try:
            output = ast.literal_eval(output_string)
            apps_windows_dict = defaultdict(list)        
            for item in output:
                apps_windows_dict[item['key']].append(item['value'])            
            self.apps_windows_dict = apps_windows_dict
            self.update_window_pointers() #Possible spaghetti
        except:
            print("update_apps_windows: Got an invalid string.")
        

    def update_window_pointers(self):
        A = set(self.apps_windows_dict.keys())
        B = set(self.window_pointers.keys())
        add = A.difference(B)
        remove = B.difference(A)
        for item in add:
            self.window_pointers[item] = 0
        for item in remove:
            del self.window_pointers[item]
        print("wm.update_window_pointers,",self.window_pointers)
        
    def get_window_dims(self,win_id):
        command = "xwininfo -id "+win_id+" | awk '/Absolute upper-left X/||/Absolute upper-left Y/||/Width/||/Height/'"
        dims = subprocess.getoutput(command).split("\n")
        ulx = dims[0].split()[3]
        uly = dims[1].split()[3]
        width = dims[2].split()[1]
        height = dims[3].split()[1]
        return [ulx,uly,width,height]

    def set_root_window_dims(self):
        #root_window_id = self.apps_windows_dict['root_window'][0]
        #root_dims = self.get_window_dims(root_window_id)
        root_window_id = subprocess.getoutput('xwininfo -root | grep "Window id" | cut -d" " -f4')
        root_dims = self.get_window_dims(root_window_id)
        self.root_window_width = root_dims[2]
        self.root_window_height = root_dims[3]

    def find_target_dims(self):
        target_dims = dict()        
        self.resize_vaac_window() #Possible spaghetti
        vaac_terminal_dims = self.get_window_dims(self.vaac_window_id)
        vaac_window_height = float(vaac_terminal_dims[3])
        root_window_height = float(self.root_window_height)
        diff = root_window_height - vaac_window_height
        
        percentage = ((diff/root_window_height)*100)
        csd_height = percentage + self.csd_app_error_percent
        ssd_height = percentage + self.ssd_app_error_percent

        target_dims['csd_height'] = str(csd_height)+"%"
        target_dims['csd_width'] = self.csd_app_width

        target_dims['ssd_height'] = str(ssd_height)+"%"
        target_dims['ssd_width'] = self.ssd_app_width
        
        print("wm.find_target_dims:",target_dims)
        self.target_dims = target_dims

    def resize_vaac_window(self):
        commands = []
        cmd0 = ['wmctrl', '-ir', self.vaac_window_id, '-b', 'remove,maximized_vert,maximized_horz']
        commands.append(cmd0)
        cmd1= ['xdotool','windowsize','--usehints',self.vaac_window_id,self.vaac_terminal_width,self.vaac_terminal_height]
        commands.append(cmd1)
        cmd2 = ['xdotool', 'windowmove', self.vaac_window_id, 'x', self.root_window_height]
        commands.append(cmd2)
        for cmd in commands:
            subprocess.run(cmd)

    def get_window_dims_dict(self):
        self.update_apps_windows() #probable spaghetti
        window_dims_dict = dict()        
        for win_id_list in self.apps_windows_dict.values():
            for win_id in win_id_list:                
                window_dims_dict[win_id] = self.get_window_dims(win_id)
        #print(window_dims_dict)
        return window_dims_dict

    def focus(self,target_app):
        #self.update_apps_windows()
        if target_app in self.apps_windows_dict:
            pointer = self.window_pointers[target_app]
            target_win_id = str(self.apps_windows_dict[target_app][pointer])
            command = ['xdotool', 'windowactivate',target_win_id]
            subprocess.run(command)
            #self.update_index(s)
        else:
            print("WindowManager:",target_app,"is not open to be focused.")
    
    def check_if_window_sizes_has_changed(self):
        dic = self.get_window_dims_dict()
        print("Checking if the following are same:")
        print("Old:",self.window_dims)
        print("New:",dic)
        if dic == self.window_dims:
            print("same")
            return False
        else:
            print("different")
            return True
    
    def resize_if_windows_changed(self):
        if self.check_if_window_sizes_has_changed(): #Possible spaghetti
            self.resize_all() #Possible spaghetti
            

    def resize_all(self):              
        window_currently_focused = (subprocess.getoutput("xdotool getactivewindow"))
        print("wm.resize_all:window_currently_focused",window_currently_focused)
        #self.update_apps_windows()
        self.find_target_dims() #Possible spaghetti
        commands = []                
        csd = [self.target_dims['csd_width'],self.target_dims['csd_height']]
        ssd = [self.target_dims['ssd_width'],self.target_dims['ssd_height']]
        for item in self.apps_windows_dict.keys():
            if item != "root_window":
                for id in self.apps_windows_dict[item]:                   
                    if id != str(self.vaac_window_id):                    
                        cmd0 = ['wmctrl', '-ir', id, '-b', 'remove,maximized_vert,maximized_horz']
                        cmd1 = ['xdotool','windowmove',id,'0','0','windowsize',id]
                        commands.append(cmd0)
                        if item in self.csd_applications:
                            commands.append(cmd1+csd)
                        else:
                            commands.append(cmd1+ssd)
                    else:
                        self.resize_vaac_window()
        print("Resize running commands:")                             
        for cmd in commands:
            print(cmd)
            subprocess.run(cmd)   
        
        subprocess.run(["xdotool", "windowactivate",window_currently_focused])
    
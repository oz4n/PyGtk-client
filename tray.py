'''
Created on 16 juin 2011

@author: cx42
'''

import pygtk
pygtk.require('2.0')
import gtk

import os
import pynotify
import urllib2
import simplejson
import MultipartPostHandler

class LitchInTray:
    def __init__(self):
        pynotify.init ("Litch.in")
        
        self.__read_properties()
        
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_file(os.getcwd() + "/images/icon32.png") # set from image icon
    
        menu = gtk.Menu()
    
        areaMenu = gtk.MenuItem(label="Take an area")
        areaMenu.connect('activate', self.take_action, self.statusIcon, "area")
        
        currentMenu = gtk.MenuItem(label="Take an open window")
        currentMenu.connect('activate', self.take_action, self.statusIcon, "window")
        
        screenMenu = gtk.MenuItem(label="Take the whole screen")
        screenMenu.connect('activate', self.take_action, self.statusIcon, "screen")
        
        quitMenu = gtk.MenuItem(label="Quit")
        quitMenu.connect('activate', self.quit, self.statusIcon)
        
        menu.append(areaMenu)
        menu.append(currentMenu)
        menu.append(screenMenu)
        menu.append(quitMenu)
    
        self.statusIcon.connect('activate', self.take_action, menu, "area")
        self.statusIcon.connect('popup-menu', self.popup_menu, menu)
    
        #self.statusIcon.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    
        self.statusIcon.set_visible(True)
    
        gtk.main()
    
    def __read_properties(self):
        basedir = os.path.expanduser('~') + '/.litchin/'
        config_file = basedir + 'conf.json'
        
        if not os.path.exists(basedir):
            os.mkdir(basedir)

        if not os.path.exists(config_file):
            config = {
                'server': 'http://litch.in/',
                'user_token': '',
                'proxy': ''
            }
            f = open(config_file, 'w')
            f.write(simplejson.dumps(config, indent=True))
        else:
            f = open(config_file, 'r')
            config = simplejson.loads(f.read())
        
        f.close()
        
        self.server = config['server']
        self.user_token = config['user_token']
        self.proxy = config['proxy']

    def __file_exists(self, path):
        """
        Based on http://stackoverflow.com/questions/82831/how-do-i-check-if-a-file-exists-using-python
        """
        try:
            open(path)
            return True
        except:
            return False

    def __get_path(self):
        i = 0
        while(True):
            path = "/tmp/shot%s.png" % (i,)
            if not self.__file_exists(path):
                return path
            i += 1

    def __show_message(self, title, message):
        n = pynotify.Notification(title, message, "new-email")
        n.set_urgency(pynotify.URGENCY_NORMAL)
        n.set_timeout(pynotify.EXPIRES_NEVER)
        n.show()

    def take_action(self, widget, event, data = None):
        if self.user_token == '':
            self.__show_message("User Token Required", "You first need to define your user_token in the .litchin/conf.json file.")
            return
        
        file_path = self.__get_path()
        
        if data == "screen":
            os.system("sleep 0.5 && import -window root %s" % (file_path,))
        elif data == "window":
            os.system("import -frame %s" % (file_path,))
        elif data == "area" or not data:
            os.system("sleep 0.2 && import %s" % (file_path,))
        
        if not self.__file_exists(file_path):
            self.__show_message("Error occured", "An error occured while creating the file.")
            return

        params = {'token': self.user_token, 'image': open(file_path, 'rb')}

        opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request(self.server, params)

        if self.proxy != "":
            req.set_proxy(self.proxy, 'http')

        response = simplejson.loads(urllib2.urlopen(req).read().strip())

        if response['success']:
            clipboard = gtk.clipboard_get()
            clipboard.set_text(response['url'])
            clipboard.store()
            self.__show_message("Copied", "The url has been copied into your clipboard.")
        else:
            self.__show_message("Error", response['message'])

    def quit(self, widget, event, data = None):
        gtk.main_quit()

    def popup_menu(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

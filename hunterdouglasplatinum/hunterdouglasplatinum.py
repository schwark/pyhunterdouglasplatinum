# adapted from https://github.com/tannewt/agohunterdouglas/agohunterdouglas.py
# license from that project included in this repo as well

import socket
import re
import logging
import time

logging.basicConfig(level=logging.INFO)
class HunterDouglasPlatinumHub:
    """
    Hub class for the Hunter Douglas Platinum - for all hub interactions

    ...

    Attributes
    ----------
    ip : str
        a string representing the ip address of the hub
    port : int, optional
        the port number of the hub - defaults to 522
    timeout : int, optional
        the timeout value (in seconds) to use for socket communications to hub, defaults to 10s        

    Methods
    -------
    get_shade(name=None, id=None)
        Returns a HunterDouglasPlatinumShade object for the shade with name or id
    get_scene(name=None, id=None)
        Returns a HunterDouglasPlatinumScene object for the shade with name or id
    get_room(name=None, id=None)
        Returns a HunterDouglasPlatinumRoom object for the shade with name or id
    """


    def __init__(self, ip, port=522, timeout=10):
        self.ip = ip
        self.port = port
        self.timeout = 10
        self.rooms = {}
        self.scenes = {}
        self.shades = {}
        self.update()

    def discover(self):
        pass

    def create_socket(self):
        try:
            sock = socket.create_connection((self.ip, self.port), timeout=self.timeout)
            helo = self.recv_until(sock, 'Shade Controller')
        except socket.error:
            sock.close()
            sock = None
        return sock

    def recv_until(self, sock, sentinel=None):
        info = ""
        while True:
            try:
                chunk = sock.recv(1)
            except socket.timeout:
                logging.debug('socket timeout')
                break
            info += chunk.decode('cp437')
            logging.debug('info is now '+info)
            if info.endswith(sentinel): break
            if not chunk: break
        return info
        
    def send_command(self, message, sentinel=None, sock=None):
        content = None
        try:
            if not sock:
                sock = self.create_socket()
                sock.sendall(message.encode())
                content = self.recv_until(sock, sentinel)
        except socket.error:
            pass
        finally:
            if sock:
                sock.close()
        return content

    def is_alive(self,sock):
        return self.send_command("$dmy", "ack", sock)

    def update(self):
        logging.info('updating state...')
        info = self.send_command("$dat", "upd01-")
        if not info:
            msg = "Unable to get data about windows and scenes from Gateway"
            return msg

        prefix = None
        lines = re.split(r'[\n\r]+', info)

        for line in lines:
            line = line.strip()
            if not prefix:
                prefix = line[:2]
            elif not line.startswith(prefix):
                continue
            else:
                line = line[2:]

            if line.startswith("$cr"):
                # name of room
                room_id = line[3:5]
                room_name = line.split('-')[-1].strip()
                if(not room_name in self.rooms):
                    self.rooms[room_name] = HunterDouglasPlatinumRoom(hub=self, name=room_name, id=int(room_id))
            elif line.startswith("$cm"):
                # name of scene
                scene_id = line[3:5]
                scene_name = line.split('-')[-1].strip()
                if(not scene_name in self.scenes):
                    self.scenes[scene_name] = HunterDouglasPlatinumScene(hub=self, name=scene_name, id=int(scene_id))
            elif line.startswith("$cs"):
                # name of a shade
                parts = line.split('-')
                shade_id = line[3:5]
                shade_name = parts[-1].strip()
                room_id = parts[1]
                if(not shade_name in self.shades):
                    self.shades[shade_name] = HunterDouglasPlatinumShade(hub=self, name=shade_name, id=int(shade_id), room=int(room_id))
            elif line.startswith("$cp"):
                # state of a shade
                shade_id = line[3:5]
                state = line[-4:-1]
                state = int(state)
                shade = self.get_shade(id=int(shade_id))
                logging.debug('updating shade state for shade '+shade_id+' to '+str(state)+' for shade '+str(shade))
                if shade:
                    shade.set_state(state)
        return True

    def get_shade(self, name=None, id=None):
        if(name):
            return self.shades[name] if name in self.shades else None
        if(id):
            return next((v for (k,v) in self.shades.items() if v.id == id), None)
        return None    
        
    def get_scene(self, name=None, id=None):
        if(name):
            return self.scenes[name] if name in self.scenes else None
        if(id):
            return next((v for (k,v) in self.scenes.items() if v.id == id), None)
        return None    
        
    def get_room(self, name=None, id=None):
        if(name):
            return self.rooms[name] if name in self.rooms else None
        if(id):
            return next((v for (k,v) in self.rooms.items() if v.id == id), None)
        return None    
        

class HunterDouglasPlatinumShade:
    """
    Shade class for the Hunter Douglas Platinum - for all shade interactions

    ...

    Attributes
    ----------
    hub : HunterDouglasPlatinumHub
        a hub controller object to which the Shade is connected
    id : int
        the id of this shade on the controller
    name : str
        the name of the shade on the controller
    room : int
        the room id of this shade on the controller
    state : int
        the current level of the shade (number from 0-255)


    Methods
    -------
    set_level(hd_value)
        Moves the shade to specified position - can be a percentage integer, or the values 'up' or 'down'
    open()
        Opens the Shade - convenience function that wraps set_level
    close()
        Closes the Shade - convenience function that wraps set_level
    is_level(hd_value)
        Checks if shade is in specified position - can be a percentage integer, or the values 'up' or 'down'
    is_up()
        Checks if shade is up - convenience function that wraps is_level
    is_down()
        Checks if shade is down - convenience function that wraps is_level
    """


    def __init__(self, hub, id, name, room):
        self.hub = hub
        self.id = id
        self.name = name
        self.room = room
        self.state = 0

    def __str__(self):
        return 'HunterDouglasPlatinumShade: '+self.name+' id: '+str(self.id)+' room: '+str(self.room)

    def set_state(self, state):
        self.state = state

    def move_shade(self, move_value):
        content = self.hub.send_command("$pss%s-04-%03d" % (self.id, move_value), "done")
        content += self.hub.send_command("$rls", "act00-00-")
        return content

    def set_level(self, hd_value):
        if "up" == hd_value:
            move_value = 255
        elif "down" == hd_value:
            move_value = 0
        else:
            if hd_value.isdigit():
                move_value = min(int(round(int(hd_value)*255.0/100)),255)
            else:
                move_value = -1
        if 0 > move_value or 255 < move_value:
            return None

        num_tries = 0
        while(not self.is_level(hd_value) and num_tries < 3):
            logging.info('moving shade to '+hd_value+' try # '+str(num_tries+1))
            self.move_shade(move_value)
            time.sleep(20)
            self.hub.update()
            num_tries += 1

        return num_tries < 3

    def open(self):
        self.set_level('up')

    def close(self):
        self.set_level('down')

    def is_up(self):
        return self.is_level('up')

    def is_down(self):
        return self.is_level('down')

    def is_level(self, state):
        logging.info('checking state '+state+' against self '+str(self.state))
        result = False
        if('up' == state):
            result = (self.state == 255)
        elif('down' == state):
            result = (self.state == 0)
        elif(state.isdigit()):
            state = int(state)
            result = (abs(self.state - int(255*state/100)) < 2)
        return result


class HunterDouglasPlatinumScene:
    """
    Scene class for the Hunter Douglas Platinum - for all scene interactions

    ...

    Attributes
    ----------
    hub : HunterDouglasPlatinumHub
        a hub controller object to which the Shade is connected
    id : int
        the id of this scene on the controller
    name : str
        the name of the scene on the controller


    Methods
    -------
    run()
        Runs the Scene
    """

    def __init__(self, hub, id, name):
        self.hub = hub
        self.id = id
        self.name = name
  
    def run(self):
        return self.hub.send_command("$inm%s-" % (self.id), "act00-00-")

class HunterDouglasPlatinumRoom:
    """
    Room class for the Hunter Douglas Platinum - for all scene interactions

    ...

    Attributes
    ----------
    hub : HunterDouglasPlatinumHub
        a hub controller object to which the Shade is connected
    id : int
        the id of this room on the controller
    name : str
        the name of the room on the controller

    """

    def __init__(self, hub, id, name):
        self.hub = hub
        self.id = id
        self.name = name
  
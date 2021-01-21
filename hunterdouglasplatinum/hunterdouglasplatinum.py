# adapted from https://github.com/tannewt/agohunterdouglas/agohunterdouglas.py
# license from that project included in this repo as well

import socket
import re
import logging

class HunterDouglasPlatinumHub:
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
        
    def socket_com(self, message, sentinel=None, sock=None):
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
        return self.socket_com("$dmy", "ack", sock)

    def update(self):
        info = self.socket_com("$dat", "upd01-")
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
                self.rooms[room_name] = HunterDouglasPlatinumRoom(hub=self, name=room_name, id=room_id)
            elif line.startswith("$cm"):
                # name of scene
                scene_id = line[3:5]
                scene_name = line.split('-')[-1].strip()
                self.scenes[scene_name] = HunterDouglasPlatinumScene(hub=self, name=scene_name, id=scene_id)
            elif line.startswith("$cs"):
                # name of a shade
                parts = line.split('-')
                shade_id = line[3:5]
                shade_name = parts[-1].strip()
                room_id = parts[1]
                self.shades[shade_name] = HunterDouglasPlatinumShade(hub=self, name=shade_name, id=shade_id, room=room_id)
            elif line.startswith("$cp"):
                # state of a shade
                shade_id = line[3:5]
                state = line[-4:-1]
                state = str(int((int(state) / 255.) * 16))
                shade = self.get_shade_by_id(shade_id)
                if shade:
                    shade.set_state(state)
        return True

    def get_shade_by_id(self, id):
        return next((v for (k,v) in self.shades.items() if v.id == id), None)

    def get_shade(self, name):
        return self.shades[name] if name in self.shades else None
        
    def get_scene(self, name):
        return self.scenes[name] if name in self.scenes else None
        
    def get_room(self, name):
        return self.rooms[name] if name in self.rooms else None
        

class HunterDouglasPlatinumShade:
    def __init__(self, hub, id, name, room):
        self.hub = hub
        self.id = id
        self.name = name
        self.room = room
        self.state = 0

    def __str__(self):
        return 'HunterDouglasPlatinumShade: '+self.name+' id: '+self.id+' room: '+self.room

    def set_state(self, state):
        self.state = state

    def set_level(self, hd_value):
        if "up" == hd_value:
            hd_value = 255
        elif "down" == hd_value:
            hd_value = 0
        else:
            if hd_value.isdigit():
                hd_value = min(int(round(int(hd_value)*255.0/100)),255)
            else:
                hd_value = -1
        
        if 0 > hd_value or 255 < hd_value:
            return None

        content = self.hub.socket_com("$pss%s-04-%03d" % (self.id, hd_value), "done")
        return content + self.hub.socket_com("$rls", "act00-00-")

    def open(self):
        self.set_level('up')

    def close(self):
        self.set_level('down')


class HunterDouglasPlatinumScene:
    def __init__(self, hub, id, name):
        self.hub = hub
        self.id = id
        self.name = name
  
    def run(self):
        return self.hub.socket_com("$inm%s-" % (self.id), "act00-00-")

class HunterDouglasPlatinumRoom:
    def __init__(self, hub, id, name):
        self.hub = hub
        self.id = id
        self.name = name
  
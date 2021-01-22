# adapted from https://github.com/tannewt/agohunterdouglas/agohunterdouglas.py
# license from that project included in this repo as well

import socket
import re
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)

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

    """

    def __init__(self, ip, port=522, timeout=10):
        self.ip = ip
        self.port = port
        self.timeout = 10
        self.rooms = {}
        self.scenes = {}
        self.shades = {}

    @classmethod
    async def create(cls, ip, port=522, timeout=10):
        """
        Class method for the creation of the HunterDouglasPlatinumHub - use this for proper initialization instead of new

        ...

        Attributes
        ----------
        ip : str
            a string representing the ip address of the hub
        port : int, optional
            the port number of the hub - defaults to 522
        timeout : int, optional
            the timeout value (in seconds) to use for socket communications to hub, defaults to 10s        

        """

        hub = HunterDouglasPlatinumHub(ip, port, timeout)
        await hub.update()
        return hub
        
    async def send_command(self, message, sentinel=None):
        """
            Sends a command to the controller and reads response till sentinel.
       
            ...
            
            Parameters
            ----------
            message : str
                Message to send to controller            
            sentinel : str, optional
                Ending sentinel phrase to look for to end reading of response
            
            Returns
            -------
            Response from the controller : str
        """
 
        content = None
        reader = None
        writer = None
        try:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
            await reader.readuntil('Shade Controller'.encode())
            writer.write(message.encode())
            await writer.drain()
            content = await reader.readuntil(sentinel.encode())
            content = content.decode('cp437')
        except Exception as e:
            logging.error('Socket error '+str(e))
        finally:
            if(writer):
                writer.close()
                await writer.wait_closed()
        return content

    async def update(self):
        """
            Updates the current state of the controller and shades and scenes
       
            ...
                    
            Returns
            -------
            Error message if applicable else empty : str
        """
 
        logging.info('updating state...')
        info = await self.send_command("$dat", "upd01-")
        if not info:
            msg = "Unable to get data about windows and scenes from Gateway"
            return msg

        logging.debug('hub response is :')
        logging.debug(info)
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
                    logging.debug('creating room '+room_name)
                    self.rooms[room_name] = HunterDouglasPlatinumRoom(hub=self, name=room_name, id=int(room_id))
            elif line.startswith("$cm"):
                # name of scene
                scene_id = line[3:5]
                scene_name = line.split('-')[-1].strip()
                if(not scene_name in self.scenes):
                    logging.debug('creating scene '+scene_name)
                    self.scenes[scene_name] = HunterDouglasPlatinumScene(hub=self, name=scene_name, id=int(scene_id))
            elif line.startswith("$cs"):
                # name of a shade
                parts = line.split('-')
                shade_id = line[3:5]
                shade_name = parts[-1].strip()
                room_id = parts[1]
                if(not shade_name in self.shades):
                    logging.debug('creating shade '+shade_name)
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
        return ""

    def get_shade(self, name=None, id=None, room=None):
        """
            Returns a shade or list of shades by id, name or room.
       
            ...
            
            Parameters
            ----------
            name : str, optional
                Name of shade to find            
            id : int, optional
                Id of shade to find
            room : int, optional
                Room Id of shade(s) to find
            
            Returns
            -------
            A shade or list of shades : [] or HunterDouglasPlatinumShade
        """
 
        if(name):
            return self.shades[name] if name in self.shades else None
        if(id):
            return next((v for (k,v) in self.shades.items() if v.id == id), None)
        if(room):
            return [value for (key, value) in self.shades.items() if value.room == room]
        return None    
        
    def get_scene(self, name=None, id=None):
        """
            Returns a scene by id, name.
       
            ...
            
            Parameters
            ----------
            name : str, optional
                Name of scene to find            
            id : int, optional
                Id of scene to find
            
            Returns
            -------
            A scene : HunterDouglasPlatinumScene
        """

        if(name):
            return self.scenes[name] if name in self.scenes else None
        if(id):
            return next((v for (k,v) in self.scenes.items() if v.id == id), None)
        return None    
        
    def get_room(self, name=None, id=None):
        """
            Returns a room by id, name.
       
            ...
            
            Parameters
            ----------
            name : str, optional
                Name of room to find            
            id : int, optional
                Id of room to find
            
            Returns
            -------
            A room : HunterDouglasPlatinumRoom
        """
        
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

    async def __move_shade(self, move_value):
        content = await self.hub.send_command("$pss%s-04-%03d" % (self.id, move_value), "done")
        content += await self.hub.send_command("$rls", "act00-00-")
        return content

    async def set_level(self, hd_value):
        """
            Moves a shade to a certain level
       
            ...
            
            Parameters
            ----------
            hd_value : str or int
                One of 'up', 'down' or number percentage open      
            
            Returns
            -------
            success : bool
        """
        
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
            await self.__move_shade(move_value)
            await asyncio.sleep(20)
            await self.hub.update()
            num_tries += 1

        return num_tries < 3

    def open(self):
        """
            Moves a shade to open state
       
            ...
            
            
            Returns
            -------
            success : bool
        """
        
        return self.set_level('up')

    def close(self):
        """
            Moves a shade to closed state
       
            ...
            
            
            Returns
            -------
            success : bool
        """
        
        return self.set_level('down')

    def is_up(self):
        """
            Checks if shade is up
       
            ...
            
            
            Returns
            -------
            is_up : bool
        """
        
        return self.is_level('up')

    def is_down(self):
        """
            Checks if shade is down
       
            ...
            
            
            Returns
            -------
            is_down : bool
        """
        
        return self.is_level('down')

    def is_level(self, state):
        """
            Checks if shade is at a certain level
       
            ...
            
            Parameters
            ----------
            hd_value : str or int
                One of 'up', 'down' or number percentage open      
            
            Returns
            -------
            if it is at stated level : bool
        """
        
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

    """

    def __init__(self, hub, id, name):
        self.hub = hub
        self.id = id
        self.name = name
  
    async def run(self):
        """
            Runs the scene
       
            ...
                        
            Returns
            -------
            response message : str
        """
        
        return await self.hub.send_command("$inm%s-" % (self.id), "act00-00-")

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

    def get_shades(self):
        return self.hub.get_shade(room=self.id)
  
Module hunterdouglasplatinum.hunterdouglasplatinum
==================================================

Classes
-------

`HunterDouglasPlatinumHub(ip, port=522, timeout=10)`
:   Hub class for the Hunter Douglas Platinum - for all hub interactions
    
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
    get_shade(name=None, id=None, room=None)
        Returns a HunterDouglasPlatinumShade object for the shade with name or id, or all shades from room with room id
    get_scene(name=None, id=None)
        Returns a HunterDouglasPlatinumScene object for the shade with name or id
    get_room(name=None, id=None)
        Returns a HunterDouglasPlatinumRoom object for the shade with name or id

    ### Methods

    `create_socket(self)`
    :

    `discover(self)`
    :

    `get_room(self, name=None, id=None)`
    :

    `get_scene(self, name=None, id=None)`
    :

    `get_shade(self, name=None, id=None, room=None)`
    :

    `is_alive(self, sock)`
    :

    `recv_until(self, sock, sentinel=None)`
    :

    `send_command(self, message, sentinel=None, sock=None)`
    :

    `update(self)`
    :

`HunterDouglasPlatinumRoom(hub, id, name)`
:   Room class for the Hunter Douglas Platinum - for all scene interactions
    
    ...
    
    Attributes
    ----------
    hub : HunterDouglasPlatinumHub
        a hub controller object to which the Shade is connected
    id : int
        the id of this room on the controller
    name : str
        the name of the room on the controller

    ### Methods

    `get_shades(self)`
    :

`HunterDouglasPlatinumScene(hub, id, name)`
:   Scene class for the Hunter Douglas Platinum - for all scene interactions
    
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

    ### Methods

    `run(self)`
    :

`HunterDouglasPlatinumShade(hub, id, name, room)`
:   Shade class for the Hunter Douglas Platinum - for all shade interactions
    
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

    ### Methods

    `close(self)`
    :

    `is_down(self)`
    :

    `is_level(self, state)`
    :

    `is_up(self)`
    :

    `move_shade(self, move_value)`
    :

    `open(self)`
    :

    `set_level(self, hd_value)`
    :

    `set_state(self, state)`
    :
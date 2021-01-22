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

    ### Static methods

    `create(ip, port=522, timeout=10)`
    :   Class method for the creation of the HunterDouglasPlatinumHub - use this for proper initialization instead of new
        
        ...
        
        Attributes
        ----------
        ip : str
            a string representing the ip address of the hub
        port : int, optional
            the port number of the hub - defaults to 522
        timeout : int, optional
            the timeout value (in seconds) to use for socket communications to hub, defaults to 10s

    ### Methods

    `get_room(self, name=None, id=None)`
    :   Returns a room by id, name.
        
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

    `get_scene(self, name=None, id=None)`
    :   Returns a scene by id, name.
        
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

    `get_shade(self, name=None, id=None, room=None)`
    :   Returns a shade or list of shades by id, name or room.
        
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

    `send_command(self, message, sentinel=None)`
    :   Sends a command to the controller and reads response till sentinel.
        
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

    `update(self)`
    :   Updates the current state of the controller and shades and scenes
        
        ...
                
        Returns
        -------
        Error message if applicable else empty : str

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

    ### Methods

    `run(self)`
    :   Runs the scene
        
        ...
                    
        Returns
        -------
        response message : str

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

    ### Methods

    `close(self)`
    :   Moves a shade to closed state
        
        ...
        
        
        Returns
        -------
        success : bool

    `is_down(self)`
    :   Checks if shade is down
        
        ...
        
        
        Returns
        -------
        is_down : bool

    `is_level(self, state)`
    :   Checks if shade is at a certain level
        
        ...
        
        Parameters
        ----------
        hd_value : str or int
            One of 'up', 'down' or number percentage open      
        
        Returns
        -------
        if it is at stated level : bool

    `is_up(self)`
    :   Checks if shade is up
        
        ...
        
        
        Returns
        -------
        is_up : bool

    `open(self)`
    :   Moves a shade to open state
        
        ...
        
        
        Returns
        -------
        success : bool

    `set_level(self, hd_value)`
    :   Moves a shade to a certain level
        
        ...
        
        Parameters
        ----------
        hd_value : str or int
            One of 'up', 'down' or number percentage open      
        
        Returns
        -------
        success : bool

    `set_state(self, state)`
    :
import time


class ReadOnlyDotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = None
    __delattr__ = None

    def __setattr__(self, k, v):
        raise RuntimeError('Read Only')

    def __setitem__(self, k, v):
        raise RuntimeError('Read Only')


class Device:
    """ Device represesnt a resource
    """

    def __init__(self, dev_info, device_pool):
        """ init Device

        Args:
            dev_info (dict): device information, must be a dict type
            device_pool (DevicePool): device pool object, used to free resource when don't need resource anymore
        """
        assert isinstance(dev_info,  dict)
        self.__dev_info = dev_info

        # extract key from dev_info, and put them in the Device object, so you can access them by dev.key1
        for key in dev_info.keys():
            self.__dict__[key] = dev_info[key]

        self.__device_manager = device_pool

    def __del__(self):
        """ free resource when the Device object get freed
        """
        self.__device_manager._DevicePool__free(self.__dev_info)


class DevicePool:
    """Device Pool

    Device Pool is used to manage resource
    """

    def __init__(self, resource_list):
        """ init device pool
        
        Args:
            resource_list(list): list of dict type, you can save resource information as dict, then pass them as a list of dict to DevicePool 
    """
        for d in resource_list:
            assert type(d) == dict, 'type of element in list must be dict type'
        
        # used to manage availble resource
        self.__available_devices = [ ReadOnlyDotDict(d) for d in resource_list ]
        # used to manage unavaible resource
        self.__unavailable_devices = [ ]


    def get(self, filter_func= lambda dev : True, timeout = 0):

        """ allocate reousrce from pool
        
        Args：
            filter_func(function): used to filter device, so you can get the exact device you want, for example, 'lambda dev: dev.id == 1', you can get the device with id attribute is 1
            timeout(int): in sec. how long do you want to wait, when there is no resource available, default 0 sec
        
        Returns:
            Device: return a device object. if timeout, return None
        """
        assert timeout >= 0, "timeout can't be negtive"

        start_time = time.time()
        while True:
            device = list(filter(filter_func, self.__available_devices))
            if len(device) != 0:
                dev = device[0]
                self.__available_devices.remove(dev)
                self.__unavailable_devices.append(dev)
                return Device(dev, self)
            else:
                wait_time = time.time() - start_time
                if wait_time >= timeout:
                    return None


    def __free(self, dev):
        """free the device you get

        Args:
            dev (ReadOnlyDotDict): device to free
        """
        if dev in self.__unavailable_devices:
            self.__unavailable_devices.remove(dev)
            if dev not in self.__available_devices:
                self.__available_devices.append(dev)

if __name__ == "__main__":
    print(dir(DevicePool))
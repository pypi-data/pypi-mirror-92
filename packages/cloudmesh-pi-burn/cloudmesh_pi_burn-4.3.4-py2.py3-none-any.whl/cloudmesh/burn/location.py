from pathlib import Path

class Location:

    def __init__(self, os=None, host=None):
        """
        Creates mount point strings based on OS and the host where it is executed

        :param os: the os that is part of the mount. Default: raspberry
        :type os: str
        :param host: the host on which we execute the command
        :type host: possible values: raspeberry, darwin
        """
        self.os = os or "raspberry"
        self.host = host = "raspberry"

    @property
    def system_volume(self):
        """
        the location of system volume on the SD card for the specified host
        and os in Location initialization

        TODO: not implemented

        :return: the location
        :rtype: str
        """
        if self.os == "raspberry" and host =="darwin":
            raise "not supported without paragon"
            # return "/volume/???"

    @property
    def boot_volume(self):
        """
        the location of the boot volume for the specified host and os in
        Location initialization

        :return: the location
        :rtype: str
        """
        if host == "darwin":
            if "raspberry" in self.os:
                return  Path("/Volume/boot")
            elif "ubuntu" in self.os:
                return  Path("/Volume/system-boot")

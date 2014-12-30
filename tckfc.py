"""
TrueCrypt key file cracker
"""
import argparse
import os
import logging
import sys
import commands
import itertools

# TCKFC log handler file
TCKFC_LOG_FILE = ".tckfc.log"

# Error messages tuple
ERROR_MESSAGES = ("TrueCrypt File does not exist", "Mount directory does not exist", 
                  "Already mounted", "Key files folder does not exist", 
                  "Combination value should be minimum from number of key files")


class TCKFCError(Exception):
    """
    TrueCrypt Key File Cracker
    Base Exception Class
    """
    def __init__(self, name):
        """
        Constructor method
        @name: str
        """
        self.name = name
        self.logger = logging.getLogger(__name__)
        self.logger.warning(name)

    def __repr__(self):
        """
        Representation dunder method
        """
        return "<TCKFCError: {name} >".format(self.name)

    def __str__(self):
        """
        Str dunder method
        """
        return "<TCKFCError: {name} >".format(self.name)

class TrueCryptHandler(object):
    """
    TrueCrypt Handler
    Main class for handling truecrypt process
    """
    def __init__(self, password, tc_file, mount_point):
        """
        Constructor method
        @password: truecrypt file password
        @tc_file: truecrypt encrypted file
        @mount_point: mount point of truecrypt file
        """
        # set the arguments
        self.password = password
        self.key_files = None
        self.tc_file = tc_file
        self.mount_point = mount_point

        # Init the logger
        self.logger = logging.getLogger(__name__)

        # Check the trucrypt is installed
        self.__check()

    def run(self):
        """
        TrueCrypt process runner
        """
        # Create the key files
        if not self.key_files:
            raise TCKFCError("Key files are None")
        self.key_files = ",".join(self.key_files)
        self.logger.debug("Key files: {0}".format(self.key_files))

        # Init command line string
        command = "truecrypt -t --non-interactive -p {0} -k {1} {2} {3} &> /dev/null"
        command = command.format(self.password, self.key_files, self.tc_file, self.mount_point)
        self.logger.debug("Command: '{0}'".format(command))

        # Execute command
        result = commands.getstatusoutput(command)
        self.logger.debug("Command result status: '{0}'".format(result[0]))
        self.logger.debug("Command result: '{0}'".format(result[1]))
        # Check the result
        if not result[0] and not result[1]:
            self.logger.info("Successfully opened with: '{0}'".format(self.key_files))
            commands.getstatusoutput("truecrypt -d {0}".format(self.tc_file))
            self.logger.info("Mount point removed")
            sys.exit(0)
        else:
            self.logger.info("Failed with: '{0}'".format(self.key_files))
    
    def __check(self):
        """
        Check the truecrypt is installed
        """
        if commands.getstatusoutput("which truecrypt")[0]:
            raise TCKFCError("TrueCrypt not installed")


class TCKFC(object):
    """
    TrueCrypt key file cracker
    Main class for cracking
    """
    def __init__(self, args):
        """
        Constructor
        @args: argparse instance
        """
        # Set the arguments
        self.key_files_dir = args.keyfiles
        self.tc_file = args.tcfile
        self.password = args.password
        self.mount_point = args.mountpoint
        self.combination = args.combination

        # Init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Argument parsing is completed")

        # Check args is valid
        self.__is_valid()

        # Find all of the possible key files
        self.key_files = self.__get_key_files()
        self.logger.debug("Key files: {0}".format(self.key_files))

    def crack(self):
        """
        Crack function
        """
        # Check the combination number
        if len(self.key_files) < self.combination:
            raise TCKFCError(ERROR_MESSAGES[4])   
        self.logger.debug("Key file combinations {0}".format(self.combination))       
        
        # Init the TrueCrypt handler
        self.tc_handler = TrueCryptHandler(self.password, self.tc_file, self.mount_point)

        # Create all possible combinations and invoke trucrypt with its
        for c in itertools.combinations(self.key_files, self.combination):
            self.tc_handler.key_files = c
            self.logger.debug("Invoke TrueCrypt: {0}, {1}, {2}, {3}".format(self.password, c, self.tc_file, self.mount_point))
            self.tc_handler.run()

    def __get_key_files(self):
        """
        Get the key files
        return: all possible key files in key_files_dir
        """
        # Find the all files in key_files_dir
        files = []
        for root, _, file_names in os.walk(self.key_files_dir):
            for file_name in file_names:
                files.append(os.path.join(os.path.abspath(root), file_name))
        return files

    def __is_valid(self):
        """
        Check directories and files are correct
        """
        if not os.path.isfile(self.tc_file):
            raise TCKFCError(ERROR_MESSAGES[0])
        if not os.path.isdir(self.mount_point):
            raise TCKFCError(ERROR_MESSAGES[1])
        if os.path.ismount(self.mount_point):
            raise TCKFCError(ERROR_MESSAGES[2])
        if not os.path.isdir(self.key_files_dir):
            raise TCKFCError(ERROR_MESSAGES[3])        

if __name__ == "__main__":
    # Init the root logger with log format
    log_formatter = logging.Formatter("[%(asctime)s] [%(levelname)-7.7s] [%(message)s]")
    root_logger = logging.getLogger(__name__)  
    root_logger.setLevel(logging.DEBUG)  

    # Init the file handler for logging
    file_handler = logging.FileHandler(TCKFC_LOG_FILE)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)    

    # Init the standart error for logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)    

    # Init the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("keyfiles", help="Key directory that contains possible key files", action="store")
    parser.add_argument("tcfile", help="TrueCrypt encrypted file", action="store")
    parser.add_argument("password", help="TrueCrypt decryption key", action="store")
    parser.add_argument("mountpoint", help="Mount point", action="store")
    parser.add_argument("-c", "--combination", help="Keyfile combinations", default=1, nargs='?', type=int)

    # Start
    try:
        root_logger.debug("Cracking is started")
        tckfc = TCKFC(parser.parse_args())
        tckfc.crack()
    except TCKFCError:
        sys.exit(1)
    else:
        root_logger.debug("Cracking is completed")
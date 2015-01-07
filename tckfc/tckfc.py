"""
TrueCrypt key file cracker
"""
import argparse
import os
import logging
import sys
import commands
import itertools
import multiprocessing
import functools
import signal
import time

__version__ = "0.2.0"

# TCKFC log handler file
TCKFC_LOG_FILE = ".tckfc.log"

# Error messages tuple
ERROR_MESSAGES = ("TrueCrypt File does not exist", "Mount directory does not exist", 
                  "Already mounted", "Key files folder does not exist", 
                  "Combination value should be minimum from number of key files",
                  "TrueCrypt not installed.")


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

def truecrypt_handler(kc, psw, tcf, mp):
    """
    TrueCrypt Handler
    @psw: truecrypt file password
    @tcf: truecrypt encrypted file
    @mp: mount point of truecrypt file   
    @kc: possible key files 
    """
    logger = logging.getLogger(__name__)
    key_files = ",".join(kc)
    logger.debug("Key files: {0}".format(key_files))

    # Init command line string
    command = "truecrypt -t --non-interactive -p {0} -k {1} {2} {3} &> /dev/null"
    command = command.format(psw, key_files, tcf, mp)
    logger.debug("Command: '{0}'".format(command))

    # Execute command
    result = commands.getstatusoutput(command)
    logger.debug("Command result status: '{0}'".format(result[0]))
    logger.debug("Command result: '{0}'".format(result[1]))
    
    # Check the result
    if not result[0] and not result[1]:
        logger.info("Successfully opened with: '{0}'".format(key_files))
        commands.getstatusoutput("truecrypt -d {0}".format(tcf))
        logger.info("Mount point removed")
        sys.exit(0)
    else:
        logger.info("Failed with: '{0}'".format(key_files))    


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
        self.pool = multiprocessing.Pool(multiprocessing.cpu_count(), self.__init_worker
            )

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
        
        # Create combinations
        combinations = itertools.combinations(self.key_files, self.combination)

        # Create partial crack function
        crack_function = functools.partial(truecrypt_handler, psw=self.password, tcf=self.tc_file, mp=self.mount_point)

        # Crack with multiple cores and wait
        self.pool.map_async(crack_function, combinations)

        # Handle ctrl-c
        try:        
            time.sleep(10)
        except KeyboardInterrupt:
            self.pool.terminate()
            self.pool.join()
        else:
            self.pool.close()
            self.pool.join()                  

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
        if commands.getstatusoutput("which truecrypt")[0]:
            raise TCKFCError(ERROR_MESSAGES[4])

    def __init_worker(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    """
    Main function
    """
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

if __name__ == "__main__":
    main()

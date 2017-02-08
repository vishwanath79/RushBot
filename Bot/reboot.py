import logging
import socket
import sys

from Bot.replierbot import ReplyToTweet

lock_socket = None # Keep the socket open until the very end of the script so we use a global variable to avoid going out of scope and being garbage-collected

def is_lock_free():
    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_id = "ingvay7.replierbot"
        lock_socket.bind('\0' + lock_id)
        logging.debug("Acquired lock %r" %(lock_id,))
        return True

    except socket.error:
        # socket already locked, task must already be running
        logging.info("failed to acquire lock %r" % (lock_id,))
        return False


if not is_lock_free():
    sys.exit()

ReplyToTweet()

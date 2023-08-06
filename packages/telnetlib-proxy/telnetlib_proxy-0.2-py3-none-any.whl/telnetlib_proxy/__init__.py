
import os
import sys
import socks
import socket
import termios
import argparse
import telnetlib
from urllib.parse import urlparse


__all__ = ["Telnet"]


def wait_key(echo=False):
    """ Wait for a key press on the console and return it.
    https://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
    """

    result = None
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON
    if not echo:
        newattr[3] = newattr[3] & ~termios.ECHO  # disable local echo
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


class Telnet(telnetlib.Telnet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.echo = False

    def mt_interact(self):
        """Multithreaded version of interact()."""
        import _thread
        _thread.start_new_thread(self.listener, ())
        while 1:
            key = wait_key(self.echo)
            if key in ['\x04']:  # Ctrl-D
                break
            self.write(key.encode('ascii'))

    def open(self, host, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, **kwargs):
        """Connect to a host.
        The optional second argument is the port number, which
        defaults to the standard telnet port (23).
        Don't try to reopen an already connected instance.
        """
        self.eof = 0
        if not port:
            port = telnetlib.TELNET_PORT
        self.host = host
        self.port = port
        self.timeout = timeout
        sys.audit("telnetlib.Telnet.open", self, host, port)

        proxy_url = os.environ.get('telnet_proxy')

        if proxy_url:
            url_info = urlparse(proxy_url)
            proxy_args = {
                'proxy_type': socks.PROXY_TYPES.get(url_info.scheme.upper()),
                'proxy_addr': url_info.hostname,
                'proxy_port': url_info.port,
                'proxy_username': url_info.username,
                'proxy_password': url_info.password
            }
        else:
            proxy_args = {}

        proxy_args.update(kwargs)

        print('Trying {}:{}...'.format(host, port))

        target_hostname = socket.gethostbyaddr(host)[0]

        if proxy_args.get('proxy_addr'):
            self.sock = socks.create_connection((host, port), timeout, **proxy_args)
            socks_hostname = socket.gethostbyaddr(proxy_args.get('proxy_addr'))[0]
            print('Connected to {} via {}.'.format(target_hostname, socks_hostname))
        else:
            self.sock = socket.create_connection((host, port), timeout)
            print('Connected to {}.'.format(target_hostname))


def main():
    """
    Usage: telnet5 [-d] ... [host [port]]
    Default host is localhost; default port is 23.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host', default='localhost')
    parser.add_argument('port', help='port', default=23)
    parser.add_argument('--echo', action='store_true', default=False, help='Enable echo')
    parser.add_argument('-d', action='count', default=0, help='Increase debug level')
    args = parser.parse_args()

    debuglevel = args.d
    host = args.host

    if args.port:
        try:
            port = int(args.port)
        except ValueError:
            port = socket.getservbyname(args.port, 'tcp')

    with Telnet() as tn:
        tn.echo = args.echo
        tn.set_debuglevel(debuglevel)
        tn.open(host, port, timeout=0.5)
        try:
            tn.mt_interact()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import logging
from math import gcd
import os
# Secure random
from secrets import SystemRandom
import signal
import socketserver
import string
import sys
import threading
import types
from datetime import datetime


logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', filename="server.log")

############################# CONSTANTS #############################

server_prefix = 'S:'
client_prefix = 'C:'
banner = f"""lastpacketbender's TCP server; written in Python 3.10"""

status_codes = {
        '00': 'WELCOME',
        '01': 'OK',
        '02': 'ERROR',
        '03': 'DATA',
        '99': 'GOODBYE'
        }

base29_charset = '0123456789ABCDEFGHIJKLMNOPQRS'

koan_text = [ "The Surangama scripture says, \"When I do not see, why do you not see my not seeing?",
             "If you see my not seeing, naturally that is not the characteristic of not seeing.",
             "If you don't see my not seeing, it is naturally not a thing-how could it not be you?\""]

############################# GLOBALS ##############################
# To create cryptographically secure integers, I'm using Py3's
# secrets module which reads from system's secure /dev/random.
####################################################################
system_random = SystemRandom()

if "DEBUG" in os.environ and os.environ["DEBUG"]:
    debug = True
    sep = "\n"
else:
    debug = False
    sep = "\r\n"

############################# MATH ##############################

class DH:
    """ Key exchange session wrapper """
    def __init__(self, p):
        self.p = p
        self.b = system_random.choice(primitive_roots(self.p))
        # FIXME: Use very large integers/look at security of picking one
        self.a = int(system_random.randint(0, 65535))
        self.e = pow(self.b, self.a) % self.p
        self.e2 = None
        self.s = None

def primitive_roots(modulo):
    required_set = {num for num in range(1, modulo) if gcd(num, modulo) }
    return [g for g in range(1, modulo) 
            if required_set == {pow(g, powers, modulo)
                                for powers in range(1, modulo)}]

# Either need to time out and return error, or kill on memory usage
def miller_rabin(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    avg = None
    for _ in range(k):
        a = system_random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

############################# SERVER COMMANDS #############################
# NOTE: Executed after lexical analysis/parsing within Parser
#
# listener loop->lexer->parser->command
###########################################################################

def rand(n):
    for _ in range(n):
        yield system_random.randint(0, 255)

def quine():
    # eval to ensure quine is self replicating
    return "_='_=%r;print(_%%_)';print(_%_)"

def base29(n, b=29):
    if n == 0:
        return '0'
    digits = ''
    while n:
        digits += base29_charset[int(n % b)]
        n //= b
    return digits[::-1] 

def code():
    with open(__file__) as f:
        for line in f.readlines():
            yield line

def koan():
    for line in koan_text:
        yield line

def dh(p, session=None):
    if not session:
        return DH(int(p))
    else:
        session.e2 = int(p)
        session.s = pow(session.e2, session.a) % session.p
        return session

def _next(data=None):
    if data:
        for line in data:
            yield line

def goodbye():
    pass

############################# Lexer/Parser #############################

class Parser:
    @staticmethod
    def parse(tokens, session=None):
        token_iter = iter(tokens)
        for token in token_iter:
            if token == "RAND":
                n = int(next(token_iter))
                return rand(n)
            elif token == "QUINE":
                return quine()
            elif token == "BASE29":
                n = int(next(token_iter))
                return base29(n)
            elif token == "CODE":
                return code()
            elif token == "KOAN":
                return koan()
            elif token == "DH":
                p = int(next(token_iter))
                return dh(p)
            elif token == "NEXT":
                # Essentially a NOP
                return _next()
            elif token == "GOODBYE":
                return goodbye()
            # DH key exchange
            elif token.isdigit():
                return dh(token, session)
class NewThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target != None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
class Lexer:
    logger = logging.getLogger('Lexer')
    cmd_narg_map = {
            "RAND": 1,
            "QUINE": 0,
            "BASE29": 1,
            "CODE": 0,
            "KOAN": 0,
            "DH": 1,
            "NEXT": 0, 
            "GOODBYE": 0
            }

    def __init__(self, msg):
        self.command = msg
        self.tokens = msg.split()

    def lex(self, exchanging=False):
        if not debug and not self.command.endswith(sep):
            return False, "MISSING <CRLF>"
        if exchanging:
            if len(self.tokens) > 1:
                return False, "INVALID NUMBER OF PARAMETERS DURING NEGOTIATION"
            elif not self.tokens[0].isdigit():
                return False, "PARAMETER NOT A NUMBER DURING NEGOTIATION"
            return True, None
        no_arg_cmds = [k for k,v in self.cmd_narg_map.items() if v == 0]
        one_arg_cmds = [k for k,v in self.cmd_narg_map.items() if v == 1]
        if len(self.tokens) > 2:
            return False, "INVALID NUMBER OF PARAMETERS"
        elif self.tokens and self.tokens[0] in no_arg_cmds:
            if len(self.tokens) != 1:
                return False, "INVALID NUMBER OF PARAMETERS"
        elif self.tokens and self.tokens[0] in one_arg_cmds:
            if len(self.tokens) != 2:
                return False, "INVALID NUMBER OF PARAMETERS"
            if not self.tokens[1].isdigit():
                return False, "PARAMETER NOT A NUMBER"
            if self.tokens[0] == "DH":
                try:
                    if not miller_rabin(int(self.tokens[1]), 40):
                        return False, "NOT PRIME"
                except RuntimeError:
                    return False, "TIMED OUT"
        else:
            return False, "SYNTAX ERROR"
        return True, None

############################# Server/main #############################

class Handler(socketserver.BaseRequestHandler):
    logger = logging.getLogger('Handler')
    # Thread local - can only ever be updated in one of two places
    welcomed = False
    # DH session
    session = None
    # Clients with pending NEXT data
    waiting = False
    next_data = b""

    @staticmethod
    def get_status(code):
        return code, status_codes[code]

    def tx(self, code='', msg='', terminator=False, prompt=False):
        # possible FIXME
        msg = msg.rstrip()
        if code:
            code, status = self.get_status(code)
            self.request.sendall(f"{server_prefix} {code} {status} {msg}{sep}".encode())
        elif prompt:
            self.request.sendall(f"{client_prefix} ".encode())
        else:
            if msg:
                self.request.sendall(f"{server_prefix} {msg}{sep}".encode())
                if terminator:
                    self.request.sendall(f"{server_prefix} .{sep}".encode())
            elif terminator:
                self.request.sendall(f"{server_prefix} .{sep}".encode())

    def rx(self):
        terminator = ".{}".format(sep, sep).encode()
        # Early write in case of attempts to break
        fname = f"{self.client_address[0]}:{self.client_address[1]}.rx"
        with open(fname, "wb+") as f:
            f.write(self.next_data)
        if not debug and self.data == terminator or (debug and self.data == terminator):
            self.waiting = False
            self.tx('01')
            self.next_data = b""
        else:
            self.next_data += self.data

    def commands(self, tokens=None, data=None):
        close = False
        if data:
            result = _next(data)
            if isinstance(result, types.GeneratorType):
                for i in result:
                    if isinstance(i, str):
                        self.rx(msg=i)
            return False
        elif tokens and tokens[0] == "NEXT":
            self.tx('01')
            self.waiting = True
            return False

        if tokens[0] == "GOODBYE":
            self.tx('99')
            return True

        # Sequencing of OK message different for DH, doesn't exist on GOODBYE
        if tokens[0] not in ["DH"] and not tokens[0].isdigit() and not self.waiting:
            # 01 OKAY - send acknowledgement of valid command
            self.tx('01')

        result = Parser.parse(tokens, session=self.session)

        if tokens[0] == "DH":
            self.session = result

        # Transmit message and terminate with . for generator types
        if isinstance(result, types.GeneratorType):
            for i in result:
                if isinstance(i, str):
                    self.tx(msg=i)
                elif isinstance(i, int):
                    self.tx(msg=str(i))
            self.tx(terminator=True)
        elif isinstance(result, str):
            if tokens[0] == "QUINE":
                self.tx(msg=result, terminator=True)
            elif tokens[0] == "BASE29":
                self.tx(msg=result)
        else:
            # We parsed a key exchange container
            if tokens[0] == "DH" or (tokens[0].isdigit() and self.session):
                if not result.s:
                    # Secret generated, send b and e to client
                    self.tx('01', f"{result.b} {result.e}")
                else:
                    self.tx('03', str(result.s))
                    # Clear session, we both now have keys
                    self.session = None
        return close

    def welcome(self):
        if not self.welcomed:
            self.tx('00', banner)
            self.welcomed = True

    def process(self, request):
        cmd = self.data.decode('utf-8')
        self.logger.debug("{} from {}:{}".format(cmd.strip(), self.client_address[0], self.client_address[1]))
        close = False 
        # Lexical analysis
        if not self.waiting:
            lexer = Lexer(cmd)
            pass_analysis, error_msg = lexer.lex(exchanging=True if self.session else False)
            if not pass_analysis:
                self.tx('02', error_msg)
            else:
                # Handoff to command handler for parsing/execution
                close = self.commands(lexer.tokens)
        # Receive NEXT data (using raw data in case files get sent)
        else:
            self.rx()
        return close



    def handle(self):
        self.welcome()
        next_data = b""
        while True:
            self.tx(prompt=True)
            # FIXME: Handle oversized data
            if not self.waiting:
                self.data = self.request.recv(4096).upper()
            else:
                # Don't strip or convert sensitive data to uppercase, we need valid signatures
                self.data = self.request.recv(4096)
            # empty data, client quit writing to socket
            if not self.data:
                break
            close = self.process(self.data)
            if close:
                self.session = None
                self.welcomed = False
                break


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address,
                 handler_class=Handler,):
        self.logger = logging.getLogger('Server')
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_address,
                                        handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug('waiting for request')
        self.logger.info(
                'Handling requests, press <Ctrl-C> to quit'
                )
        socketserver.TCPServer.serve_forever(self, poll_interval)
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.verify_request(
                self, request, client_address,
                )

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.process_request(
                self, request, client_address,
                )

    def server_close(self):
        self.logger.debug('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.finish_request(
                self, request, client_address,
                )

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(
                self, request_address,
                )

    def shutdown(self):
        self.logger.debug('shutdown()')
        return socketserver.TCPServer.shutdown(self)

if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print("USAGE: ./server.py <PORT NUM>")
        exit(3301)

    HOST, PORT = "localhost", int(sys.argv[1])

    with Server((HOST, PORT), Handler) as server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        # server_thread.setDaemon(True)
        server_thread.start()
        logger = logging.getLogger('Server')
        logger.info('Server on %s:%s', ip, port)
        try:
            while True:
                res = server.handle_request()
        except KeyboardInterrupt:
            logger.info('interrupt received, terminating...')
            server.shutdown()
            server.socket.close()

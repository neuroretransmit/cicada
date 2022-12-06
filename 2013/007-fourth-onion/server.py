#!/usr/bin/env python3

import logging
# Secure random
from secrets import SystemRandom
import socketserver
import sys
import threading

import types
import re
from math import gcd

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

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
# NOTE: Does NOT need to be seeded, it is an unused param from doc
#
# To create cryptographically secure integers, I'm using Py3's
# secrets module which reads from system's secure /dev/random.
####################################################################

# TODO: Look at rootkit to see if /dev/urandom and random are the
# same character device now. Recent kernel changes increased speed
# and I remember having to fix a hook for injecting cyclic patterns.
system_random = SystemRandom()

# Diffie-hellman sessions currently under negotiation
negotiating = {}

############################# MATH ##############################

class DH:
    """ Key exchange session wrapper """
    def __init__(self, p):
        self.p = p
        self.b = system_random.choice(primitive_roots(self.p))
        self.a = int(system_random.random())
        self.e = self.b ** self.a % self.p
        self.e2 = None
        self.s = None

def primitive_roots(modulo):
    required_set = {num for num in range(1, modulo) if gcd(num, modulo) }
    return [g for g in range(1, modulo) 
            if required_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]

def is_prime(n):
    if n < 3 or n % 2 == 0:
        return n == 2
    else:
        return not any(n % i == 0 for i in range(3, int(n**0.5 + 2), 2))

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
            yield line#.rstrip()

def koan():
    for line in koan_text:
        yield line

def dh(p, session=None):
    if not session:
        return DH(int(p))
    else:
        session.e2 = int(p)
        session.s = session.e2 ** session.a % session.p
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
        if not self.command.endswith("\r\n"):
            return False, "MISSING <CRLF>"
        if exchanging:
            if len(self.tokens) > 1:
                return False, "INVALID NUMBER OF PARAMETERS DURING NEGOTIATION"
            if not self.tokens[0].isdigit():
                return False, "PARAMETER NOT A NUMBER DURING NEGOTIATION"
            return True, None
        no_arg_cmds = [k for k,v in self.cmd_narg_map.items() if v == 0]
        one_arg_cmds = [k for k,v in self.cmd_narg_map.items() if v == 1]
        print(self.tokens)
        if len(self.tokens) > 2:
            return False, "INVALID NUMBER OF PARAMETERS"
        elif self.tokens[0] in no_arg_cmds:
            if len(self.tokens) != 1:
                return False, "INVALID NUMBER OF PARAMETERS"
        elif self.tokens[0] in one_arg_cmds:
            if len(self.tokens) != 2:
                return False, "INVALID NUMBER OF PARAMETERS"
            if not self.tokens[1].isdigit():
                return False, "PARAMETER NOT A NUMBER"
            if self.tokens[0] == "DH":
                if not is_prime(int(self.tokens[1])):
                    return False, "NOT PRIME"
        else:
            return False, "SYNTAX ERROR"
        return True, None

############################# Server/main #############################

class Handler(socketserver.BaseRequestHandler):
    logger = logging.getLogger('Handler')
    # FIXME: What if multiple users connect from behind the same router
    # Add another attribute to uniquely identify them
    welcomed = set()
    # Clients with a pending NEXT
    waiting = set()
    mutex = threading.Lock()

    @staticmethod
    def get_status(code):
        return code, status_codes[code]

    def tx(self, code='', msg='', terminator=False, prompt=False):
        # possible FIXME
        msg = msg.rstrip()
        if code:
            code, status = self.get_status(code)
            self.request.sendall(f"{server_prefix} {code} {status} {msg}\r\n".encode())
        elif prompt:
            self.request.sendall(f"{client_prefix} ".encode())
        else:
            if msg:
                self.request.sendall(f"{server_prefix} {msg}\r\n".encode())
                if terminator:
                    self.request.sendall(f"{server_prefix} .\r\n".encode())
            elif terminator:
                self.request.sendall(f"{server_prefix} .\r\n".encode())

    def rx(self, msg=''):
        # possible FIXME
        print(f"{client_prefix} {msg}".decode('utf-8'))
        
    def negotiation(self):
        return negotiating[self.client_address[0]] if self.is_negotiating() else None
    
    def is_negotiating(self):
        return self.client_address[0] in negotiating

    def commands(self, tokens=None, data=None):
        close = False
        if data:
            result = _next(data)
            if isinstance(result, types.GeneratorType):
                for i in result:
                    if isinstance(i, str):
                        self.rx(msg=i)
            return False
        elif tokens and tokens[0] == "NEXT" and not data:
            self.tx('01')
            with self.mutex:
                self.waiting.add(self.client_address[0])
            return False
        
        if tokens[0] == "GOODBYE":
            self.tx('99')
            return True

        # Sequencing of OK message different for DH, doesn't exist on GOODBYE
        if tokens[0] not in ["DH"] and not tokens[0].isdigit() and self.client_address[0] not in self.waiting:
            # 01 OKAY - send acknowledgement of valid command
            self.tx('01')

        result = Parser.parse(tokens, session=self.negotiation())

        # Add client to negotiating sessions
        if tokens[0] == "DH":
            negotiating[self.client_address[0]] = result

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
            if tokens[0] == "DH" or (tokens[0].isdigit() and self.is_negotiating()):
                if not result.s:
                    # Secret generated, send b and e to client
                    self.tx('01', f"{result.b} {result.e}")
                else:
                    self.tx('03', str(result.s))
                    negotiating.pop(self.client_address[0])
        return close

    def welcome(self):
        if self.client_address[0] not in self.welcomed:
            self.tx('00', banner)
            self.welcomed.add(self.client_address[0])

    def handle(self):
        self.welcome()
        
        close = False
        client = self.client_address[0]
        while True:
            self.tx(prompt=True)
            # FIXME: Handle oversized data
            if not client in self.waiting:
                self.data = self.request.recv(1024).upper()
                print("in not waiting")
            else:
                # Don't strip or convert sensitive data to uppercase, we need valid signatures
                self.data = self.request.recv(1024)
                print("in waiting")
            # empty data, client quit writing to socket
            if not self.data:
                break
            cmd = self.data.decode('utf-8')
            self.logger.debug("{} wrote: {}".format(client, cmd))
            # Receive data
            if client in self.waiting:
                # self.data = self.request.recv(1024)
                if isinstance(self.data, types.GeneratorType):
                    for i in result:
                        if isinstance(i, str):
                            self.rx(msg=i)
                # Bypass lexing for data
                if self.data.endswith(b".\r\n"):
                    with self.mutex:
                        self.waiting.remove(client)
                    self.tx('01')
            # Lexical analysis
            else:
                lexer = Lexer(cmd)
                pass_analysis, error_msg = lexer.lex(exchanging=self.is_negotiating())
                if not pass_analysis:
                    self.tx('02', error_msg)
                else:
                    # Handoff to command handler for parsing/execution
                    close = self.commands(lexer.tokens)
            if close:
                self.welcomed.remove(client)
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
        server_thread.setDaemon(True)
        server_thread.start()
        logger = logging.getLogger('Server')
        logger.info('Server on %s:%s', ip, port)
        try:
            while True:
                server.handle_request()
        except KeyboardInterrupt:
            logger.info('interrupt received, terminating...')
            server.shutdown()
            server.socket.close()

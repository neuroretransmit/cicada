#!/usr/bin/env python3

import logging
import random
import re
import socketserver
import string
import sys
import threading

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

banner = """Web browsers are useless here.                                                  
                                                                                
                                                                                
    ,+++77777++=:,                    +=                      ,,++=7++=,,       
  7~?7   +7I77 :,I777  I          77 7+77 7:        ,?777777??~,=+=~I7?,=77 I   
=7I7I~7  ,77: ++:~+7 77=7777 7     +77=7 =7I7     ,I777= 77,:~7 +?7, ~7   ~ 777?
77+7I 777~,,=7~  ,::7=7: 7 77   77: 7 7 +77,7 I777~+777I=   =:,77,77  77 7,777, 
= 7  ?7 , 7~,~  + 77 ?: :?777 +~77 77? I7777I7I7 777+77   =:, ?7   +7 777?      
    77 ~I == ~77= +777 777~: I,+77?  7  7:?7? ?7 7 7 77 ~I   7I,,?7 I77~        
     I 7=77~+77+?=:I+~77?     , I 7? 77 7   777~ +7 I+?7  +7~?777,77I           
       =77 77= +7 7777         ,7 7?7:,??7     +7    7   77??+ 7777,            
           =I, I 7+:77?         +7I7?7777 :             :7 7                    
              7I7I?77 ~         +7:77,     ~         +7,::7   7                 
             ,7~77?7? ?:         7+:77777,           77 :7777=                  
              ?77 +I7+,7         7~  7,+7  ,?       ?7?~?777:                   
                 I777=7777 ~     77 :  77 =7+,    I77  777                      
                   +      ~?     , + 7    ,, ~I,  = ? ,                         
                                  77:I+                                         
                                  ,7                                            
                                   :77                                          
                                      :                                         
                                                                                
Welcome.                                                                        
"""

message = """A message for you:

0000000:2d2d2d2d2d424547494e20504750205349474e4544204d4553534147452d2d2d2d2d0a486173683a20534841310a0a20202020200a5665727920676f6f642e0a20
0000041:20200a596f75206861766520646f6e652077656c6c20746f20636f6d652074686973206661722e0a20200a7873786e616b73696374366567786b712e6f6e696f6e
0000082:0a20200a476f6f64206c75636b2e0a2020200a333330310a20202020200a2d2d2d2d2d424547494e20504750205349474e41545552452d2d2d2d2d0a5665727369
00000c3:6f6e3a20476e7550472076312e342e31312028474e552f4c696e7578290a0a69514963424145424167414742514a513653304841416f4a45426766416556364e51
0000104:6b502f4a3051414c44716133564a7939784c4c6c6749356a5068524970340a66786562624e6874454c4f4859466b44355a397a745159476c65376c4b504d386c6b
0000145:4d536e636949593035394b4969354e53545637493937734a626f473377740a6b6848745a674e52773176325751357575724375356c31772b38342f4c354a7a324e
0000186:6d456c784f427a57723638646c5159743271664251786b327a522f6654490a544c43454776465a746c6e724e66426b376a7349794a59635858506761625334376f
00001c7:5039764f45586c42312b506d30433775505042504e3761716b665550476c0a6f3166326873634a66374a65324476625a742b3665787859736d3537467039353358
0000208:414e41642f557046567a542f3835325867363367745a72492b536d66335a0a4256636a70437a7948337753385230694d2b7270303243774a704a7a7357474c7865
0000249:51476d584c325358424234337a565a414a716c355564584c5447586b62640a6e504d64332f43624a2b6c37724f305941673570334a66344b617558375a64365a63
000028a:3277484b4c4f76666a5176455758495931434d68493638426a30725a6f2f0a4d2f666933313346465450416d3678684b52762f74482f387756726172326a593777
00002cb:6e45385878685273793734415a35477141326f484d6566544171335975570a35505838733638324a34706b44554b48476134793635766a49703136706d45496e4d
000030c:414c4a4762777a366d7461754251716c53364152735166656b446e336f5a0a796f73532b675743336a6449764835733557555147566c376a797a3974342b335467
000034d:35635439526e367058324e564e585378677a585842346e493258727259610a346b517235615742386c737361763372796a3543673246486c312b4d4b4f30675976
000038e:2f554633515437354d6978514d75344d2b3577436e4e656b676675794f360a5a7679627a70347334537a526a6b6b39734d4d360a3d5759564f0a2d2d2d2d2d454e
00003cf:4420504750205349474e41545552452d2d2d2d2d0a
Offset: 3301, Skip: 0, Col: 65, Line: 16.
"""

clue = """Here is a clue:

0000000: 1fd9d91c746f141803d010071f18f0028a0b69763d1d19037daa222b4f46b3264d21ed1d31c514982b502e558ffe583b2e018e62bfe44ac063caf344469c53c7da
0000041: 72beefe909de045a3df0e8b7320d570516b431c42f73c08e39af504fd00e88bb323ae09f436395fe1955dd99251693a5971a1738871354ebebf6e74f94b21f7a3b
0000082: 346063d15bd2f0fbacc86d74b6aaaac0d44b6c54300b5eabb9d699f854ae855385fb5bce0a4304964bf6a9020acb540921d17844f39856a97a2f2623547c61009a
00000c3: 421b1756748009c31b9311745f5a2e661175c8b7958fe459fae4d96e9323b29fd21f83565c60f69d51da75ddaf6f06283b77fc0362ba41e570e70a6b6efa2a34b0
0000104: d9f1d2dde221bf636d9c7c47b6291d4bf7b3389916c46652edf7daf8efa2d0d0909f96b57a3310a3c029da90481eeb4b0d53620be26ab5fb5370bfd4edc49514b2
0000145: 2c43c402fc58554b1556d092d7410fb5cd8ba8d92af3cbbc023f3787c3ece9afee71cef31d63b826bd2292bfac22c6e5cc034237575f1737e2aa24262deced106b
0000186: 89e2032ebe6ab51c8d0cf0fe2394b0c5c8d609b1c54bd2178631f9c0f2350d7a798e52b44a50517bc0dd245db004fe0ca6460c02e81699fdea7494165c96ed4bfd
00001c7: 45d26598bf08c3d8e5486ead896f29bd0b996515157448132ea6e02f8f9d23108e69874956fdf69f2ced112f1a4924c8ec35182253c5288be0e3aa2ccbf7b7affc
0000208: d1dc90726bb30c26d41f5854a41b2ea0dc68345aa3bb11b8688c407d36cdd4cdde47d26348d75397e1636b06dbae541452c1173b59b70bc37fe28615c5636158a0
0000249: 38ab6ba758d90d2b93402505265e8374a7f5d9a7528837aad79d8e6ca20b8deac1a67755b7db9f79835a463bce04ded91a13d72c57950d95fd2f65d207299596f1
000028a: 82d27d220e44a4f95d1abb5ad1d133133b4c787721c0a3ddd32c311ffb6d8b8bc9df64658c9156bd0c1393a35236ecb18cdb93cfa5c23ccee333704fe1606fa063
00002cb: 2307b427788df8036c164ce171d42fd3d0fded1bbd8690bff52e35536a3aaaf9fa6872178f94b35b056e860d637c81664a1e1310df56344ddf19bf4fa4f2a28193
000030c: dc34cdd5423ef2cbe680fbc015ce9f6cd71424789674424ef787a1e7aec7f22d487af53bfe5e4ed4b8f207279573f00c7270e136095eb70fe6c465e0291297d059
000034d: 376088f46e159efee300d64eea644a6b5a7038f411d0f4efd67446836860f1084a01e180bacec753403fe6a845e02f82f7781eba82d2dfb38274c156f7b546cb19
000038e: b4ba5b8e84f85645830eeb3d70207d299b649e8d592536e4df0b03888ca3740d9de623d00aea1e0adfcf23d92c6dde711d187ca9d592c31ab00ac6e217892ccefd
00003cf: 1be10b
Offset: 0, Skip: 0, Col: 65, Line: 16.
"""

errors = [
"""The command you typed
Does not seem to exist
But countless more do.
""",
"""%3301, unrecognized command
 \\?\\
 """,
"command not found\n",
"Not a typewriter\n",
"?SYNTAX ERROR\n",
"Bad command or file name\n"
]

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

LOOKUP = {
    'F': 2,
    'U': 3,
    'V': 3,
    'TH': 5,
    'O': 7,
    'R': 11,
    'C': 13,
    'K': 13,
    'G': 17,
    'W': 19,
    'H': 23,
    'N': 29,
    'I': 31,
    'J': 37,
    'EO': 41,
    'P': 43,
    'X': 47,
    'S': 53,
    'Z': 53,
    'T': 59,
    'B': 61,
    'E': 67,
    'M': 71,
    'L': 73,
    'NG': 79,
    'ING': 79,
    'OE': 83,
    'D': 89,
    'A': 97,
    'AE': 101,
    'Y': 103,
    'IA': 107,
    'IO': 107,
    'EA': 109
}

FIRST_LETTER_LOOKUP = {}

lookup_keys = LOOKUP.keys()
for letter in ENGLISH_ALPHABET:
        FIRST_LETTER_LOOKUP[letter] = [x for x in LOOKUP.keys() if x.startswith(letter)]

def preprocess(txt, keep_tabs_breaks = True):
    preprocessed = txt.upper()
    if not keep_tabs_breaks:
        processed = txt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    preprocessed = preprocessed.replace("QU", "CW").replace("Q", "K")
    return preprocessed


class Gematria:
    @staticmethod
    def english_to_value(txt):
        txt = preprocess(txt)
        i = 0
        result = 0
        txt_iter = iter(txt)
        for c in txt_iter:
            if c in FIRST_LETTER_LOOKUP.keys():
                candidates = FIRST_LETTER_LOOKUP[c]

                # Peek forward in text to match larger possibilities
                peek2 = None
                peek3 = None

                if i + 1 < len(txt) - 1:
                    peek2 = c + txt[i + 1]
                if i + 2 < len(txt) - 1:
                    peek3 = peek2 + txt[i + 2]

                if peek3 and peek3 in candidates:
                    result += LOOKUP[peek3]
                    next(txt_iter, None)
                    next(txt_iter, None)
                    i += 2
                elif peek2 and peek2 in candidates:
                    result += LOOKUP[peek2]
                    next(txt_iter, None)
                    i += 1
                elif c in candidates:
                    result += LOOKUP[c]
                else:
                    if c.isspace() or c in string.punctuation:
                        i += 1
                        continue
            i += 1
        return result

def is_prime(n):
    if n < 3 or n % 2 == 0:
        return n == 2
    else:
        return not any(n % i == 0 for i in range(3, int(n**0.5 + 2), 2))

def factor(n):
   for i in range(1, n + 1):
       if n % i == 0:
           yield i

class Handler(socketserver.BaseRequestHandler):
    logger = logging.getLogger('Handler')

    def digit(self, number):
        if is_prime(number):
            reverse = int(str(number)[::-1])
            if not is_prime(reverse):
                factors = list(factor(reverse))
                self.request.sendall(f"{reverse} : {factors}\n".encode())
            else:
                self.request.sendall("+\n".encode())
        else:
            factors = list(factor(number))
            self.request.sendall(f"{number} : {factors}\n".encode())

    def gematria(self, cmd):
        phrase = re.sub(r"count\s", "", cmd)
        count = Gematria.english_to_value(phrase)
        reverse = int(str(count)[::-1])
        if is_prime(count) and is_prime(reverse):
            response = f"{count}+\n"
        elif is_prime(count):
            response = f"{count}*\n"
        else:
            response = f"{count}\n"
        self.request.sendall(response.encode())

    def command(self, cmd):
        close = False
        if "primes" == cmd:
            primes = [x for x in range(3301) if is_prime(x) and (x < 73 or x > 1223)]
            primes_str = ""
            for prime in primes:
                if prime == 29 or prime == 3257:
                    primes_str += str(prime) + "  "
                else:
                    primes_str += str(prime) + " "
            primes_str += "\n"
            self.request.sendall(primes_str.encode())
        elif cmd in ["hello", "hi", "get message", "get 3301", "get 1033"]:
            self.request.sendall(message.encode())
        elif cmd in ["clue", "hint", "get hint"]:
            self.request.sendall(clue.encode())
        elif cmd in ["exit", "quit", "bye", "goodbye"]:
            self.request.sendall("goodbye\n".encode())
            close = True
        elif cmd in ["cicada", "adacic"]:
            self.request.sendall("+\n".encode())
        elif "count" in cmd:
            self.gematria(cmd)
        elif "help" == cmd:
            self.request.sendall("help, [number] (or number [number]), count [phrase], hello\n".encode())
        else:
            self.request.sendall(random.choice(errors).encode())
        return close

    def handle(self):
        self.request.sendall(banner.encode())
        while True:
            self.data = self.request.recv(1024).strip().lower()
            if not self.data:  # b'' when client shuts down writing on socket.
                break
            cmd = re.sub('[^a-z0-9_ \t]', '', self.data.decode('utf-8')).replace("q", "")
            self.logger.debug("{} wrote: {}".format(self.client_address[0], cmd))
            parts = cmd.split()
            if cmd.isdigit() or "number" in cmd:
                if len(parts) == 2 and parts[1].isdigit():
                    num = int(parts[1])
                    if num >= 0xffffffffffffffff:
                        self.request.sendall("0 0\n".encode())
                    else:
                        self.digit(num)
                else:
                    num = int(cmd)
                    if num >= 0xffffffffffffffff:
                        self.request.sendall("0 0\n".encode())
                    else:
                        self.digit(num)
            elif "get http" in cmd:
                self.request.sendall("Not a webserver\n".encode())
                close = True
            else:
                close = self.command(cmd)
            if close:
                break

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address,
                 handler_class=Handler,
                 ):
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

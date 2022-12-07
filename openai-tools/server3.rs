// Struct to store diffie hellman variables
struct DHVars {
    p: BigUint,
    g: BigUint,
    xa: BigUint,
    xb: BigUint,
}

// Map to store code and response names
let response_map = {
    "00" : "WELCOME",
    "01" : "OK",
    "02" : "ERROR",
    "03" : "DATA",
    "99" : "GOODBYE"
};

// Main TCP server loop
fn main() {
    // Create a TCP listener
    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();

    // Accept connections and process them, spawning a new thread for each one
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                thread::spawn(|| {
                    handle_connection(stream);
                });
            }
            Err(e) => {
                println!("Error: {}", e);
            }
        }
    }
    drop(listener);
}

// Handle a single connection
fn handle_connection(mut stream: TcpStream) {
    // Send the welcome message
    let welcome_msg = format!("00 WELCOME Rust\r\n");
    stream.write(&welcome_msg.into_bytes()).unwrap();

    // Create a DHVars struct
    let mut dhvars = DHVars {
        p: BigUint::zero(),
        g: BigUint::zero(),
        xa: BigUint::zero(),
        xb: BigUint::zero()
    };

    // Create a buffer for reading data
    let mut buf = [0; 512];

    loop {
        let bytes_read = match stream.read(&mut buf) {
            Ok(n) => n,
            Err(e) => {
                println!("Error: {}", e);
                break;
            }
        };

        if bytes_read == 0 {
            break;
        }

        // Parse the command
        let command = parse_command(&buf);

        match command.as_str() {
            "RAND" => {
                let num: usize = command[1].parse().unwrap();
                handle_rand_command(&mut stream, num);
            }
            "QUINE" => handle_quine_command(&mut stream),
            "BASE29" => {
                let num: BigUint = BigUint::parse_bytes(command[1].as_bytes(), 10).unwrap();
                handle_base29_command(&mut stream, num);
            }
            "CODE" => handle_code_command(&mut stream),
            "KOAN" => handle_koan_command(&mut stream),
            "DH" => {
                let p: BigUint = BigUint::parse_bytes(command[1].as_bytes(), 10).unwrap();
                handle_dh_command(&mut stream, &mut dhvars, p);
            }
            "NEXT" => handle_next_command(&mut stream),
            "GOODBYE" => {
                handle_goodbye_command(&mut stream);
                break;
            }
            _ => {
                handle_invalid_command(&mut stream);
            }
        }
    }
}

// Parse a command
fn parse_command(buf: &[u8]) -> Vec<String> {
    let cmd = String::from_utf8_lossy(&buf[..]);
    let cmd_vec: Vec<&str> = cmd.split(" ").collect();
    let vec: Vec<String> = cmd_vec.iter().map(|s| s.to_string()).collect();
    vec
}

// Handle a RAND command
fn handle_rand_command(stream: &mut TcpStream, num: usize) {
    let ok_msg = format!("01 OK\r\n");
    stream.write(&ok_msg.into_bytes()).unwrap();

    for _ in 0..num {
        let num: u8 = rand::thread_rng().gen_range(0, 255);
        let num_msg = format!("{}\r\n", num);
        stream.write(&num_msg.into_bytes()).unwrap();
    }

    let dot_msg = format!(".\r\n");
    stream.write(&dot_msg.into_bytes()).unwrap();
}

// Handle a QUINE command
fn handle_quine_command(stream: &mut TcpStream) {
    let ok_msg = format!("01 OK\r\n");
    stream.write(&ok_msg.into_bytes()).unwrap();

    let quine_msg = format!("fn main(){{print!(\"{{}},{{0:?}})\")}}\r\n", "fn main(){print!(\"{},{0:?})\");}\r\n");
    stream.write(&quine_msg.into_bytes()).unwrap();

    let dot_msg = format!(".\r\n");
    stream.write(&dot_msg.into_bytes()).unwrap();
}

// Handle a BASE29 command
fn handle_base29_command(stream: &mut TcpStream, num: BigUint) {
    let ok_msg = format!("01 OK {}\r\n", num.to_str_radix(29));
    stream.write(&ok_msg.into_bytes()).unwrap();
}

// Handle a CODE command
fn handle_code_command(stream: &mut TcpStream) {
    let ok_msg = format!("01 OK\r\n");
    stream.write(&ok_msg.into_bytes()).unwrap();

    let code_msg = format!("[Server Source Code]\r\n");
    stream.write(&code_msg.into_bytes()).unwrap();

    let dot_msg = format!(".\r\n");
    stream.write(&dot_msg.into_bytes()).unwrap();
}

// Handle a KOAN command
fn handle_koan_command(stream: &mut TcpStream) {
    let ok_msg = format!("01 OK\r\n");
    stream.write(&ok_msg.into_bytes()).unwrap();

    let koan_msg = format!("A master who lived as a hermit on a mountain was asked by a monk, \"What is the Way?\"\r\n\"What a fine mountain this is,\" the master said in reply.\r\n\"I am not asking you about the mountain, but about the Way.\"\r\n\"So long as you cannot go beyond the mountain, my son, you cannot reach the Way,\" replied the master.\r\n");
    stream.write(&koan_msg.into_bytes()).unwrap();

    let dot_msg = format!(".\r\n");
    stream.write(&dot_msg.into_bytes()).unwrap();
}

// Handle a DH command
fn handle_dh_command(stream: &mut TcpStream, dhvars: &mut DHVars, p: BigUint) {
    let g: BigUint = rand::thread_rng().gen_biguint_range(&BigUint::from(2u32), &p);

    let xa: BigUint = rand::thread_rng().gen_biguint_range(&BigUint::from(2u32), &p);
    let ea = &g.modpow(&xa, &p);

    let ok_msg = format!("01 OK {} {}\r\n", g.to_str_radix(10), ea.to_str_radix(10));
    stream.write(&ok_msg.into_bytes()).unwrap();

    // Read the exponent from the client
    let mut buf = [0; 512];
    let bytes_read = match stream.read(&mut buf) {
        Ok(n) => n,
        Err(e) => {
            println!("Error: {}", e);
            return;
        }
    };

    if bytes_read == 0 {
        return;
    }

    let command = parse_command(&buf);
    let xb: BigUint = BigUint::parse_bytes(command[0].as_bytes(), 10).unwrap();
    let eb = &g.modpow(&xb, &p);

    // Compute the secret key
    let xa_inv = xa.modpow(&(p - BigUint::from(2u32)), &p);
    let k = eb.modpow(&xa_inv, &p);

    // Store the DH vars
    dhvars.p = p;
    dhvars.g = g;
    dhvars.xa = xa;
    dhvars.xb = xb;

    // Send the response
    let data_msg = format!("03 DATA {}\r\n", k.to_str_radix(10));
    stream.write(&data_msg.into_bytes()).unwrap();
}

// Handle a GOODBYE command
fn handle_goodbye_command(stream: &mut TcpStream) {
    let msg = format!("99 GOODBYE\r\n");
    stream.write(&msg.into_bytes()).unwrap();
}

// Handle an invalid command
fn handle_invalid_command(stream: &mut TcpStream) {
    let msg = format!("02 ERROR\r\n");
    stream.write(&msg.into_bytes()).unwrap();
}
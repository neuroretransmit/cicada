extern crate rand;
//extern crate rand_core;

use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;
use std::collections::HashMap;
use rand::prelude::*;
use num_bigint::BigUint;
//use rand_core::{OsRng, Rngcore};

// struct for Diffie-Hellman variables
struct DHVars{
    prime_modulus: BigUint,
    base: BigUint,
    secret_int: BigUint,
    exponent_result: BigUint
}

fn num_to_base29(num: u32) -> String {
    let mut result = String::new();
    let mut num = num;

    let symbols = vec!['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R'];

    while num > 0 {
        let index = (num % 29) as usize;
        result.push(symbols[index]);
        num /= 29;
    }

    result.chars().rev().collect::<String>()
}

pub fn main() {
    // get listening port from command line
    let port = std::env::args().nth(1).expect("Please provide a port");
    let port: u16 = port.parse::<u16>().expect("Please provide a valid port");
    // validate port is between 0 and 65535
    if port > 65535 || port < 0 {
        panic!("Port must be between 0 and 65535");
    }
    // create server
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).expect("Cannot bind to port");
    println!("Listening on port {}", port);

    // save code and response names in a hashmap
    let mut code_response_map: HashMap<&str, &str> = HashMap::new();
    code_response_map.insert("00", "WELCOME");
    code_response_map.insert("01", "OK");
    code_response_map.insert("02", "ERROR");
    code_response_map.insert("03", "DATA");
    code_response_map.insert("99", "GOODBYE");

    // save each client's diffie hellman variables in a struct, and store it in a map with key of client's ip + port and value of the struct until they disconnect
    let mut dh_vars_map: HashMap<String, DHVars> = HashMap::new();

    // main server loop
    for stream in listener.incoming() {
        // handle each client on a new thread
        thread::spawn(move || {
            let mut stream = stream.expect("Connection Failed");
            println!("Connection Established");
            // get client's ip and port
            let ip_addr = stream.peer_addr().expect("Cannot get client's ip address").to_string();
            // welcome message
            let welcome_response = format!("00 WELCOME Rust\r\n");
            stream.write_all(welcome_response.as_bytes()).expect("Cannot write to stream");

            loop {
                // show prompt
                let prompt = "C: ";
                stream.write_all(prompt.as_bytes()).expect("Cannot write to stream");
                // get client's message
                let mut data = String::new();
                stream.read_to_string(&mut data).expect("Cannot read from stream");
                // response message
                let mut response_message = String::new();
                // interpret CRLF as \r\n
                data = data.replace("\r\n", "\r\nC: ");
                // convert command to uppercase
                let command = data.to_uppercase();
                let command = command.trim();
                // split command into a vector
                let command_vec: Vec<&str> = command.split(' ').collect();
                // split first element of command vec into a vector
                let command_vec_1: Vec<&str> = command_vec[0].split_terminator(':').collect();
                // save code and response name from command vec 1
                let code = command_vec_1[0];
                let response_name = command_vec_1[1];
                // check if command is in code response map
                let response_name_from_map = code_response_map.get(code);
                match response_name_from_map {
                    Some(x) => {
                        if x == response_name {
                            // println!("correct response name in map");
                            match response_name {
                                "BASE29" => {
                                    // check if command has enough parameters
                                    if command_vec.len() < 2 {
                                        // error if not enough parameters
                                        response_message = format!("02 ERROR Not enough parameters\r\n");
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    } else {
                                        // validate n is a valid number
                                        let n: u32 = match command_vec[1].parse() {
                                            Ok(n) => n,
                                            Err(_) => {
                                                // error if invalid
                                                response_message = format!("02 ERROR Not a valid number\r\n");
                                                stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                                continue
                                            }
                                        };
                                        // convert base 10 number to base 29
                                        let base29_string = num_to_base29(n);
                                        // build base 29 response
                                        response_message = format!("01 OK {}\r\n", base29_string);
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    }
                                },
                                "DH" => {
                                    // validate DH command
                                    if command_vec.len() != 2 {
                                        // send 02 error 
                                        response_message = format!("02 ERROR Invalid DH command\r\n");
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    } else {
                                        // save prime modulus
                                        let prime_modulus: BigUint = command_vec[1].parse().expect("Cannot parse prime modulus");
                                        // select base
                                        let mut rng = thread_rng();
                                        let random_base: u8 = rng.gen_range(0..=255);
                                        let base: BigUint = BigUint::from(random_base);
                                        // select secret int
                                        let random_secret_int = rand::random::<u64>();
                                        let secret_int: BigUint = BigUint::from(random_secret_int);
                                        // compute exponent result
                                        let exponent_result = base.modpow(&secret_int, &prime_modulus);
                                        // save diffie hellman variables to struct
                                        let dh_vars = DHVars {
                                            prime_modulus,
                                            base,
                                            secret_int,
                                            exponent_result
                                        };
                                        // save diffie hellman variables in map
                                        dh_vars_map.insert(ip_addr.clone(), dh_vars);
                                        // send 01 ok response
                                        response_message = format!("01 OK {} {}\r\n", base, exponent_result);
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    }
                                },
                                "RAND" => {
                                    // validate RAND command
                                    if command_vec.len() != 2 {
                                        // send 02 error
                                        response_message = format!("02 ERROR Invalid RAND command\r\n");
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    } else {
                                        // save n
                                        let n: u64 = command_vec[1].parse().expect("Cannot parse n");
                                        // send 01 ok
                                        response_message = format!("01 OK\r\n");
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                        // generate random numbers
                                        for _i in 0..n {
                                            let random_num = rand::random::<u64>();
                                            response_message = format!("{}\r\n", random_num);
                                            stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                        }
                                        // send .
                                        response_message = format!(".\r\n");
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    }
                                },
                                "QUINE" => {
                                    // read server code from server.rs
                                    let mut f = std::fs::File::open("server.rs").expect("Cannot read from file");
                                    let mut server_code = String::new();
                                    f.read_to_string(&mut server_code).expect("Cannot read from file");
                                    // save each line of code in a vector
                                    let server_code_vec: Vec<&str> = server_code.split('\n').collect();
                                    response_message = format!("01 OK\r\n");
                                    // send 01 ok response
                                    stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    // send server code line by line
                                    for code_line in server_code_vec {
                                        response_message = format!("{}\r\n", code_line);
                                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    }
                                    // send dot on line by itself
                                    response_message = format!(".\r\n");
                                    stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                },
                                "KOAN" => {
                                    // send 01 ok response
                                    response_message = format!("01 OK\r\n");
                                    stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                    // send koan
                                    response_message = format!("A master who lived as a hermit on a mountain was asked by a\r\nmonk, \"What is the Way?\"\r\n\"What a fine mountain this is,\" the master said in reply\r\n\"I am not asking you about the mountain, but about the Way.\"\r\n\"So long as you cannot go beyond the mountain, my son, you\r\n cannot reach the Way,\" replied the master\r\n.\r\n");
                                    stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                                },
                                "GOODBYE" => {
                                    response_message = format!("99 GOODBYE\r\n");
                                    break;
                                },
                                "NEXT" => {
                                    // println!("next command");
                                    let mut data = String::new();
                                    let mut response_message = String::new();
                                    // get client's message until dot is encountered
                                    loop {
                                        // show prompt
                                        let prompt = "C: ";
                                        stream.write_all(prompt.as_bytes()).expect("Cannot write to stream");
                                        // get client's message
                                        let mut data_tmp = String::new();
                                        stream.read_to_string(&mut data_tmp).expect("Cannot read from stream");
                                        if data_tmp == ".\r\n" {
                                            break;
                                        } else {
                                            data.push_str(&data_tmp);
                                        }
                                    }
                                    // save client's message to a random file name
                                    let mut f = std::fs::File::create("random_file_name.txt").expect("Cannot create file");
                                    f.write_all(data.as_bytes()).expect("Cannot write to file");
                                    f.sync_data().expect("Cannot sync data");
                                    // set response message
                                    response_message = format!("01 OK\r\n");
                                }
                            }
                        }
                    },
                    _ => {
                        let response_message = "02 SYNTAX ERROR\r\n";
                        stream.write_all(response_message.as_bytes()).expect("Cannot write to stream");
                    }
                }
            }
        });
    }
}

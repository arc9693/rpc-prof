use rand::distributions::Alphanumeric;
use rand::{thread_rng, Rng};
use ttrpc::context::{self};
use ttrpc::Client;
use ttrpc_demo::proto::task;
use ttrpc_demo::proto::task_ttrpc;
use ttrpc_demo::utils;
use std::env;

fn generate_random_string(length: usize) -> String {
    let rng = thread_rng();
    let random_string: String = rng
        .sample_iter(&Alphanumeric)
        .take(length)
        .map(char::from)
        .collect();
    random_string
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        println!("Usage: {} <num_requests> <payload_size>", args[0]);
        return;
    }
    let num_requests: usize = args[1].parse().unwrap();
    let payload_size: usize = args[2].parse().unwrap();

    let c = Client::connect(utils::SOCK_ADDR).unwrap();
    let tc = task_ttrpc::TaskClient::new(c);

    // make 100 requests
    for i in 0..num_requests {
        let req = task::CreateTaskRequest {
            id: generate_random_string(payload_size),
            bundle: i.to_string(),
            terminal: true,
            stdin: "stdin".to_string(),
            stdout: "stdout".to_string(),
            stderr: "stderr".to_string(),
            checkpoint: "checkpoint".to_string(),
            parent_checkpoint: "parent_checkpoint".to_string(),
            special_fields: Default::default(),
        };
        let response = tc.create(context::with_timeout(0), &req).unwrap();
        println!("RESPONSE={:?}", response);
    }
}

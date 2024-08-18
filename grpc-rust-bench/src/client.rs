pub mod grpc_task {
    tonic::include_proto!("task");
}

use grpc_task::task_client::TaskClient;
use grpc_task::CreateTaskRequest;
use rand::{thread_rng, Rng};
use rand::distributions::Alphanumeric;
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

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        println!("Usage: {} <num_requests> <payload_size>", args[0]);
        return Ok(());
    }
    let num_requests: usize = args[1].parse().unwrap();
    let payload_size: usize = args[2].parse().unwrap();

    let mut client = TaskClient::connect("http://[::1]:50051").await?;
    for i in 0..num_requests{
        let request = tonic::Request::new(CreateTaskRequest {
            id: generate_random_string(payload_size),
            bundle: i.to_string(),
            terminal: true,
            stdin: "stdin".to_string(),
            stdout: "stdout".to_string(),
            stderr: "stderr".to_string(),
            checkpoint: "checkpoint".to_string(),
            parent_checkpoint: "parent_checkpoint".to_string(),
        });
        let response = client.create(request).await?;
        println!("RESPONSE={:?}", response);
    }

    Ok(())
}

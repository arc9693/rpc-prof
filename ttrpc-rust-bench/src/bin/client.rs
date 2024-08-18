use ttrpc::context::{self, Context};
use ttrpc::Client;
use ttrpc_demo::proto::task;
use ttrpc_demo::proto::task_ttrpc;
use ttrpc_demo::utils;
use rand::{thread_rng, Rng};
use rand::distributions::Alphanumeric;

fn generate_random_string(length: usize) -> String {
    let mut rng = thread_rng();
    let random_string: String = rng
        .sample_iter(&Alphanumeric)
        .take(length)
        .map(char::from)
        .collect();
    random_string
}

fn main() {
    let c = Client::connect(utils::SOCK_ADDR).unwrap();
    let tc = task_ttrpc::TaskClient::new(c);

    // make 100 requests
    for i in 0..100 {
        let req = task::CreateTaskRequest {
            id: generate_random_string((i+1)*10000),
            bundle: "bundle".to_string(),
            terminal: true,
            stdin: "stdin".to_string(),
            stdout: "stdout".to_string(),
            stderr: "stderr".to_string(),
            checkpoint: "checkpoint".to_string(),
            parent_checkpoint: "parent_checkpoint".to_string(),
            special_fields: Default::default(),
        };
        let resp = tc.create(default_ctx(), &req).unwrap();
        println!("Create task response: {:?}", resp);
    }
}

fn default_ctx() -> Context {
    let mut ctx = context::with_timeout(0);
    ctx.add("key-1".to_string(), "value-1-1".to_string());
    ctx.add("key-1".to_string(), "value-1-2".to_string());
    ctx.set("key-2".to_string(), vec!["value-2".to_string()]);

    ctx
}

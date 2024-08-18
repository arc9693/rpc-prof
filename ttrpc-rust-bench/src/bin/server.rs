

use ttrpc_demo::proto::task_ttrpc;
use ttrpc_demo::proto::task;
use ttrpc_demo::utils;
use std::sync::Arc;
use std::thread;
use memory_stats::memory_stats;



struct TaskService;
impl task_ttrpc::Task for TaskService {
    fn create(&self, _ctx: &ttrpc::TtrpcContext, _: task::CreateTaskRequest) -> ttrpc::Result<task::CreateTaskResponse> {
        // Create a dummy response
        let resp = task::CreateTaskResponse {
            pid: 123,
            special_fields: Default::default(),
        };
        print_memory_stats();
        Ok(resp)
    }
}

fn main() {
    let t = Box::new(TaskService {}) as Box<dyn task_ttrpc::Task + Send + Sync>;
    let t = Arc::new(t);
    let task_service = task_ttrpc::create_task(t);
    utils::remove_if_sock_exist(utils::SOCK_ADDR).unwrap();
    let mut server = ttrpc::Server::new()
    .bind(
        utils::SOCK_ADDR)
        .unwrap()
        .register_service(task_service);
    
        server.start().unwrap();

        // Hold the main thread until receiving signal SIGTERM
        let (tx, rx) = std::sync::mpsc::channel();
        thread::spawn(move || {
            ctrlc::set_handler(move || {
                tx.send(()).unwrap();
            })
            .expect("Error setting Ctrl-C handler");
            println!("Server is running, press Ctrl + C to exit");
        });
    
        rx.recv().unwrap();
    

}

static mut COUNTER: u32 = 0;
static mut TOTALRSS: usize = 0;
static mut TOTALVMS: usize = 0;
fn print_memory_stats() {
    let stats = memory_stats().unwrap();
    unsafe {
        COUNTER += 1;
        TOTALRSS += stats.physical_mem;
        TOTALVMS += stats.virtual_mem;
        print!("RSS: {} ", stats.physical_mem);
        print!("VMS: {} ", stats.virtual_mem);
        println!("Average RSS: {}", TOTALRSS as u32 / COUNTER);
        println!("Average VMS: {}", TOTALVMS as u32 / COUNTER);
    }
}

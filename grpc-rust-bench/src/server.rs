use tonic::{transport::Server, Request, Response, Status};
use memory_stats::memory_stats;
pub mod grpc_task {
    tonic::include_proto!("task");
}

use grpc_task::task_server::{Task, TaskServer};
use grpc_task::{CreateTaskRequest, CreateTaskResponse};


#[derive(Debug, Default)]
pub struct TaskService {}

#[tonic::async_trait]
impl Task for TaskService {
    async fn create(
        &self,
        _: Request<CreateTaskRequest>,
    ) -> Result<Response<CreateTaskResponse>, Status> {
        let reply = CreateTaskResponse {
            pid: 123,
        };
        print_memory_stats();
        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let ts = TaskService::default();
    println!("request_number,memory_rss,memory_vms,average_rss,average_vms");
    Server::builder()
        .add_service(TaskServer::new(ts))
        .serve(addr)
        .await?;

    Ok(())
}

// calculate memory stats
// average

static mut COUNTER: usize = 0;
static mut TOTALRSS: usize = 0;
static mut TOTALVMS: usize = 0;
fn print_memory_stats() {
    let stats = memory_stats().unwrap();
    unsafe {
        COUNTER += 1;
        TOTALRSS += stats.physical_mem;
        TOTALVMS += stats.virtual_mem;
        // print all in one line spaced by tab
        println!("{},{},{},{},{}", COUNTER, stats.physical_mem, stats.virtual_mem, TOTALRSS/COUNTER, TOTALVMS/COUNTER);
    }
}

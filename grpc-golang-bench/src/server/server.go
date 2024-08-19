package main

import (
	"context"
	"fmt"
	"grpc-demo/pb/task"
	"math/rand"
	"net"
	"os"
	"runtime"

	"google.golang.org/grpc"
)

const port = ":9000"

func main() {
	fmt.Printf("request_count,go_app_memory\n")
	runtime.GC()
	// defer profile.Start(profile.MemProfile, profile.MemProfileRate(1), profile.ProfilePath(".")).Stop()
	// create a new grpc server
	s := grpc.NewServer(grpc.UnaryInterceptor(serverInterceptor))

	lis, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	task.RegisterTaskServer(s, &taskService{})
	if err := s.Serve(lis); err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	// close the server
	defer s.Stop()

}

type taskService struct {
	task.UnimplementedTaskServer
}

func (s taskService) Create(ctx context.Context, r *task.CreateTaskRequest) (*task.CreateTaskResponse, error) {
	response := &task.CreateTaskResponse{
		Pid: uint32(rand.Intn(1000)),
	}
	return response, nil
}

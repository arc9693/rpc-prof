package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"runtime"
	"ttrpc-demo/pb/task"

	_ "net/http/pprof"

	"github.com/containerd/ttrpc"
)

const port = ":9002"

func main() {
	fmt.Printf("request_count,go_app_memory\n")
	runtime.GC()

	//defer profile.Start(profile.MemProfile, profile.MemProfileRate(1), profile.ProfilePath(".")).Stop()

	s, err := ttrpc.NewServer(
		ttrpc.WithUnaryServerInterceptor(serverInterceptor),
	)
	defer func() {
		if err := s.Close(); err != nil {
			log.Println(err)
		}
	}()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	lis, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	task.RegisterTaskService(s, &taskService{})
	if err := s.Serve(context.Background(), lis); err != nil {
		fmt.Fprintln(os.Stderr, err)
	}

}

type taskService struct {
	task.TaskService
}

func (s taskService) Create(ctx context.Context, r *task.CreateTaskRequest) (*task.CreateTaskResponse, error) {
	response := &task.CreateTaskResponse{
		Pid: uint32(rand.Intn(1000)),
	}
	return response, nil
}

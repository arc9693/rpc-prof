package main

import (
	"context"
	"fmt"
	"math/rand"
	"net"
	"os"
	"strconv"
	"ttrpc-demo/pb/task"

	"github.com/containerd/containerd/api/types"
	"github.com/containerd/ttrpc"
)

const port = ":9002"

func main() {
	// take a number as an argument
	if len(os.Args) != 3 {
		fmt.Fprintf(os.Stderr, "Usage: %s <port>\n", os.Args[0])
		os.Exit(1)
	}
	times, err := strconv.Atoi(os.Args[1])
	payloadSize, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to convert argument to int: %v\n", err)
		os.Exit(1)
	}
	conn, err := net.Dial("tcp", port)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to dial: %v \n", err)
		os.Exit(1)
	}
	client := task.NewTaskClient(ttrpc.NewClient(conn))
	for i := 0; i < times; i++ {
		// Generate a task request using random values in each iteration
		taskRequest := &task.CreateTaskRequest{
			Id:     fmt.Sprintf("task-%d", rand.Intn(times)),
			Bundle: fmt.Sprintf("bundle-%d", rand.Intn(times)),
			Rootfs: []*types.Mount{
				&types.Mount{
					Type:    fmt.Sprintf("type-%d", rand.Intn(times)),
					Source:  fmt.Sprintf("source-%d", rand.Intn(times)),
					Target:  fmt.Sprintf("target-%d", rand.Intn(times)),
					Options: []string{fmt.Sprintf("option1-%d", rand.Intn(times)), fmt.Sprintf("option2-%d", rand.Intn(times))},
				},
			},
			Terminal:         rand.Intn(2) == 0,
			Stdin:            fmt.Sprintf("stdin-%d", rand.Intn(times)),
			Stdout:           fmt.Sprintf("stdout-%d", rand.Intn(times)),
			Stderr:           fmt.Sprintf("stderr-%d", rand.Intn(times)),
			Checkpoint:       fmt.Sprintf("checkpoint-%d", rand.Intn(times)),
			ParentCheckpoint: fmt.Sprintf("parent_checkpoint-%d", rand.Intn(times)),
			Options:          nil,
		}
		// increase the size of the payload
		for j := 0; j < payloadSize; j++ {
			taskRequest.Rootfs = append(taskRequest.Rootfs, &types.Mount{
				Type:    fmt.Sprintf("type-%d", rand.Intn(times)),
				Source:  fmt.Sprintf("source-%d", rand.Intn(times)),
				Target:  fmt.Sprintf("target-%d", rand.Intn(times)),
				Options: []string{fmt.Sprintf("option1-%d", rand.Intn(times)), fmt.Sprintf("option2-%d", rand.Intn(times))},
			})
		}
		// send the request to the server
		_, err := client.Create(context.Background(), taskRequest)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		//fmt.Fprintln(os.Stdout, taskResponse.Pid)
	}
}

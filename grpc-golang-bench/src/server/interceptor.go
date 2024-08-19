package main

import (
	"context"
	"fmt"
	"runtime"

	"google.golang.org/grpc"
)

type ProfilingInterceptor struct {
	stasts map[string]*FunctionStats
}

type FunctionStats struct {
	Calls                 uint64
	TotalAllocationBefore uint64
	TotalHeapUsageBefore  uint64
	TotalObjectsBefore    uint64
	TotalAllocationAfter  uint64
	TotalHeapUsageAfter   uint64
	TotalObjectsAfter     uint64
}

var m runtime.MemStats

func NewProfilingInterceptor() *ProfilingInterceptor {
	return &ProfilingInterceptor{
		stats: make(map[string]*FunctionStats),
	}
}

var pi = NewProfilingInterceptor()

var count = 0

func serverInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, method grpc.UnaryHandler) (interface{}, error) {
	res, err := method(ctx, req)

	runtime.ReadMemStats(&m)
	count++
	sys := m.Sys
	heapReleased := m.HeapReleased
	goappmem := sys - heapReleased
	// Print the stats
	fmt.Printf("%d,%f\n", count, bToKb(goappmem))

	return res, err
}

func bToKb(b uint64) float64 {
	return float64(b) / 1024
}

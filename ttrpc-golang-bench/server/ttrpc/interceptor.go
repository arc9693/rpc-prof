package main

import (
	"context"
	"fmt"
	"runtime"

	"github.com/containerd/ttrpc"
)

type ProfilingInterceptor struct {
	stats map[string]*FunctionStats
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

func serverInterceptor(ctx context.Context, unmarshal ttrpc.Unmarshaler, info *ttrpc.UnaryServerInfo, method ttrpc.Method) (interface{}, error) {
	// Call the actual method which is implementation specific
	res, err := method(ctx, unmarshal)
	runtime.ReadMemStats(&m)
	sys := m.Sys
	heapReleased := m.HeapReleased
	goappmem := sys - heapReleased
	// Print the stats
	fmt.Printf("%f\t%f\t%f\t%d\n", bToKb(sys), bToKb(heapReleased), bToKb(goappmem), m.NumGC)

	return res, err
}

func bToKb(b uint64) float64 {
	return float64(b) / 1024
}

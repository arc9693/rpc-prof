package main

import (
	"context"
	"fmt"
	"runtime"

	"google.golang.org/grpc"
)

var m runtime.MemStats
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

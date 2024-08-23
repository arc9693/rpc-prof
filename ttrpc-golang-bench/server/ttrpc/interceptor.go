package main

import (
	"context"
	"fmt"
	"runtime"

	"github.com/containerd/ttrpc"
)

var count = 0
var m runtime.MemStats

func serverInterceptor(ctx context.Context, unmarshal ttrpc.Unmarshaler, info *ttrpc.UnaryServerInfo, method ttrpc.Method) (interface{}, error) {
	res, err := method(ctx, unmarshal)
	runtime.ReadMemStats(&m)
	sys := m.Sys
	heapReleased := m.HeapReleased
	goappmem := sys - heapReleased
	count++

	fmt.Printf("%d,%f\n", count, bToKb(goappmem))
	return res, err
}

func bToKb(b uint64) float64 {
	return float64(b) / 1024
}

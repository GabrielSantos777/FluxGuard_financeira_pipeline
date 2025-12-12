package main

import (
	"context"

	"github.com/jackc/pgx/v4"
)

func ConnectDB(connStr string) (*pgx.Conn, error) {
	return pgx.Connect(context.Background(), connStr)
}

package main

import "os"

func LoadConfig() string {
	connStr := os.Getenv("DATABASE_URL")
	if connStr == "" {
		panic("ERRO: DATABASE_URL não está definida.")
	}
	return connStr
}

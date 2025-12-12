package main

import (
	"context"
	"fmt"

	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()
	connStr := LoadConfig()

	conn, err := ConnectDB(connStr)
	if err != nil {
		fmt.Println("ERRO ao conectar ao banco:", err)
		return
	}
	defer conn.Close(context.Background())

	fmt.Println("Conexão com PostgreSQL OK!")

	ultima, err := BuscarUltimaCotacao(conn)
	if err != nil {
		fmt.Println("ERRO ao buscar cotação:", err)
		return
	}

	fmt.Println("\n--- Monitoramento Go ---")
	fmt.Printf("Última coleta: %s\n", ultima.TimestampColeta.Format("02-01-2006 15:04:05"))
	fmt.Printf("Compra (USD): R$ %.4f\n", ultima.ValorCompra)
}

package main

import (
	"context"
	"time"

	"github.com/jackc/pgx/v4"
)

type Cotacao struct {
	TimestampColeta time.Time
	ValorCompra     float64
}

func BuscarUltimaCotacao(conn *pgx.Conn) (*Cotacao, error) {
	query := `
		SELECT timestamp_coleta, valor_compra
		FROM cotacoes
		ORDER BY timestamp_coleta DESC
		LIMIT 1;
	`

	var c Cotacao

	err := conn.QueryRow(context.Background(), query).
		Scan(&c.TimestampColeta, &c.ValorCompra)

	if err != nil {
		return nil, err
	}

	return &c, nil
}

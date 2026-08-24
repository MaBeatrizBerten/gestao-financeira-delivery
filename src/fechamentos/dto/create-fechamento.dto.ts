export class CreateFechamentoDto {
  data: string;
  fundoTroco?: number;
  dinheiroGaveta?: number;
  totalDinheiro?: number;
  totalPix?: number;
  totalCartao?: number;
  totalIfood?: number;
  totalSaidasDinheiro?: number;
  sangria?: number;
  diferenca?: number;
  observacao?: string;

  // Aliases em snake_case para compatibilidade
  fundo_troco?: number;
  dinheiro_gaveta?: number;
  total_dinheiro?: number;
  total_pix?: number;
  total_cartao?: number;
  total_ifood?: number;
  total_saidas_dinheiro?: number;
}

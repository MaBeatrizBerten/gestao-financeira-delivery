import { IsString, IsNumber, IsOptional, IsIn, Min } from 'class-validator';

export class CreateLancamentoDto {
  @IsString()
  data!: string;

  @IsString()
  @IsIn(['Entrada', 'Saída'])
  tipo!: string;

  @IsString()
  categoria!: string;

  @IsOptional()
  @IsString()
  descricao?: string;

  @IsNumber()
  @Min(0.01)
  valor!: number;

  @IsOptional()
  @IsString()
  formaPagamento?: string;

  @IsOptional()
  @IsString()
  @IsIn(['Pago', 'Pendente'])
  status?: string;

  @IsOptional()
  @IsNumber()
  @Min(1)
  qtdPedidos?: number;
}

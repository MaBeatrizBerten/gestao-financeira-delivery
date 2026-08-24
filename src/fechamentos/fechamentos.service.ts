import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateFechamentoDto } from './dto/create-fechamento.dto';

export interface ResumoDia {
  vendasDinheiro: number;
  vendasPix: number;
  vendasCartao: number;
  vendasIfood: number;
  totalVendas: number;
  saidasDinheiro: number;
  totalSaidas: number;
  qtdPedidos: number;

  // Compatibilidade com snake_case
  vendas_dinheiro?: number;
  vendas_pix?: number;
  vendas_cartao?: number;
  vendas_ifood?: number;
  total_vendas?: number;
  saidas_dinheiro?: number;
  total_saidas?: number;
  qtd_pedidos?: number;
}

@Injectable()
export class FechamentosService {
  constructor(private prisma: PrismaService) {}

  /**
   * Equivalente ao 'obter_resumo_dia' do projeto em Python.
   * Busca os lançamentos do dia no Prisma e agrega os totais por forma de pagamento.
   */
  async obterResumoDia(data: string): Promise<ResumoDia> {
    const lancamentos = await this.prisma.lancamento.findMany({
      where: { data },
    });

    if (!lancamentos || lancamentos.length === 0) {
      return {
        vendasDinheiro: 0.0,
        vendasPix: 0.0,
        vendasCartao: 0.0,
        vendasIfood: 0.0,
        totalVendas: 0.0,
        saidasDinheiro: 0.0,
        totalSaidas: 0.0,
        qtdPedidos: 0,
        vendas_dinheiro: 0.0,
        vendas_pix: 0.0,
        vendas_cartao: 0.0,
        vendas_ifood: 0.0,
        total_vendas: 0.0,
        saidas_dinheiro: 0.0,
        total_saidas: 0.0,
        qtd_pedidos: 0,
      };
    }

    const entradas = lancamentos.filter(
      (l) => l.tipo?.trim().toLowerCase() === 'entrada',
    );
    const saidas = lancamentos.filter((l) => {
      const tipo = l.tipo?.trim().toLowerCase();
      return tipo === 'saída' || tipo === 'saida';
    });

    const isDinheiro = (fp: string) => fp?.trim().toLowerCase() === 'dinheiro';
    const isPix = (fp: string) => fp?.trim().toLowerCase() === 'pix';
    const isCartao = (fp: string) => {
      const normalizado = fp?.trim().toLowerCase() || '';
      const cartaoKeywords = [
        'cartão',
        'cartao',
        'crédito',
        'credito',
        'débito',
        'debito',
      ];
      return cartaoKeywords.some((kw) => normalizado.includes(kw));
    };
    const isIfood = (fp: string) => {
      const normalizado = fp?.trim().toLowerCase() || '';
      const ifoodKeywords = ['ifood', 'menudino', 'delivery', 'plataforma'];
      return ifoodKeywords.some((kw) => normalizado.includes(kw));
    };

    const vendasDinheiro = entradas
      .filter((l) => isDinheiro(l.formaPagamento))
      .reduce((acc, l) => acc + l.valor, 0);

    const vendasPix = entradas
      .filter((l) => isPix(l.formaPagamento))
      .reduce((acc, l) => acc + l.valor, 0);

    const vendasCartao = entradas
      .filter((l) => isCartao(l.formaPagamento))
      .reduce((acc, l) => acc + l.valor, 0);

    const vendasIfood = entradas
      .filter((l) => isIfood(l.formaPagamento))
      .reduce((acc, l) => acc + l.valor, 0);

    const totalVendas = entradas.reduce((acc, l) => acc + l.valor, 0);

    const saidasDinheiro = saidas
      .filter((l) => isDinheiro(l.formaPagamento))
      .reduce((acc, l) => acc + l.valor, 0);

    const totalSaidas = saidas.reduce((acc, l) => acc + l.valor, 0);

    const qtdPedidos = entradas.reduce(
      (acc, l) => acc + (l.qtdPedidos ?? 1),
      0,
    );

    const round = (num: number) => Number(num.toFixed(2));

    return {
      vendasDinheiro: round(vendasDinheiro),
      vendasPix: round(vendasPix),
      vendasCartao: round(vendasCartao),
      vendasIfood: round(vendasIfood),
      totalVendas: round(totalVendas),
      saidasDinheiro: round(saidasDinheiro),
      totalSaidas: round(totalSaidas),
      qtdPedidos,
      vendas_dinheiro: round(vendasDinheiro),
      vendas_pix: round(vendasPix),
      vendas_cartao: round(vendasCartao),
      vendas_ifood: round(vendasIfood),
      total_vendas: round(totalVendas),
      saidas_dinheiro: round(saidasDinheiro),
      total_saidas: round(totalSaidas),
      qtd_pedidos: qtdPedidos,
    };
  }

  /**
   * Salva um novo fechamento de caixa, calculando as diferenças da gaveta.
   */
  async salvarFechamentoCaixa(dto: CreateFechamentoDto) {
    const data = dto.data;
    const fundoTroco = dto.fundoTroco ?? dto.fundo_troco ?? 0;
    const dinheiroGaveta = dto.dinheiroGaveta ?? dto.dinheiro_gaveta ?? 0;
    const sangria = dto.sangria ?? 0;
    const observacao = dto.observacao ?? null;

    let totalDinheiro = dto.totalDinheiro ?? dto.total_dinheiro;
    let totalPix = dto.totalPix ?? dto.total_pix;
    let totalCartao = dto.totalCartao ?? dto.total_cartao;
    let totalIfood = dto.totalIfood ?? dto.total_ifood;
    let totalSaidasDinheiro =
      dto.totalSaidasDinheiro ?? dto.total_saidas_dinheiro;

    // Se os totais do dia não foram informados manualmente, busca via obterResumoDia
    if (
      totalDinheiro === undefined ||
      totalPix === undefined ||
      totalCartao === undefined ||
      totalIfood === undefined ||
      totalSaidasDinheiro === undefined
    ) {
      const resumo = await this.obterResumoDia(data);
      if (totalDinheiro === undefined) totalDinheiro = resumo.vendasDinheiro;
      if (totalPix === undefined) totalPix = resumo.vendasPix;
      if (totalCartao === undefined) totalCartao = resumo.vendasCartao;
      if (totalIfood === undefined) totalIfood = resumo.vendasIfood;
      if (totalSaidasDinheiro === undefined)
        totalSaidasDinheiro = resumo.saidasDinheiro;
    }

    // Cálculo da conferência da gaveta:
    // Dinheiro Esperado = Fundo Troco + Vendas em Dinheiro - Saídas em Dinheiro - Sangrias
    // Diferença = Dinheiro Gaveta - Dinheiro Esperado
    const dinheiroEsperado = Number(
      (fundoTroco + totalDinheiro - totalSaidasDinheiro - sangria).toFixed(2),
    );
    const diferenca = Number((dinheiroGaveta - dinheiroEsperado).toFixed(2));

    // Data/hora da criação no padrão YYYY-MM-DD HH:mm:ss
    const agora = new Date();
    const pad = (n: number) => String(n).padStart(2, '0');
    const criadoEm = `${agora.getFullYear()}-${pad(agora.getMonth() + 1)}-${pad(agora.getDate())} ${pad(agora.getHours())}:${pad(agora.getMinutes())}:${pad(agora.getSeconds())}`;

    return await this.prisma.fechamentoCaixa.create({
      data: {
        data,
        fundoTroco,
        dinheiroGaveta,
        totalDinheiro,
        totalPix,
        totalCartao,
        totalIfood,
        totalSaidasDinheiro,
        sangria,
        diferenca,
        observacao,
        criadoEm,
      },
    });
  }

  /**
   * Lista todos os fechamentos de caixa ordenados por data desc e id desc.
   */
  async listarTodos() {
    return await this.prisma.fechamentoCaixa.findMany({
      orderBy: [{ data: 'desc' }, { id: 'desc' }],
    });
  }

  /**
   * Busca um fechamento específico por ID.
   */
  async buscarPorId(id: number) {
    const fechamento = await this.prisma.fechamentoCaixa.findUnique({
      where: { id },
    });
    if (!fechamento) {
      throw new NotFoundException('Fechamento de caixa não encontrado');
    }
    return fechamento;
  }

  /**
   * Busca fechamentos por data.
   */
  async buscarPorData(data: string) {
    return await this.prisma.fechamentoCaixa.findMany({
      where: { data },
      orderBy: { id: 'desc' },
    });
  }

  /**
   * Remove um fechamento por ID.
   */
  async remover(id: number) {
    await this.buscarPorId(id);
    return await this.prisma.fechamentoCaixa.delete({
      where: { id },
    });
  }
}

import { Test, TestingModule } from '@nestjs/testing';
import { FechamentosService } from './fechamentos.service';
import { PrismaService } from '../prisma/prisma.service';

describe('FechamentosService', () => {
  let service: FechamentosService;
  let prisma: PrismaService;

  const mockPrisma = {
    lancamento: {
      findMany: jest.fn(),
    },
    fechamentoCaixa: {
      create: jest.fn(),
      findMany: jest.fn(),
      findUnique: jest.fn(),
      delete: jest.fn(),
    },
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        FechamentosService,
        {
          provide: PrismaService,
          useValue: mockPrisma,
        },
      ],
    }).compile();

    service = module.get<FechamentosService>(FechamentosService);
    prisma = module.get<PrismaService>(PrismaService);
    jest.clearAllMocks();
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('obterResumoDia', () => {
    it('deve retornar zeros quando não houver lançamentos no dia', async () => {
      mockPrisma.lancamento.findMany.mockResolvedValue([]);

      const resultado = await service.obterResumoDia('2026-08-24');

      expect(resultado.totalVendas).toBe(0);
      expect(resultado.vendasDinheiro).toBe(0);
      expect(resultado.vendasPix).toBe(0);
      expect(resultado.vendasCartao).toBe(0);
      expect(resultado.vendasIfood).toBe(0);
      expect(resultado.saidasDinheiro).toBe(0);
      expect(resultado.totalSaidas).toBe(0);
      expect(resultado.qtdPedidos).toBe(0);
    });

    it('deve agrupar corretamente os lançamentos por forma de pagamento', async () => {
      mockPrisma.lancamento.findMany.mockResolvedValue([
        {
          id: 1,
          data: '2026-08-24',
          tipo: 'Entrada',
          categoria: 'Dogueria',
          valor: 100,
          formaPagamento: 'Dinheiro',
          qtdPedidos: 2,
        },
        {
          id: 2,
          data: '2026-08-24',
          tipo: 'Entrada',
          categoria: 'Dogueria',
          valor: 50,
          formaPagamento: 'Pix',
          qtdPedidos: 1,
        },
        {
          id: 3,
          data: '2026-08-24',
          tipo: 'Entrada',
          categoria: 'Dogueria',
          valor: 80,
          formaPagamento: 'Cartão de Débito',
          qtdPedidos: 2,
        },
        {
          id: 4,
          data: '2026-08-24',
          tipo: 'Entrada',
          categoria: 'iFood',
          valor: 120,
          formaPagamento: 'iFood / Repasse',
          qtdPedidos: 3,
        },
        {
          id: 5,
          data: '2026-08-24',
          tipo: 'Saída',
          categoria: 'Insumos',
          valor: 30,
          formaPagamento: 'Dinheiro',
          qtdPedidos: 1,
        },
        {
          id: 6,
          data: '2026-08-24',
          tipo: 'Saída',
          categoria: 'Energia',
          valor: 70,
          formaPagamento: 'Pix',
          qtdPedidos: 1,
        },
      ]);

      const resultado = await service.obterResumoDia('2026-08-24');

      expect(resultado.vendasDinheiro).toBe(100);
      expect(resultado.vendasPix).toBe(50);
      expect(resultado.vendasCartao).toBe(80);
      expect(resultado.vendasIfood).toBe(120);
      expect(resultado.totalVendas).toBe(350);
      expect(resultado.saidasDinheiro).toBe(30);
      expect(resultado.totalSaidas).toBe(100);
      expect(resultado.qtdPedidos).toBe(8);
    });
  });

  describe('salvarFechamentoCaixa', () => {
    it('deve calcular a diferença da gaveta corretamente e persistir no banco', async () => {
      mockPrisma.lancamento.findMany.mockResolvedValue([
        {
          id: 1,
          data: '2026-08-24',
          tipo: 'Entrada',
          categoria: 'Dogueria',
          valor: 200,
          formaPagamento: 'Dinheiro',
          qtdPedidos: 4,
        },
        {
          id: 2,
          data: '2026-08-24',
          tipo: 'Saída',
          categoria: 'Pão',
          valor: 40,
          formaPagamento: 'Dinheiro',
          qtdPedidos: 1,
        },
      ]);

      mockPrisma.fechamentoCaixa.create.mockImplementation(({ data }) =>
        Promise.resolve({ id: 1, ...data }),
      );

      const dto = {
        data: '2026-08-24',
        fundoTroco: 50,
        sangria: 30,
        dinheiroGaveta: 180, // Esperado: 50 + 200 - 40 - 30 = 180 => Diferença = 0
        observacao: 'Turno da noite ok',
      };

      const resultado = await service.salvarFechamentoCaixa(dto);

      expect(resultado.fundoTroco).toBe(50);
      expect(resultado.totalDinheiro).toBe(200);
      expect(resultado.totalSaidasDinheiro).toBe(40);
      expect(resultado.sangria).toBe(30);
      expect(resultado.dinheiroGaveta).toBe(180);
      expect(resultado.diferenca).toBe(0);
      expect(mockPrisma.fechamentoCaixa.create).toHaveBeenCalledTimes(1);
    });

    it('deve calcular sobra positiva ou falta negativa na gaveta', async () => {
      mockPrisma.lancamento.findMany.mockResolvedValue([]);
      mockPrisma.fechamentoCaixa.create.mockImplementation(({ data }) =>
        Promise.resolve({ id: 2, ...data }),
      );

      // Fundo = 100, Total vendas = 0, Saídas = 0, Sangria = 0 => Esperado: 100.
      // Gaveta contada = 95 => Falta de 5 (diferenca = -5)
      const dto = {
        data: '2026-08-24',
        fundoTroco: 100,
        dinheiroGaveta: 95,
        totalDinheiro: 0,
        totalPix: 0,
        totalCartao: 0,
        totalIfood: 0,
        totalSaidasDinheiro: 0,
        sangria: 0,
      };

      const resultado = await service.salvarFechamentoCaixa(dto);
      expect(resultado.diferenca).toBe(-5);
    });
  });
});

import { Test, TestingModule } from '@nestjs/testing';
import { FechamentosController } from './fechamentos.controller';
import { FechamentosService } from './fechamentos.service';

describe('FechamentosController', () => {
  let controller: FechamentosController;
  let service: FechamentosService;

  const mockFechamentosService = {
    obterResumoDia: jest.fn(),
    salvarFechamentoCaixa: jest.fn(),
    listarTodos: jest.fn(),
    buscarPorId: jest.fn(),
    buscarPorData: jest.fn(),
    remover: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [FechamentosController],
      providers: [
        {
          provide: FechamentosService,
          useValue: mockFechamentosService,
        },
      ],
    }).compile();

    controller = module.get<FechamentosController>(FechamentosController);
    service = module.get<FechamentosService>(FechamentosService);
    jest.clearAllMocks();
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('obterResumo', () => {
    it('deve chamar service.obterResumoDia com a data fornecida via query', async () => {
      mockFechamentosService.obterResumoDia.mockResolvedValue({ totalVendas: 100 });

      const res = await controller.obterResumo('2026-08-24');

      expect(service.obterResumoDia).toHaveBeenCalledWith('2026-08-24');
      expect(res).toEqual({ totalVendas: 100 });
    });
  });

  describe('obterResumoPorParam', () => {
    it('deve chamar service.obterResumoDia com o parâmetro de rota', async () => {
      mockFechamentosService.obterResumoDia.mockResolvedValue({ totalVendas: 150 });

      const res = await controller.obterResumoPorParam('2026-08-24');

      expect(service.obterResumoDia).toHaveBeenCalledWith('2026-08-24');
      expect(res).toEqual({ totalVendas: 150 });
    });
  });

  describe('criar', () => {
    it('deve chamar service.salvarFechamentoCaixa com o DTO', async () => {
      const dto = {
        data: '2026-08-24',
        fundoTroco: 50,
        dinheiroGaveta: 100,
      };
      mockFechamentosService.salvarFechamentoCaixa.mockResolvedValue({ id: 1, ...dto });

      const res = await controller.criar(dto);

      expect(service.salvarFechamentoCaixa).toHaveBeenCalledWith(dto);
      expect(res).toHaveProperty('id', 1);
    });
  });

  describe('listar', () => {
    it('deve listar todos quando sem query data', async () => {
      mockFechamentosService.listarTodos.mockResolvedValue([{ id: 1 }]);

      const res = await controller.listar();

      expect(service.listarTodos).toHaveBeenCalled();
      expect(res).toEqual([{ id: 1 }]);
    });

    it('deve buscar por data quando fornecida a query data', async () => {
      mockFechamentosService.buscarPorData.mockResolvedValue([{ id: 2, data: '2026-08-24' }]);

      const res = await controller.listar('2026-08-24');

      expect(service.buscarPorData).toHaveBeenCalledWith('2026-08-24');
      expect(res).toEqual([{ id: 2, data: '2026-08-24' }]);
    });
  });

  describe('buscarPorId', () => {
    it('deve buscar por id', async () => {
      mockFechamentosService.buscarPorId.mockResolvedValue({ id: 1 });

      const res = await controller.buscarPorId(1);

      expect(service.buscarPorId).toHaveBeenCalledWith(1);
      expect(res).toEqual({ id: 1 });
    });
  });

  describe('remover', () => {
    it('deve remover fechamento por id', async () => {
      mockFechamentosService.remover.mockResolvedValue({ id: 1 });

      const res = await controller.remover(1);

      expect(service.remover).toHaveBeenCalledWith(1);
      expect(res).toEqual({ id: 1 });
    });
  });
});

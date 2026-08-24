import { Test, TestingModule } from '@nestjs/testing';
import { LancamentosService } from './lancamentos.service';
import { PrismaService } from '../prisma/prisma.service';

describe('LancamentosService', () => {
  let service: LancamentosService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        LancamentosService,
        {
          provide: PrismaService,
          useValue: {
            lancamento: {
              create: jest.fn(),
              findMany: jest.fn(),
              findUnique: jest.fn(),
              update: jest.fn(),
              delete: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get<LancamentosService>(LancamentosService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});

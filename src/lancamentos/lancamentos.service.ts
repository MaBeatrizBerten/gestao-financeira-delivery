import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { Prisma } from '@prisma/client';

@Injectable()
export class LancamentosService {
  constructor(private prisma: PrismaService) {}

  async criar(data: Prisma.LancamentoCreateInput) {
    return await this.prisma.lancamento.create({
      data,
    });
  }

  async listarTodos() {
    return await this.prisma.lancamento.findMany({
      orderBy: [{ data: 'desc' }, { id: 'desc' }],
    });
  }

  async buscarPorId(id: number) {
    const lancamento = await this.prisma.lancamento.findUnique({
      where: { id },
    });
    if (!lancamento) throw new NotFoundException('Lançamento não encontrado');
    return lancamento;
  }

  async atualizar(id: number, data: Prisma.LancamentoUpdateInput) {
    await this.buscarPorId(id); // Verifica se existe
    return await this.prisma.lancamento.update({
      where: { id },
      data,
    });
  }

  async remover(id: number) {
    await this.buscarPorId(id); // Verifica se existe
    return await this.prisma.lancamento.delete({
      where: { id },
    });
  }
}

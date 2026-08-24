import {
  Controller,
  Get,
  Post,
  Delete,
  Body,
  Param,
  Query,
  ParseIntPipe,
} from '@nestjs/common';
import { FechamentosService } from './fechamentos.service';
import { CreateFechamentoDto } from './dto/create-fechamento.dto';

@Controller('fechamentos')
export class FechamentosController {
  constructor(private readonly fechamentosService: FechamentosService) {}

  /**
   * GET /fechamentos/resumo?data=YYYY-MM-DD
   * Retorna os totais agrupados por forma de pagamento para a data indicada.
   */
  @Get('resumo')
  async obterResumo(@Query('data') data?: string) {
    const dataConsulta =
      data || new Date().toISOString().split('T')[0];
    return await this.fechamentosService.obterResumoDia(dataConsulta);
  }

  /**
   * GET /fechamentos/resumo/:data
   * Rota alternativa para obter o resumo do dia via URL param.
   */
  @Get('resumo/:data')
  async obterResumoPorParam(@Param('data') data: string) {
    return await this.fechamentosService.obterResumoDia(data);
  }

  /**
   * POST /fechamentos
   * Salva um novo fechamento de caixa, calculando a conferência e diferença da gaveta.
   */
  @Post()
  async criar(@Body() createFechamentoDto: CreateFechamentoDto) {
    return await this.fechamentosService.salvarFechamentoCaixa(
      createFechamentoDto,
    );
  }

  /**
   * GET /fechamentos
   * Lista todos os fechamentos de caixa ou filtra por ?data=YYYY-MM-DD.
   */
  @Get()
  async listar(@Query('data') data?: string) {
    if (data) {
      return await this.fechamentosService.buscarPorData(data);
    }
    return await this.fechamentosService.listarTodos();
  }

  /**
   * GET /fechamentos/:id
   * Busca um fechamento específico pelo ID.
   */
  @Get(':id')
  async buscarPorId(@Param('id', ParseIntPipe) id: number) {
    return await this.fechamentosService.buscarPorId(id);
  }

  /**
   * DELETE /fechamentos/:id
   * Exclui um fechamento de caixa pelo ID.
   */
  @Delete(':id')
  async remover(@Param('id', ParseIntPipe) id: number) {
    return await this.fechamentosService.remover(id);
  }
}

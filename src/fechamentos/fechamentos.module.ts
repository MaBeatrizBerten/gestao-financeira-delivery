import { Module } from '@nestjs/common';
import { FechamentosService } from './fechamentos.service';
import { FechamentosController } from './fechamentos.controller';

@Module({
  providers: [FechamentosService],
  controllers: [FechamentosController]
})
export class FechamentosModule {}

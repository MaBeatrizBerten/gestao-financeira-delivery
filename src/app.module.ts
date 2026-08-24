import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrismaModule } from './prisma/prisma.module';
import { LancamentosModule } from './lancamentos/lancamentos.module';
import { FechamentosModule } from './fechamentos/fechamentos.module';

@Module({
  imports: [PrismaModule, LancamentosModule, FechamentosModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

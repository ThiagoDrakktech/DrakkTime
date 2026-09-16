# DrakkTime
Software para cálculo de horas extras.

## Funcionalidades implementadas
- Cadastro de colaborador com: nome, sobrenome, CPF, cargo e período trabalhado.
- Registro de jornada com:
  - entrada
  - saída para almoço
  - retorno do almoço
  - término do expediente
  - retorno pós-expediente (opcional) com nova baixa
- Cálculo de horas extras por colaborador.
- Geração de tabela final com total de horas extras.

## Regras de jornada
- **Gerente**: 44h semanais.
- **Assistente Administrativo**: 44h semanais.
- **Auxiliar de Manutenção**: 44h semanais.
- **Oficial de manutenção**: escala 12/36 (referência diária de 12h).

Para cargos de 44h semanais:
- `todo_sabado`: 8h de segunda a sexta e 4h no sábado.
- `alternado`: compensação durante a semana (8h48 de segunda a sexta), com sábado sem carga horária padrão.

## Executar testes
```bash
python -m unittest discover -s tests
```

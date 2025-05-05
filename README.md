# Placar Interativo 🎮🏀

![Interface de Controle](controlador.png)  
![Placar Interativo](placar.png)

## Linguagens e Tecnologias 🛠️
- **Python 🐍**: Lógica principal do projeto.
- **PyQt5 🖼️**: Interface gráfica para as janelas do placar e controle.
- **Sockets (TCP) 🔌**: Comunicação entre a interface de controle e o placar.

## Arquivos 📂
- **placar.py**: Exibe o placar interativo com timer, nomes e pontuações.
- **controle.py**: Interface para atualizar nomes, período, timer, selecionar ícones e executar ações rápidas.

## Instalação e Execução 🚀

1. **Instale o PyQt5:**
   ```bash
   pip install PyQt5
   ```

2. **Instale a fonte Digital-7:**
   - Caso a fonte **Digital-7** não esteja instalada, baixe-a [aqui](https://www.dafont.com/digital-7.font) (ou utilize outro link de sua preferência) e instale-a no seu sistema.

3. **Inicie o projeto:**
   - Rode o arquivo `main.py`:
     ```bash
     python main.py
     ```

## Observações 📌
- As atualizações enviadas pelo controle são recebidas pelo placar via socket TCP 📡.
- No modo decrescente, o timer decrementa até chegar a zero, onde ele para automaticamente 🛑.
- As janelas são configuradas para serem leves e integradas ao ambiente de streaming, possibilitando uma personalização fácil 🎨.
- **Atenção:** Caso a fonte **Digital-7** não esteja instalada no sistema, instale-a para que os números sejam exibidos corretamente.

Sinta-se à vontade para ajustar as configurações e personalizar o projeto conforme suas necessidades. Divirta-se! 😄🎉

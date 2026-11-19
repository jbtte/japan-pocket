# Japão Pocket — HTML/PWA + um JSON por dia

Este projeto separa **interface fixa** (HTML/CSS/JavaScript) de **conteúdo** (JSON). O GitHub Actions gera o índice e publica o site automaticamente: para um novo roteiro, basta enviar **um novo JSON** em `data/`.

## Estrutura

```text
index.html                   App (layout)
assets/style.css             Estilo mobile-first
assets/app.js                Renderização, Google Maps, progresso
sw.js                        Cache e uso offline
manifest.webmanifest         PWA
icons/icon.svg               Ícone
 data/tokyo-03.json          Roteiro real de exemplo
 data/_modelo.json           Exemplo para criar novos dias
 data/days.json              Índice gerado automaticamente (não editar)
 scripts/build_index.py      Gera o índice dos dias
 .github/workflows/pages.yml Publicação automática no GitHub Pages
```

## Publicar a primeira vez

1. Crie um repositório GitHub público chamado, por exemplo, `japao-pocket`.
2. Envie **todos** os arquivos do ZIP, incluindo a pasta `.github` (ela pode ficar oculta no explorador).
3. No repositório: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Acesse **Actions** e verifique o workflow `Publicar guia de viagem`. Se necessário, execute `Run workflow`.
5. Abra `https://SEU_USUARIO.github.io/japao-pocket/`.
6. No Chrome do celular, toque em **Salvar todos os roteiros offline**. Confirme a mensagem antes de testar em modo avião.

## Uso diário (um único JSON)

1. Copie `data/_modelo.json` e preencha o dia, como `data/kyoto-01.json`. Use IDs únicos e estáveis para o dia e cada parada.
2. Faça commit/upload **apenas desse novo arquivo** para `data/` no ramo `main`.
3. GitHub Actions detectará o push, gerará a lista de dias e publicará a versão atualizada.
4. **Ainda com internet no celular**, abra o guia e toque novamente em **Salvar todos os roteiros offline** para baixar o novo dia.

Para testar/visualizar localmente antes de publicar: `python3 scripts/build_index.py && python3 -m http.server 8000` e acesse `http://localhost:8000` no computador. Para testar service worker no celular, use GitHub Pages (HTTPS).

## Campos por parada

- `id` (estável), `time`, `end`, `title`, `kind`, `priority` (`essencial`, `opcional` ou `flexivel`).
- `context`: por que visitar; `observe`: o que observar/fazer.
- `location`: `query` (destino), `from` (origem), `mode` (`walking`, `transit` etc.).
- `transport`: instrução curta; `next`: próxima etapa.
- `links`: lugares menores dentro da parada, com links do Maps.
- `foods`: sugestões de pratos/snacks, com `name`, `place`, `why`, `query`, `optional`.
- No nível do dia: `suica`, `notes`, `source`, `intro`, `date`, `city`, `title`.

## Limitações e cuidados

- O site e os roteiros baixados funcionam offline; Google Maps **não** garante rotas a pé ou de transporte público sem conexão.
- O botão de offline precisa ser usado novamente após publicar novos roteiros.
- O checklist usa armazenamento local do navegador, não sincroniza entre aparelhos.
- Dados e links do JSON são publicados: não inclua segredos ou informações privadas.
- Para instalação PWA consistente entre navegadores, pode ser necessário acrescentar ícones PNG 192/512 ao manifest; o atalho à tela inicial pode funcionar sem isso.
- Se o GitHub Pages ainda não estiver configurado, o workflow não conseguirá publicar até escolher **Source: GitHub Actions** em Settings → Pages.

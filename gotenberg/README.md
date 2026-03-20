# POC Gotenberg (`pdf-poc`)

[Gotenberg](https://gotenberg.dev/) é um serviço em Docker que expõe uma API HTTP para converter **HTML → PDF** usando **Chromium** (e outras rotas para Office, merge, etc.).

Este POC reutiliza o `template.html` e `styles.css` na raiz de `pdf-poc/` (os mesmos usados pelo fluxo WeasyPrint).

## Pré-requisitos

- Docker (Docker Compose v2)
- Python 3.10+ com `httpx`:

  ```bash
  pip install httpx
  ```

  Ou, a partir da raiz de `pdf-poc/`:

  ```bash
  pip install -r requirements.txt
  ```

## Subir o Gotenberg

```bash
cd pdf-poc/gotenberg
docker compose up -d
```

Health check: <http://127.0.0.1:3049/health> (porta definida em `docker-compose.yml`)

## Gerar o PDF

Na pasta `pdf-poc/`:

```bash
python gotenberg/convert_to_pdf.py
```

Saída: `pdf-poc/output-gotenberg.pdf`

Outro host/porta:

```bash
GOTENBERG_URL=http://localhost:3000 python gotenberg/convert_to_pdf.py
```

## Parar o container

```bash
cd pdf-poc/gotenberg
docker compose down
```

## Notas

- O formulário multipart exige o HTML principal como arquivo chamado **`index.html`**; o script envia `template.html` com esse nome.
- O `template.html` referencia `styles.css` e fontes do Google; o Chromium no container precisa de **rede** para baixar as fontes (padrão do Compose).
- Para produção: não exponha o Gotenberg publicamente sem autenticação/rede privada; renderizar HTML arbitrário tem riscos de segurança.

## Documentação

- Rotas HTML: <https://gotenberg.dev/docs/routes#html>

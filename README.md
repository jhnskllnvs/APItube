# --- DESCRIÇÃO BÁSICA --- #
Primeira API de minha autoria. Feita em python usando FastAPI e SQLAlchemy. Baseada no desafio Alura de Backend.

> Essa API roda em localhost, no endereço padrão que o uvicorn oferece (127.0.0.1:8000)

> Ela é feita com um banco de dados relacional MySQL em mente (Versão MySQL: 8.0)

> Usuário root, senha root. Nesse sentido, não há medidas de segurança instauradas.

# --- PROBLEMAS CONHECIDOS --- #

> Você pode criar e apagar usuários sem um login.

> Você pode acessar páginas adicionais no método get_free_videos mudando os parâmetros.

> Você consegue ver, no código fonte em main.py, a "key" (um hex32 aleatóriamente gerado pelo shell do OpenSSL) e o algorítimo usado para a geração do token.

> A busca do usuário atual retorna a hash da sua senha.

> A busca por categorias é em título ao invés de ID.

> O método update_video requer todas as informações colocadas novamente para funcionar.

# --- CONSIDERAÇÕES FINAIS --- #

Esta primeira API, apesar das vulnerabilidades e defeitos, será base para futuras APIs similares que eu fizer.

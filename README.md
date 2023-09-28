# APItube
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

Pretendo cuidar de todos os problemas listado em meu próximo projeto. Esta API já levou bastante esforço e vários dias para completar, e é fruto dos meus atuais estudos. Não é um projeto muito ambicioso, mas vai ser base para muitas coisas que farei futuramente (especialmente porque eu não quero escrever 100 linhas de novo para fazer um sistema de autenticação, por mais "frouxo" que este seja).

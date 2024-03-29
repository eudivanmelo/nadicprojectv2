# CRM para Empresa de Manutenção de Computadores

Este é um projeto de Sistema de CRM desenvolvido em Django para auxiliar empresas que oferecem serviços básicos de manutenção de computadores, como formatação, limpeza e substituição de peças. O CRM permite que a empresa gerencie eficientemente seus clientes, agendamentos de serviços, ordens de serviço e pagamentos, proporcionando uma melhor experiência para os clientes e facilitando o controle interno das operações.

## Funcionalidades Principais

- Cadastro e gerenciamento de clientes.
- Registro e agendamento de serviços oferecidos.
- Acompanhamento de ordens de serviço, incluindo status e observações.
- Registro de pagamentos feitos pelos clientes.
- Visualização de métricas importantes através de um dashboard.
- Fácil navegação e usabilidade para os usuários.

## Tecnologias Utilizadas

- Django: Framework web em Python para o desenvolvimento do backend.
- HTML/CSS: Para a criação da interface do usuário.
- Bootstrap: Para facilitar o design responsivo da aplicação.
- SQLite: Banco de dados leve e fácil de usar, adequado para projetos de pequeno porte.

## Instruções de Instalação

1. Clone este repositório para o seu ambiente local.
2. Instale as dependências listadas no arquivo `requirements.txt` usando o comando `pip install -r requirements.txt`.
3. Execute as migrações do banco de dados com o comando `python manage.py migrate`.
4. Inicie o servidor de desenvolvimento com `python manage.py runserver`.
5. Acesse a aplicação no navegador através do endereço `http://localhost:8000`.

## ToDo List

- [ ] Implementar a funcionalidade de cadastro e gerenciamento de clientes.
- [ ] Desenvolver o sistema de agendamento de serviços.
- [ ] Criar a interface para acompanhar ordens de serviço.
- [ ] Implementar a funcionalidade de registro de pagamentos.
- [ ] Desenvolver um dashboard para visualização de métricas.
- [ ] Realizar testes de unidade para garantir a qualidade do código.
- [ ] Aprimorar o design e a usabilidade da aplicação.
- [ ] Documentar o código e adicionar comentários onde necessário.

## Lista de Páginas

- Página inicial/dashboard
- Página de Login
- Página de Clientes
- Página de Serviços
- Página de Agendamento
- Página de Ordem de Serviço
- Página de Pagamento

Este projeto está em fase inicial de desenvolvimento e novas funcionalidades serão adicionadas conforme necessário. Contribuições são bem-vindas e encorajadas. Se você tiver alguma sugestão ou encontrar algum problema, por favor, abra uma nova issue ou envie um pull request.

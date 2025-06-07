# TECH_flask_chat
Flask App as an educational lab for AI and IoT.
Aplicação Flask como laboratório didático para IA e IoT.

With many thanks to Miguel Grinberg (https://github.com/miguelgrinberg) for his Flask Mega-Tutorial (https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

AI-aided development.

___

## Aplicação inicial
O objetivo desta versão é apresentar o framework Flask.

Esta aplicação consiste em dois clientes de chat: usuario e atendente e cada cliente um mantém seu próprio log de conversa (`usuario.log` e `atendente.log`, respectivamente). No entanto, ainda não se conversam de fato.

### Recursos:
* Framework Flask: `flask`
* Para expansão modular: Blueprint e Jinja2
* Uso de variáveis de ambiente: `python-dotenv`

## Na primeira vez que usar este pacote
* Faça download do repositório.
* Descompacte o arquivo em uma pasta no seu computador, **DE FORMA ORGANIZADA**.
* Na pasta flask_app, clique com o botão direito do mouse e selecione `Mostrar mais opções` --> `Abrir com Code` (opção de menu com o ícone do VSCode).
* Crie e configure um ambiente virtual
    * Abra um terminal no VSCode e execute:
    * `python.exe -m venv .venv`
    * `.venv\Scripts\Activate`
    * Isso ativa o ambiente virtual e o prompt deverá mudar, passando a mostrar `(.venv)` no início da linha. Digite:
        * `python.exe -m pip install --upgrade pip`
        * `pip install flask python-dotenv`

           Agora você pode executar a aplicação:
        * `flask run`

## Quando usar nas próximas vezes, digite:
* `.venv\Scripts\Activate`
* `flask run`

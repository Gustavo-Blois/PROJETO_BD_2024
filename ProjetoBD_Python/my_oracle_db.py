import getpass
import oracledb

def login():
    un = 'adgmr'
    cs = 'orclgrad1.icmc.usp.br/pdb_elaine.icmc.usp.br'
    pw = getpass.getpass(f'Enter password for {un}@{cs}: ')
    try:
        connection = oracledb.connect(user=un, password=pw, dsn=cs)
        print("Conexão estabelecida com sucesso!")
        return connection
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
def menu_atletas(connection):
    tecla_do_usuario = ''  
    while(True): 
        tecla_do_usuario = input("""
            \033[2J
            \033[H 
            MENU ATLETAS
            Pressione 'q' para sair
            Pressione 'c' para adicionar um atleta à base de dados 
            pressione 'o' para verificar objetivos de desenvolvimento de um atleta
            """)
        match tecla_do_usuario:
            case 'c':
                adicionar_atleta(connection)
            case 'o':
                objetivos_atleta(connection)
            case 'q':
                break
            case _:
                pass

def adicionar_atleta(connection):
    # Solicitar informações do atleta
    nome_atleta = input("\033[2J\033[HQual o nome do atleta? ")
    cpf_atleta = input("Qual o CPF do atleta no formato XXX.XXX.XXX-XX? ")
    data_nascimento = input("Qual a data de nascimento do atleta no formato YYYY-MM-DD? ")
    clube_ou_equipe = input("A qual clube ou equipe o atleta pertence? ")
    mentor = input("Qual o CPF do mentor do atleta? ")
    escolaridade = input("Qual a escolaridade do atleta? ")
    num_telefone = input("Qual o número de telefone do atleta no formato (XX)XXXXX-XXXX? ")
    pais = input("Qual o país do atleta? ")
    estado = input("Qual o estado do atleta no formato XX? ")
    cidade = input("Qual a cidade do atleta? ")
    logradouro = input("Qual o endereço do atleta? ")
    numero = input("Qual o número da residência do atleta? ")
    complemento = input("Algum complemento ao endereço? ")
    input_geral = (
        nome_atleta + cpf_atleta + data_nascimento + clube_ou_equipe + mentor +
        escolaridade + num_telefone + pais + estado + cidade + logradouro + numero + complemento
    )
    if not input_seguro(input_geral):  # Verificar se a entrada é segura
        print("Erro na inserção: entrada contém dados inadequados.")
        input("Pressione Enter para continuar...")
        return

    # Inserção no banco de dados
    try:
        with connection.cursor() as cursor:
            # Primeiro, inserir na tabela PESSOA
            sql_pessoa = "INSERT INTO PESSOA (CPF, TIPO) VALUES (:1, 'ATLETA')"
            cursor.execute(sql_pessoa, [cpf_atleta])

            # Depois, inserir na tabela ATLETA
            sql_atleta = """
                INSERT INTO ATLETA (
                    PESSOA, CLUBE_OU_EQUIPE, NOME, MENTOR, DATA_NASC, ESCOLARIDADE,
                    NUM_TELEFONE, PAIS, ESTADO, CIDADE, LOGRADOURO, NUMERO, COMPLEMENTO
                ) VALUES (
                    :1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8, :9, :10, :11, :12, :13
                )
            """
            cursor.execute(sql_atleta, [
                cpf_atleta, clube_ou_equipe, nome_atleta, mentor, data_nascimento,
                escolaridade, num_telefone, pais, estado, cidade, logradouro, numero, complemento
            ])

            # Confirmar transação
            connection.commit()

        print("Atleta adicionado com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao inserir atleta no banco de dados: {e}")
        connection.rollback()  # Desfazer alterações em caso de erro
    finally:
        input("Pressione Enter para continuar")

def objetivos_atleta(connection):
    input_usuario = input("\033[2J\033[HQual o nome do atleta? ")
    if input_seguro(input_usuario):
        sql = """SELECT A.NOME, O.NUM_OBJETIVO,O.DESCRICAO, O.STATUS
                FROM ATLETA A
                JOIN OBJETIVO_DE_DESENVOLVIMENTO O
                ON UPPER(A.NOME) = UPPER(:1) AND A.PESSOA = O.ATLETA 
                """
        with connection.cursor() as cursor:
            for r in cursor.execute(sql,(input_usuario,)):
                print(r)
            while(input("Pressione Enter para continuar") != ''):
                pass
    else:
        print("Erro na consulta, a entrada não está adequada")
        input("Pressione Enter para continuar")


def menu_mentores(connection):
    tecla_do_usuario = ''  
    while(True): 
        tecla_do_usuario = input("""
            \033[2J\033[HMENU ATLETAS
            Pressione 'q' para sair
            Pressione 'a' para verificar os atletas mentorados por um mentor 
            """)
        match tecla_do_usuario:
            case 'a':
                atletas_mentorados(connection)
            case 'q':
                break
            case _:
                pass

def atletas_mentorados(connection):
    input_usuario = input("\033[2J\033[HQual o nome do mentor? ")
    if input_seguro(input_usuario):
        sql = """
                SELECT A.NOME, A.CLUBE_OU_EQUIPE
                FROM MENTOR M JOIN ATLETA A
                ON UPPER(M.NOME) = UPPER(:1) AND A.MENTOR = M.PESSOA
                """ # TODO: COLOCAR QUERY ADEQUADA
        with connection.cursor() as cursor:
            for r in cursor.execute(sql,(input_usuario,)):
                print(r)
            input("Pressione Enter para continuar")
    else:
        print("Erro na consulta, a entrada não está adequada")
        while(input("Pressione Enter para continuar") != ''):
                pass


def input_seguro(input_usuario):
    substrings_proibidas = [",","'",";","--"]

    for substring in substrings_proibidas:
        if substring in input_usuario:
            return False
    return True


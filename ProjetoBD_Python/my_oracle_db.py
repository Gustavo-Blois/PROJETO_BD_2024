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
    

def adicionar_atleta(connection):
    # Solicitar informações do atleta
    print("Digite Q em qualquer uma das questões para sair")

    nome_atleta = input("\033[2J\033[HQual o nome do atleta? ")
    if nome_atleta.upper() == 'Q': return

    cpf_atleta = input("Qual o CPF do atleta no formato XXX.XXX.XXX-XX? ")
    if cpf_atleta.upper() == 'Q': return

    data_nascimento = input("Qual a data de nascimento do atleta no formato YYYY-MM-DD? ")
    if data_nascimento.upper() == 'Q': return

    clube_ou_equipe = input("A qual clube ou equipe o atleta pertence? ")
    if clube_ou_equipe.upper() == 'Q': return

    mentor = input("Qual o CPF do mentor do atleta no formato XXX.XXX.XXX-XX? ")
    if mentor.upper() == 'Q': return

    escolaridade = input("Qual a escolaridade do atleta? ")
    if escolaridade.upper() == 'Q': return

    num_telefone = input("Qual o número de telefone do atleta no formato (XX)XXXXX-XXXX? ")
    if num_telefone.upper() == 'Q': return

    pais = input("Qual o país do atleta? ")
    if pais.upper() == 'Q': return

    estado = input("Qual o estado do atleta no formato XX? ")
    if estado.upper() == 'Q': return

    cidade = input("Qual a cidade do atleta? ")
    if cidade.upper() == 'Q': return

    logradouro = input("Qual o endereço do atleta? ")
    if logradouro.upper() == 'Q': return

    numero = input("Qual o número da residência do atleta? ")
    if numero.upper() == 'Q': return
    
    complemento = input("Algum complemento ao endereço? ")
    if complemento.upper() == 'Q': return
    elif complemento == '': complemento = 'N'

    try:
        n_alergias = int(input("Quantas alergias o atleta tem? "))
        alergias = []
        for enesima_alergia in range(n_alergias):
            alergia = input(f"Qual a {enesima_alergia + 1}ª alergia do atleta? ")
            alergias.append(alergia)

        print("As alergias registradas foram:", alergias)

    except ValueError:
        print("Por favor, insira um número válido para a quantidade de alergias.")
    
    try:
        n_doencas = int(input("Quantas doenças o atleta tem? "))
        doencas = []
        for enesima_doenca in range(n_doencas):
            doenca = input(f"Qual a {enesima_doenca + 1}ª doença do atleta? ")
            doencas.append(doenca)
        print("As doenças registradas foram:", doencas)

    except ValueError:
        print("Por favor, insira um número válido para a quantidade de doenças.")
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
            
            # Por fim, adicionar alergias e doenças
            sql_alergias = """
                INSERT INTO ALERGIAS_ATLETA (ATLETA,ALERGIA)
                VALUES (:1,:2)
            """
            for alergia in alergias:
                cursor.execute(sql_alergias,[cpf_atleta,alergia])

            sql_doencas = """
                INSERT INTO DOENCAS_ATLETA (ATLETA,DOENCA)
                VALUES (:1,:2)
            """

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


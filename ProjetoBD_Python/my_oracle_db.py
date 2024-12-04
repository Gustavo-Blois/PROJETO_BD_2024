import getpass
import oracledb

def login():
    un = 'adgmr'
    cs = 'orclgrad1.icmc.usp.br/pdb_elaine.icmc.usp.br'
    pw = getpass.getpass(f'Enter password for {un}@{cs}: ')
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        return connection
def menu_atletas(connection):
    tecla_do_usuario = ''  
    while(True): 
        tecla_do_usuario = input("""
            \033[2J
            \033[H 
            MENU ATLETAS
            Pressione 'q' para sair
            Pressione 'r' para verificar recordes de um dado atleta 
            pressione 'o' para verificar objetivos de desenvolvimento de um atleta
            """)
        match tecla_do_usuario:
            case 'r':
                recordes_atletas(connection)
            case 'o':
                objetivos_atletas(connection)
            case 'q':
                break
            case _:
                pass

def recordes_atletas(connection):
    with connection.cursor() as cursor:
        sql = """select 'drop table '||table_name||' cascade constraints;' from user_tables""" #TODO :  COLOCAR QUERY ADEQUADA
        for r in cursor.execute(sql):
            print(r)
        cursor.close()

def objetivos_atletas(connection):
    sql = """select 'drop table '||table_name||' cascade constraints;' from user_tables""" # TODO: COLOCAR QUERY ADEQUADA
    with connection.cursor() as cursor:
        for r in cursor.execute(sql):
            print(r)
            while(input("Pressione Enter para continuar") != 'c'):
                pass
        cursor.close

def menu_mentores(connection):
    tecla_do_usuario = ''  
    while(True): 
        tecla_do_usuario = input("""
            \033[2J
            \033[H 
            MENU ATLETAS
            Pressione 'q' para sair
            Pressione 'a' para verificar os atletas mentorados por um dado mentor 
            """)
        match tecla_do_usuario:
            case 'a':
                recordes_atletas(connection)
            case 'q':
                break
            case _:
                pass

def atletas_mentorados(connection):
    sql = """select 'drop table '||table_name||' cascade constraints;' from user_tables""" #TODO: COLOCAR QUERY ADEQUADA
    with connection.cursor() as cursor:
        for r in cursor.execute(sql):
            print(r)
        cursor.close()
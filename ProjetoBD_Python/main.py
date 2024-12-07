import my_oracle_db

def main():

    connection = my_oracle_db.login() #Consulte my_oracle_db.py para mais detalhes sobre o login
    
    print(connection)
    tecla_do_usuario = ''
    if connection:
        while(connection): 
            tecla_do_usuario = input("""
                \033[2J
                \033[H 
                BANCO DE DADOS
                APOIO AO ATLETISMO
                Pressione Q para sair
                Pressione A para adicionar um atleta à base de dados 
                pressione O para verificar objetivos de desenvolvimento de um atleta
                Pressione M para verificar os atletas mentorados por um mentor
                Pressione V para verificar atletas com as mesmas alergias que o Gabriel Barbosa
                """)
            match tecla_do_usuario.upper():
                case 'M':
                    my_oracle_db.atletas_mentorados(connection)
                case 'A':
                    my_oracle_db.adicionar_atleta(connection)
                case 'O':
                    my_oracle_db.objetivos_atleta(connection)
                case 'V':
                    my_oracle_db.alergias_gabriel_barbosa(connection)
                case 'Q':
                    break
                case _:
                    pass
        connection.cursor().close()
        connection.close()

        print("\033[2J\033[H") #Apaga a tela e retorna ao terminal
    else:
        print("Não foi possível se conectar à base de dados")
    

if __name__ == '__main__':
    main()
    



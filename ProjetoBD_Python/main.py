import my_oracle_db

def main():

    connection = my_oracle_db.login() # Consulte my_oracle_db.py para mais detalhes sobre o login
    
    print(connection)
    tecla_do_usuario = ''
    if connection.is_healthy():
        while(True): 
            tecla_do_usuaryio = input("""
                \033[2J
                \033[H 
                BD ATLETAS
                Pressione 'q' para sair
                Pressione 'a' para entrar na área de atletas
                pressione 'm' para entrar na área de mentores
                """)
            match tecla_do_usuario:
                case 'a':
                    my_oracle_db.menu_atletas(connection)
                case 'm':
                    my_oracle_db.menu_mentores(connection)
                case 'q':
                    break
                case _:
                    pass

        print("\033[2J\033[H") #Apaga a tela e retorna ao terminal
    else:
        print("Não foi possível se conectar à base de dados")

if __name__ == '__main__':
    main()
    



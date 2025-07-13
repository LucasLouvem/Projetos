import sqlite3
from datetime import datetime

# Nome do arquivo do banco de dados
DB_NAME = 'escola_jiujitsu.db'

def conectar_db():
    """Conecta ao banco de dados e retorna a conexão e o cursor."""
    conn = sqlite3.connect(DB_NAME)
    # Garante que as chaves estrangeiras sejam respeitadas
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    """Cria as tabelas 'alunos', 'pagamentos' e 'presencas' se não existirem."""
    conn, cursor = conectar_db()
    try:
        # Tabela ALUNOS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento TEXT, -- YYYY-MM-DD
                endereco TEXT,
                data_matricula TEXT NOT NULL, -- YYYY-MM-DD
                grau_atual TEXT DEFAULT 'Branca',
                celular_contato TEXT,
                email TEXT UNIQUE,
                nome_responsavel TEXT,
                celular_responsavel TEXT
            )
        ''')

        # Tabela PAGAMENTOS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                data_pagamento TEXT NOT NULL, -- YYYY-MM-DD
                valor_pago REAL NOT NULL,
                mes_referencia TEXT NOT NULL, -- YYYY-MM (ex: 2025-07)
                status TEXT NOT NULL DEFAULT 'Pago', -- 'Pago', 'Pendente', 'Atrasado'
                FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
            )
        ''')

        # Tabela PRESENCAS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presencas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                data_aula TEXT NOT NULL, -- YYYY-MM-DD
                horario_aula TEXT, -- HH:MM (opcional)
                FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        print("Tabelas verificadas/criadas com sucesso no banco de dados.")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()

# --- Funções para Manipulação de Dados ---

def inserir_aluno(nome, data_nascimento, endereco, data_matricula,
                  grau_atual='Branca', celular_contato=None, email=None,
                  nome_responsavel=None, celular_responsavel=None):
    """Insere um novo aluno no banco de dados."""
    conn, cursor = conectar_db()
    try:
        cursor.execute("""
            INSERT INTO alunos (nome, data_nascimento, endereco, data_matricula,
                                grau_atual, celular_contato, email,
                                nome_responsavel, celular_responsavel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, data_nascimento, endereco, data_matricula,
              grau_atual, celular_contato, email,
              nome_responsavel, celular_responsavel))
        conn.commit()
        print(f"Aluno '{nome}' inserido com sucesso! ID: {cursor.lastrowid}")
        return cursor.lastrowid # Retorna o ID do aluno inserido
    except sqlite3.IntegrityError:
        print(f"Erro: E-mail '{email}' já cadastrado para outro aluno.")
        return None
    except sqlite3.Error as e:
        print(f"Erro ao inserir aluno: {e}")
        return None
    finally:
        conn.close()

def inserir_pagamento(aluno_id, data_pagamento, valor_pago, mes_referencia, status='Pago'):
    """Registra um novo pagamento para um aluno."""
    conn, cursor = conectar_db()
    try:
        cursor.execute("""
            INSERT INTO pagamentos (aluno_id, data_pagamento, valor_pago, mes_referencia, status)
            VALUES (?, ?, ?, ?, ?)
        """, (aluno_id, data_pagamento, valor_pago, mes_referencia, status))
        conn.commit()
        print(f"Pagamento de R${valor_pago:.2f} para o aluno ID {aluno_id} (ref. {mes_referencia}) registrado com sucesso!")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir pagamento: {e}")
        return None
    finally:
        conn.close()

def inserir_presenca(aluno_id, data_aula, horario_aula=None):
    """Registra a presença de um aluno em uma aula."""
    conn, cursor = conectar_db()
    try:
        cursor.execute("""
            INSERT INTO presencas (aluno_id, data_aula, horario_aula)
            VALUES (?, ?, ?)
        """, (aluno_id, data_aula, horario_aula))
        conn.commit()
        print(f"Presença do aluno ID {aluno_id} registrada para a aula de {data_aula}.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir presença: {e}")
        return None
    finally:
        conn.close()

def buscar_alunos(termo_busca=""):
    """Busca alunos por nome, CPF ou e-mail. Se vazio, retorna todos."""
    conn, cursor = conectar_db()
    alunos_encontrados = []
    try:
        if termo_busca:
            # Usamos LIKE para busca parcial e OR para buscar em múltiplos campos
            cursor.execute("""
                SELECT id, nome, data_nascimento, endereco, data_matricula,
                       grau_atual, celular_contato, email,
                       nome_responsavel, celular_responsavel
                FROM alunos
                WHERE nome LIKE ? OR email LIKE ? OR celular_contato LIKE ?
            """, ('%' + termo_busca + '%', '%' + termo_busca + '%', '%' + termo_busca + '%'))
        else:
            cursor.execute("""
                SELECT id, nome, data_nascimento, endereco, data_matricula,
                       grau_atual, celular_contato, email,
                       nome_responsavel, celular_responsavel
                FROM alunos
            """)
        alunos_encontrados = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar alunos: {e}")
    finally:
        conn.close()
    return alunos_encontrados

def buscar_pagamentos_aluno(aluno_id):
    """Busca todos os pagamentos de um aluno específico."""
    conn, cursor = conectar_db()
    pagamentos = []
    try:
        cursor.execute("""
            SELECT id, data_pagamento, valor_pago, mes_referencia, status
            FROM pagamentos
            WHERE aluno_id = ?
            ORDER BY data_pagamento DESC
        """, (aluno_id,))
        pagamentos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar pagamentos: {e}")
    finally:
        conn.close()
    return pagamentos

def buscar_presencas_aluno(aluno_id):
    """Busca todas as presenças de um aluno específico."""
    conn, cursor = conectar_db()
    presencas = []
    try:
        cursor.execute("""
            SELECT id, data_aula, horario_aula
            FROM presencas
            WHERE aluno_id = ?
            ORDER BY data_aula DESC
        """, (aluno_id,))
        presencas = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar presenças: {e}")
    finally:
        conn.close()
    return presencas

def contar_presencas_aluno(aluno_id):
    """Conta o total de presenças de um aluno."""
    conn, cursor = conectar_db()
    total_presencas = 0
    try:
        cursor.execute("SELECT COUNT(*) FROM presencas WHERE aluno_id = ?", (aluno_id,))
        total_presencas = cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Erro ao contar presenças: {e}")
    finally:
        conn.close()
    return total_presencas

# --- Bloco de Teste (para você rodar e ver funcionando no terminal) ---
if __name__ == "__main__":
    criar_tabelas()

    print("\n--- Testando Inserção de Alunos ---")
    # Aluno maior de idade
    id_lucas = inserir_aluno(
        nome="Lucas Mendes",
        data_nascimento="2002-07-15", # Seu aniversário, Lucas!
        endereco="Rua das Flores, 123 - Centro",
        data_matricula=datetime.now().strftime("%Y-%m-%d"),
        celular_contato="21987654321",
        email="lucas.mendes@email.com"
    )

    # Aluno menor de idade (exemplo)
    id_ana = inserir_aluno(
        nome="Ana Clara",
        data_nascimento="2015-01-20",
        endereco="Av. Principal, 456 - Bairro Novo",
        data_matricula=datetime.now().strftime("%Y-%m-%d"),
        celular_contato="21998765432",
        email="ana.clara@email.com",
        nome_responsavel="Carlos Silva",
        celular_responsavel="21912345678"
    )

    # Tentativa de inserir aluno com email duplicado
    inserir_aluno(
        nome="Lucas Duplicado",
        data_nascimento="2000-01-01",
        endereco="Rua Teste, 1",
        data_matricula=datetime.now().strftime("%Y-%m-%d"),
        email="lucas.mendes@email.com"
    )

    print("\n--- Testando Busca de Alunos ---")
    print("Todos os alunos:")
    for aluno in buscar_alunos():
        print(aluno)

    print("\nBuscando 'Lucas':")
    for aluno in buscar_alunos("Lucas"):
        print(aluno)

    print("\n--- Testando Inserção de Pagamentos ---")
    if id_lucas:
        inserir_pagamento(id_lucas, datetime.now().strftime("%Y-%m-%d"), 150.00, "2025-07")
        inserir_pagamento(id_lucas, "2025-06-20", 150.00, "2025-06")
    if id_ana:
        inserir_pagamento(id_ana, datetime.now().strftime("%Y-%m-%d"), 150.00, "2025-07")
        inserir_pagamento(id_ana, "2025-06-25", 150.00, "2025-06", status='Atrasado') # Exemplo de atrasado

    print("\n--- Testando Busca de Pagamentos do Lucas ---")
    if id_lucas:
        for pgto in buscar_pagamentos_aluno(id_lucas):
            print(pgto)

    print("\n--- Testando Inserção de Presenças ---")
    if id_lucas:
        inserir_presenca(id_lucas, datetime.now().strftime("%Y-%m-%d"), "19:00")
        inserir_presenca(id_lucas, "2025-07-01", "19:00")
        inserir_presenca(id_lucas, "2025-06-28", "19:00")
        inserir_presenca(id_lucas, "2025-06-27", "19:00")
        inserir_presenca(id_lucas, "2025-06-26", "19:00")
        # Adicionando mais presenças para testar a lógica de grau (se tiver 30 aulas)
        for i in range(25): # Adiciona mais 25 presenças
            inserir_presenca(id_lucas, f"2025-06-{i+1:02d}", "19:00") # Datas fictícias
    if id_ana:
        inserir_presenca(id_ana, datetime.now().strftime("%Y-%m-%d"), "18:00")

    print("\n--- Testando Busca de Presenças do Lucas ---")
    if id_lucas:
        for pres in buscar_presencas_aluno(id_lucas):
            print(pres)

    print(f"\nTotal de presenças do Lucas: {contar_presencas_aluno(id_lucas)}")
    print(f"Total de presenças da Ana: {contar_presencas_aluno(id_ana)}")

    # Exemplo de como você usaria a contagem de presenças para a lógica do grau
    if id_lucas:
        total_aulas_lucas = contar_presencas_aluno(id_lucas)
        if total_aulas_lucas >= 30:
            print(f"Lucas tem {total_aulas_lucas} aulas. Ele pode estar pronto para subir de grau!")
            # Aqui você chamaria uma função para atualizar o grau do aluno
        else:
            print(f"Lucas tem {total_aulas_lucas} aulas. Ele ainda não atingiu 30 aulas para subir de grau.")
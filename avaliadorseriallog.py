import os
import time
import multiprocessing


# ===============================
# Consolidação dos resultados
# ===============================

def consolidar_resultados(resultados):
    total_linhas = 0
    total_palavras = 0
    total_caracteres = 0

    contagem_global = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for r in resultados:
        total_linhas += r["linhas"]
        total_palavras += r["palavras"]
        total_caracteres += r["caracteres"]

        for chave in contagem_global:
            contagem_global[chave] += r["contagem"][chave]

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem_global
    }


# ===============================
# Processamento de arquivo
# ===============================

def processar_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.readlines()

    total_linhas = len(conteudo)
    total_palavras = 0
    total_caracteres = 0

    contagem = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for linha in conteudo:
        palavras = linha.split()

        total_palavras += len(palavras)
        total_caracteres += len(linha)

        for p in palavras:
            if p in contagem:
                contagem[p] += 1

        # Simulação de processamento pesado
        for _ in range(1000):
            pass

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem
    }


# ===============================
# EXECUÇÃO SERIAL
# ===============================

def executar_serial(pasta):
    resultados = []

    inicio = time.time()

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            caminho = os.path.join(pasta, arquivo)
            resultados.append(processar_arquivo(caminho))

    fim = time.time()

    resumo = consolidar_resultados(resultados)

    print("\n=== EXECUÇÃO SERIAL ===")
    print(f"Tempo total: {fim - inicio:.4f} segundos")

    return fim - inicio, resumo


# ===============================
# EXECUÇÃO PARALELA (POOL)
# ===============================

def executar_paralelo(pasta, n_processos):

    arquivos = [
        os.path.join(pasta, f)
        for f in os.listdir(pasta)
        if f.endswith(".txt")
    ]

    inicio = time.time()

    with multiprocessing.Pool(processes=n_processos) as pool:
        resultados = pool.map(processar_arquivo, arquivos)

    fim = time.time()

    resumo = consolidar_resultados(resultados)

    print(f"\n=== PARALELO ({n_processos} processos) ===")
    print(f"Tempo total: {fim - inicio:.4f} segundos")

    return fim - inicio, resumo


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":

    pasta = "log2"

    tempos = {}

    # SERIAL
    t1, resumo = executar_serial(pasta)
    tempos[1] = t1

    print("\n=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {resumo['linhas']}")
    print(f"Total de palavras: {resumo['palavras']}")
    print(f"Total de caracteres: {resumo['caracteres']}")

    print("\nContagem de palavras-chave:")
    for k, v in resumo["contagem"].items():
        print(f"{k}: {v}")

    # PARALELO
    for p in [2, 4, 8, 12]:
        tp, _ = executar_paralelo(pasta, p)
        tempos[p] = tp

    # TABELA FINAL
    print("\n=== TABELA FINAL ===")
    print("Proc | Tempo | Speedup | Eficiência")

    for p in [1, 2, 4, 8, 12]:
        tempo = tempos[p]
        speedup = tempos[1] / tempo
        eficiencia = speedup / p

        print(f"{p:4} | {tempo:.4f} | {speedup:.2f} | {eficiencia:.2f}")
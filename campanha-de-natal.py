import pandas as pd
import chardet
import os


class Setup:
    """
        Esse objeto é responsável por armazenar os parâmetros do processamento por se tratar 
        de um projeto simples, mas em casos mais complexos, é possível obter esses parâmetros 
        a partir de um banco de dados ou API, por exemplo.
    """
    input_file_name = './data/natal2021.csv'
    output_file_name = './data/natal2021_processed.csv'
    chunk_size = 1000


def get_enconding(file_path: str):
    """Retorna o encoding do arquivo."""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())

    return result['encoding']


def remove_file_if_exists(file_path: str):
    """Remove o arquivo se ele existir."""
    if os.path.exists(file_path):
        os.remove(file_path)


def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Processa um chunk do arquivo indivudualmente."""
    chunk = chunk.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    chunk['CITY_ASCII'] = (chunk['CITY']
                           .str.normalize('NFKD')
                           .str.encode('ascii', errors='ignore')
                           .str.decode('utf-8')
                           .str.upper()
                           .str.replace(r'[^A-Z0-9-\s]+', '', regex=True))
    # obs: Nos requisitos não pede para manter espaços no campo CITY_ASCII, porém no
    # exemplo prático os espaços se mantém após a formatação, então optei por manter espaços.

    chunk['PHONE'] = chunk['PHONE'].str.replace(r'[^0-9]+', '', regex=True)

    return chunk


def process_christmas_data(input_path: str, output_path: str, chunk_size: int) -> None:
    """Processa o arquivo de dados de Natal."""

    encoding = get_enconding(input_path)
    print(f'O arquivo de entrada possui enconding: {encoding}')
    
    remove_file_if_exists(output_path)

    if not os.path.exists(input_path):
        print('Arquivo de entrada não foi encontrado, finalizando processo.')
        return

    print(f'Processando arquivo "{input_path}" a cada {chunk_size} instâncias...')
    # Lendo o arquivo CSV em pedaços(chunks) de 1000 linhas
    with pd.read_csv(input_path, sep=',', encoding=encoding, chunksize=chunk_size) as chunks:
        
        for chunk in chunks:
            processed_chunk = process_chunk(chunk)
            # A cada iteração é salvo o diferencial no arquivo de saída para evitar memoryleak
            processed_chunk.to_csv(output_path, mode='a', index=False, header=not os.path.exists(output_path))
        
    print(f'Processo finalizado, resultado está disponível no arquivo "{output_path}"!')


if __name__ == '__main__':
    try:
        process_christmas_data(
            Setup.input_file_name,
            Setup.output_file_name,
            Setup.chunk_size
        )
    except Exception as exception:
        print(f'O processamento não pode ser concluído devido a um erro: {exception}')

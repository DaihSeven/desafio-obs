from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

app = Flask(__name__)

# Métrica para contar erros
error_count = Counter('app_errors_total', 'Total number of errors')

# Métrica para medir o tempo de execução de uma função
function_duration = Histogram('app_function_duration_seconds', 'Time spent in function execution', ['function_name'])

# Rota para página inicial com mensagem de boas-vindas
@app.route('/')
def welcome():
    return '2° aplicação testando com sucesso'

# Rota para gerar erros intencionalmente
@app.route('/generate-error')
def generate_error():
    try:
        # Simulando uma exceção
        1 / 0
    except Exception as e:
        # Incrementando a métrica de erros
        error_count.inc()
        return f"Erro gerado: {str(e)}", 500

# Rota para medir o tempo de execução
@app.route('/calculate-duration')
def calculate_duration():
    start_time = time.time()
    # Simulando uma operação demorada
    time.sleep(2)
    function_duration.labels(function_name='calculate_duration').observe(time.time() - start_time)
    return "Tempo de execução medido com sucesso"

# Rota para expor métricas do Prometheus com quebras de linha
@app.route('/metrics')
def metrics():
    metrics_data = generate_latest(REGISTRY)
    return Response(metrics_data, content_type='text/plain; version=0.0.4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
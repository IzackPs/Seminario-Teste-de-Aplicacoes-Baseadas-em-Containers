# 📦 Seminário: Teste de Aplicações Baseadas em Contêineres

Repositório destinado ao seminário de Engenharia de Software II, focado em demonstrar na prática os desafios, testes e as melhores práticas (DevSecOps e Engenharia de Caos) em aplicações executadas em ambientes conteinerizados.

## 🛠️ Stack Tecnológica
* **Linguagem & Framework:** Python 3.14.4 | Flask 3.1.3
* **Servidor de Produção (WSGI):** Gunicorn 25.3.0
* **Orquestração & Infraestrutura:** K3s (Kubernetes leve)
* **Testes de Carga e Estresse:** Grafana k6
* **Observabilidade:** Grafana (Dashboard 15757)
* **Segurança (Container Scanning):** Aqua Security Trivy

---

## 🚀 Arquitetura e Limites (Kubernetes)
O ambiente foi rigorosamente configurado para espelhar um cenário de produção escalável e previsível:

* **HPA (Horizontal Pod Autoscaler):** Escalonamento horizontal dinâmico de 1 a 20 réplicas, acionado ao atingir 70% de utilização de CPU.
* **Resource Quotas:** Limites estritos para garantir estabilidade do cluster e forçar o escalonamento durante os testes:
  * **CPU:** Requests de `30m` | Limits de `60m`
  * **Memória:** Limites omitidos intencionalmente para suportar o buffer TCP da alta carga do K6, focando o gargalo estritamente na CPU.
* **Probes de Saúde:**
  * **Readiness:** Verifica a rota `/health` a cada 2s (tolerância de 3 falhas). Impede que tráfego seja enviado a Pods que ainda estão inicializando.
  * **Liveness:** Verifica a rota `/health` a cada 5s (tolerância de 5 falhas). Responsável por reiniciar Pods travados ou mortos.

---

## 🌪️ Engenharia de Caos e Resiliência (Self-Healing)
Para provar a eficácia dos testes de infraestrutura, a API possui uma rota de injeção de falhas (`/crash`). 
Ao ser acionada, ela cria um arquivo temporário no sistema (`/tmp/api_crashed.flag`), sinalizando para todos os *workers* do Gunicorn que a aplicação entrou em estado crítico e deve retornar Erro 500 na rota `/health`. 

**Resultado esperado e validado:** O Kubernetes detecta a falha via Liveness Probe, destrói o contêiner corrompido e provisiona um novo contêiner limpo (*Self-healing*) em menos de 30 segundos, restaurando a disponibilidade do sistema sem intervenção humana.

---

## 🚦 Testes de Carga (Grafana k6)
O script de estresse (`stress.js`) foi construído para validar o comportamento do contêiner sob alta demanda:
* **Ramp-up e Ramp-down:** Escalonamento progressivo (até 600 VUs em 1 minuto) para evitar esgotamento abrupto de portas TCP.
* **Validações (Checks):** Validação ativa das respostas HTTP para garantir que a aplicação não apenas suporte a conexão, mas retorne o status `200 OK` esperado.
* **Parametrização:** Execução agnóstica de ambiente utilizando variáveis de ambiente (`BASE_URL`).

---

## 🔒 Segurança e Boas Práticas (DevSecOps)
A construção da imagem Docker adota o conceito de **Shift-Left Security** e as melhores práticas da indústria:

* **Multistage Build:** Separação estrita entre o ambiente de compilação (*Builder*) e o ambiente de execução (*Runtime*). Isso reduz drasticamente o tamanho da imagem final e elimina ferramentas de compilação da superfície de ataque.
* **Princípio do Menor Privilégio (Non-root):** Execução do processo principal atrelada a um usuário restrito (`apiapp`), abandonando o acesso `root` padrão.
* **Imagem Base Otimizada:** Utilização da versão `slim` do Debian 13.4.
* **Dependências Determinísticas:** Travamento estrito das versões de bibliotecas no `requirements.txt`.
* **Auditoria de Vulnerabilidades:** Varredura de CVEs (Common Vulnerabilities and Exposures) garantida pelo uso contínuo do **Trivy** na imagem final.
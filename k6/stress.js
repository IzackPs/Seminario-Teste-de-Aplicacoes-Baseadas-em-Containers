import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  // Escalonamento para evitar esgotamento TCP
  stages: [
    { duration: '25s', target: 200 }, // Sobe para 200 usuários em 25s
    { duration: '1m', target: 600 },  // Fica com 600 usuários por 1 minuto
    { duration: '30s', target: 0 },   // Desce para 0 gradualmente
  ],
};

// BOAS PRÁTICAS: Permite passar a URL via variável de ambiente. 
// Se não passar nada, ele usa o IP padrão do seu K3s.
const BASE_URL = __ENV.BASE_URL || 'http://192.168.10.10:30080';

export default function () {
  const params = {
    headers: { 'Connection': 'keep-alive' },
    timeout: '10s', // Dá mais tempo para o servidor responder sob carga
  };
  
  // Guardamos a resposta da requisição na variável 'res'
  const res = http.get(BASE_URL, params); 
  
  // VALIDAÇÃO (O "Teste" de fato)
  // O K6 vai gerar um relatório visual mostrando quantos % das requisições deram certo.
  check(res, {
    'status é 200 (OK)': (r) => r.status === 200,
  });
  
  // AUMENTAMOS O SLEEP SIGNIFICATIVAMENTE
  // Isso impede que o k6 tente abrir milhares de portas por segundo e derrube a rede antes da CPU
  sleep(1); 
}
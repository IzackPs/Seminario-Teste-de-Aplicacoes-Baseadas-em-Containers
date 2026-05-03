import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  // Vamos subir os usuarios aos poucos para nao assustar o TCP
  stages: [
    { duration: '25s', target: 200 }, // Sobe para 200 usuarios em 25s
    { duration: '1m', target: 600 }, // Fica com 600 usuarios por 1 minuto
    { duration: '30s', target: 0 },   // Desce para 0 gradualmente
  ],
};

export default function () {
  const params = {
    headers: { 'Connection': 'keep-alive' },
    timeout: '10s', // Da mais tempo para o servidor responder sob carga
  };
  
  // Verifique se este IP e o do seu Debian/K3s
  http.get('http://192.168.10.10:30080', params); 
  
  // AUMENTAMOS O SLEEP SIGNIFICATIVAMENTE
  // Isso impede que o k6 tente abrir milhares de portas por segundo e derrube a rede antes da CPU
  sleep(1); 
}

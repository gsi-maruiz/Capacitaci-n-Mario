import http from 'k6/http';
import { check, sleep } from 'k6';

const url = 'http://127.0.0.1:8000/graphql';
export let options = {  
  stages: [
    { duration: '10s', target: 40 },
    { duration: '20s', target: 40 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<100'], // 95% of requests must complete below 100 miliseconds    
  },  
};

export default function () {
  const body = JSON.stringify({ query: 'query{allIngredients{name}}' });
  const param={
    headers:{
      'Content-Type': 'application/json'
    }
  }

  const res=http.post(url,body,param);
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1)
}

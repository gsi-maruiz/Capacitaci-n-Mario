import http from 'k6/http';
import { check, sleep } from 'k6';

const url = 'https://gapiqa.generalsoftwareinc.net/api/client';
export let options = {
    stages: [
        { duration: '10s', target: 40 },
        { duration: '20s', target: 40 },
        { duration: '10s', target: 0 },
      ],
      thresholds: {
        http_req_duration: ['p(95)<200'], // 95% of requests must complete below 200 miliseconds    
      },
};

export default function () {
  const body = JSON.stringify({ query: 'query{UserMeGet{data{username}}}' });
  const param={      
       headers:{ 
           'Content-Type': 'application/json' ,
           'authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhYnkiLCJleHAiOjI2OTY3NzIzMTgsIm9yaWdJYXQiOjE2MTY3NzIzMTh9.pJIImYNXzlzhgPUe0cUCqLAD2e7NEJn-AHI09EtWPzg'
     }
  }

  const res=http.post(url,body,param);
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1)
}

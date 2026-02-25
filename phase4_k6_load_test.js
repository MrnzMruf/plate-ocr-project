// phase4_k6_load_test.js
// Phase 4: Heavy load test with k6
// 700 concurrent virtual users, 5 minutes duration
// Goal: ~69 RPS, <1% failure, 0% data loss

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 100 },     // ramp-up
    { duration: '4m',  target: 700 },     // peak load
    { duration: '30s', target: 0 },       // ramp-down
  ],
  thresholds: {
    'http_req_failed':   ['rate<0.01'],     // <1% failed requests
    'http_req_duration': ['p(95)<2000'],    // 95% requests < 2s
  },
};

export default function () {
  const payload = JSON.stringify({
    // Simulate image upload request (multipart would be more accurate but complex in k6)
    filename: `test-${__VU}-${Date.now()}.jpg`
  });

  const res = http.post('http://localhost:8000/upload/', payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'queued successfully': (r) => r.json('status') === 'queued',
    'has task_id': (r) => !!r.json('task_id'),
  });

  sleep(1);  // simulate user think time
}

/**
 * 라이선스 미명시 패키지 리스크 시연용 샘플 앱.
 *
 * 이 파일은 express(MIT), lodash(MIT), nightmare(라이선스 불명확)를
 * 사용하는 최소한의 Hello World 예제입니다.
 */

const express = require('express');
const _ = require('lodash');

const app = express();
const PORT = 3000;

// lodash를 사용한 간단한 유틸리티 (MIT 라이선스)
const greetings = ['Hello', 'World', 'OpenChain', 'SBOM'];
const shuffled = _.shuffle(greetings);

app.get('/', (req, res) => {
  res.json({
    message: 'Hello, World!',
    greeting: shuffled[0],
    warning: '이 앱은 라이선스가 불명확한 패키지를 포함합니다.',
    packages: {
      express: 'MIT - 명확',
      lodash: 'MIT - 명확',
      nightmare: 'UNLICENSED - 상업적 사용 위험'
    }
  });
});

app.listen(PORT, () => {
  console.log(`서버 시작: http://localhost:${PORT}`);
  console.log('경고: nightmare 패키지의 라이선스가 불명확합니다.');
  console.log('라이선스 미명시 = 기본적으로 All Rights Reserved (사용 권한 없음)');
});

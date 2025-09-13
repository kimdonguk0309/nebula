#####################################################
환경 설정
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -e .
#####################################################
nebula/
├── nebula/
│   ├── __init__.py
│   ├── protocol.py          # nb:// 프로토콜 구현
│   ├── markup.py            # NebulaML 파서
│   ├── dht.py               # Kademlia 기반 DHT
│   ├── browser.py           # Tkinter GUI 브라우저
│   └── node.py              # full-node 실행기
├── apps/
│   └── welcome.neb          # 샘플 페이지
├── README.md
├── pyproject.toml           # pip install -e .  지원
└── run.py                   # python run.py  한 방에 실행

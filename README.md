# 전기차 충전소 찾기 앱
https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15100485  


## 피드백
정보?가 풍부하지 못하다  
뭔가 더 추가해봐라  
충전소 위치로 가는 길을 알려주는 기능 등..  
map에 있다고..  

## 일정
|주차|계획|내용|진행도|
|---|---|---|---|
|1주차| GUI 배치, API호출 | 버튼, 지도, 그래프 등 대략적인 배치 | [100%] |
|2주차| 그래프, 즐겨찾기, 검색기록 | 받아온 데이터 그래프로 출력, 즐겨찾기 및 검색기록 파일로 저장, 읽어오기 | [50%] 즐겨찾기, 검색기록 완료 |
|3주차| 지도, 상세정보 | 지도 구현, 지도에 충전소 위치 표시, 충전소 선택해서 상세정보 표시 | [100%] |
|4주차| 이메일, 충전기 정보 표시 | 이메일 전송, tkinter노트북 기능으로 충전기 정보 표시 | | 
|5주차| 길찾기 | 선택한 충전소까지의 경로 출력 | 



## 추가
- 길 알려주기: https://developers.google.com/maps/documentation/javascript/directions?hl=ko  
- https://console.cloud.google.com/apis/library/browse?filter=category:maps&project=scriptlangtermproject&supportedpurview=project



## 변경할거
모든 충전소 위치를 미리 로드하도록? -> 너무 오래걸릴듯  
같은 장소에 있는 충전소는 한개만 표시, 클릭시 상세정보에는 전부 표시  
선택한 충전기는 마커색 다르게 표시  
이미지 범위 밖의 마커는 링크를 넘기지 않음 -> 이거 어케함??  
가까운 마커는 하나만 표시  
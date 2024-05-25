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
|1주차| GUI 배치, API호출 | 버튼, 지도, 그래프 등 대략적인 배치 | [80%] GUI 배치중, API호출 성공 |
|2주차| 그래프, 즐겨찾기, 검색기록 | 받아온 데이터 그래프로 출력, 즐겨찾기 및 검색기록 파일로 저장, 읽어오기 | [50%] 즐겨찾기, 검색기록 완료 |
|3주차| 지도, 상세정보 | 지도 구현, 지도에 충전소 위치 표시, 지도를 클릭해 충전소 선택, 상세정보 표시 | [30%] 지도 불러오기 |
|4주차| 이메일, 충전기 정보 표시 | 이메일 전송, tkinter노트북 기능으로 충전기 정보 표시 | | 
|5주차| 마무리 | 필요시 새로운 기능 추가 | 



## 추가
- 길 알려주기: https://developers.google.com/maps/documentation/javascript/directions?hl=ko  
- https://console.cloud.google.com/apis/library/browse?filter=category:maps&project=scriptlangtermproject&supportedpurview=project




## 변경할거
콤보박스로 지역 선택하도록?  
모든 충전소 위치를 미리 로드하도록?  
같은 장소에 있는 충전소는 한개만 표시, 클릭시 상세정보에는 전부 표시  

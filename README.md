# 전기차 충전소 찾기 앱

## Progress
- [x] 그래프
- [x] 즐겨찾기
- [x] 검색기록
- [x] 지도
- [x] 상세정보
- [x] 이메일
- [x] 충전기 정보 표시
- [x] 길찾기
- [ ] C/C++ 연동
- [ ] 텔레그램 봇



## 추가
구글 길찾기가 작동하지 않는 관계로 네이버 길찾기 사용  
네이버 Maps API  

## 변경할거
거리순 정렬  


## Map memo
900x900 기준  

zoom == 13일때 가로로 보이는 거리가 1이라고 하면,  
zoom == 14일때는 1/2,  
zoom == 15일때는 1/4,  
zoom == 16일때는 1/8, ...

zoom == 12일때는 2,  
zoom == 11일때는 4,  
zoom == 10일때는 8, ...

zoom == 13일때 대략 ±0.055가 한계.

```py
    limit = 0.055 * (2 ** (13 - zoom))
```

**작동검증**  
마커 많이 찍을때(9999개 로드) 기본상태에서는 지도 로드 안되던거 줌 당기면 로드됨(죽전 기준)  



## Marker Grouping
0. 보이는 지점의 마커만 가지고 수행
1. 아무 점 하나 잡기
2. 합칠 범위 설정(배율에 따라 다름)
3. 범위 안의 점들의 중심을 마커로 설정
4. 합쳐지지 않은 다른 점들로 다시 수행

```py
radius = (0.055 * (2 ** (13 - zoom))) / 2
```
일때  
![image](img/r_2.png)

```py
radius = (0.055 * (2 ** (13 - zoom))) / 10
```
일때  
![image](img/r_10.png)

```py
radius = (0.055 * (2 ** (13 - zoom))) / 20
```
일때
![image](img/r_20.png)


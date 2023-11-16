# final-pjt

## 1일차(2023-11-16)

### Back
  - 데이터베이스 모델링(ERD)
    - 우선 모든 서비스의 기본이 되는 User Model을 중심으로 User Model과 1:N 관계를 가지는 예금 모델, 적금 모델을 설정하였고, 예/적금 모델과 1:N 관계를 가지는 예/적금 옵션 모델을 추가적으로 설정하였습니다. 또한, 예/적금 상세 조회 페이지에서 해당 상품에 대한 리뷰 기능을 구현하기 위해 예/적금 모델 및 User Model과 1:N 관계를 가지는 Review 모델 또한 설정하였습니다.
    - 근처 은행 검색 기능을 구현하기 위해 Bank Model을 구현하였습니다.
    - 커뮤니티 기능을 구현하기 위해 Article, Comment Model을 추가적으로 구현하였습니다.
  
  - 회원 커스터마이징 기능 구현
    - 필수 요구사항 중 회원 커스터마이징 기능을 구현하였습니다.
    - 회원 관리 라이브러리인 allauth와 dj-rest-auth를 이용하여 기본 User Model을 상속받아 커스텀 User Model과 Serializer를 구성하였습니다.
    - 추가 field로 유저의 닉네임에 해당하는 nickname, 유저의 나이에 해당하는 age, 유저의 자산에 해당하는 asset, 유저의 연봉에 해당하는 salary, 유저가 가입한 상품 목록인 financial_products field를 생성하였습니다.
    - 또한, 회원 정보 확인 / 수정 / 탈퇴 기능을 나누어 구현하기 위해 url에 해당하는 view 함수의 method를 GET, PUT, DELETE로 나누었습니다.
    - method가 GET일 경우에는 유저의 모든 정보를 확인할 수 있도록 User model의 모든 Field를 확인할 수 있는 Serializer를 통해 해당 유저의 정보를 출력할 수 있도록 구현하였습니다.
    - method가 PUT일 경우에는 수정 가능한 정보만 수정할 수 있도록, 별도의 Serializer를 통해 수정할 수 있는 필드를 지정해준 다음, 모든 정보가 아닌 일부분의 정보만 수정해도 제출이 가능하도록 partial=True 인자를 추가하여 view 함수를 구현하였습니다.
    - method가 DELETE인 경우에는 회원 탈퇴가 가능하도록 delete() 함수를 이용하여 view 함수를 구현하였습니다.
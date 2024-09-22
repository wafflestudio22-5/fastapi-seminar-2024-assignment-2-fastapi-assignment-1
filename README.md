# FastAPI 세미나 과제 2

세미나 2에서는 SQLAlchemy 를 사용하여 데이터베이스를 다루는 방법을 배웠습니다.
이번 과제에서는 데이터베이스를 사용하여 과제 1에서 구현했던 API 를 고도화하고, 추가 API 를 구현해봅니다.

## 과제 목표

- ER 다이어그램을 활용하여 도메인에 적합한 데이터베이스 모델을 설계할 수 있다.
- FastAPI 에서 데이터베이스를 사용하여 영구적인 데이터를 저장하고 조회할 수 있다.

## 준비 사항

- 모든 과제는 python 3.11 버전을 사용할 것을 전제로 합니다.
- 본 과제의 가상환경의 생성은 poetry 를 사용합니다.
  - poetry 를 설치한 뒤, `poetry env use -- 3.11` 과 같은 명령어를 이용해 가상환경을 생성하세요.
  - `poetry install` 명령어를 통해 패키지를 설치하세요.
  - `pyproject.toml` 과 `poetry.lock` 파일은 수정하지 않습니다.

## 과제 2-1

ER 다이어그램을 사용하여 와팡의 데이터베이스 모델을 설계해봅니다.
설계에 필요한 정보는 다음과 같습니다.

- 유저는 username, email, password, phone_number 를 가지고 있습니다.
- 유저는 최대 하나의 상점만 소유할 수 있습니다.
- 상점은 store_name, address, email, phone_number 를 가지고 있습니다.
- 상점은 여러 개의 상품을 가질 수 있습니다.
- 상품은 item_name, price, stock 을 가지고 있습니다.
- 유저는 물건을 찜할 수 있습니다.
- 유저는 여러 개의 주문을 할 수 있습니다.
- 주문은 진행 상태에 따라 `canceled`, `ordered`, `delivered`, `returned`, `completed` 중 하나의 상태를 가집니다.
- 한 주문에는 여러 개의 상품이 포함될 수 있습니다.
- 유저는 상품마다 최대 한 개의 리뷰를 남길 수 있습니다.
- 리뷰는 별점과 내용을 가지고 있습니다.


## 과제 2-2

2-1 의 ER 다이어그램을 데이터베이스에 매핑하여 데이터베이스를 생성하고, FastAPI 에서 데이터베이스를 사용할 수 있도록 설정해봅니다.

### RDS 생성

세미나 2 의 실습으로 대체합니다.

### 데이터베이스 모델 구현

2-1 의 ER 다이어그램을 참고하여 데이터베이스 모델을 구현합니다.

### alembic 으로 마이그레이션

alembic 을 사용하여 데이터베이스 마이그레이션을 수행합니다.


## 과제 2-3

여러분은 로켓배송으로 유명한 와팡의 개발자입니다. 과제 1에 이어, 상점과 상품 관리 API 를 구현해야 합니다.
이번에는 데이터베이스를 사용하여 상점과 상품 정보를 저장하고, 조회할 수 있어야 합니다.
더불어, 과제 1에서 구현했던 유저 API 도 데이터베이스를 사용하도록 수정해야 합니다.

### 상점 추가 API

- 상점 추가 API 는 POST 메서드로 `/api/store` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `store_name`, `address`, `email`, `phone_number` 필드를 포함해야 합니다.
  - `store_name` 필드는 3글자 이상 20글자 이하의 문자열이어야 합니다.
  - `address`, `email`, `phone_number`가 비어있다면 사용자의 정보를 사용합니다.
- **한 유저는 최대 하나의 상점만 생성할 수 있습니다.**
- 상점 추가에 성공하면 `201 Created` 상태코드와 함께 상점 정보를 JSON 형식으로 반환합니다.
- ## 상점 추가에 실패하는 경우는 다음과 같습니다.
  - 이미 상점을 생성한 유저가 상점을 추가하려고 할 경우:
    - `409 Conflict` 상태코드와 함께 응답으로 `{"detail": "User already owns a store"}`를 반환합니다.
  - `store_name`, `address`, `email`, `phone_number` 필드 중 하나라도 형식이 올바르지 않은 경우:
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`를 반환합니다.
  - `store_name`, `address`, `email`, `phone_number` 필드 중 1개 이상이 비어있고 유저의 정보로도 대체할 수 없는 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Missing required fields"}`를 반환합니다.
  - 회원가입되지 않은 유저가 상점을 생성하려고 할 경우:
    - `401 Unauthorized` 상태코드를 반환합니다.
  - 이미 존재하는 `store_name`, `email` 또는 `phone_number`를 사용하는 경우:
    - `409 Conflict` 상태코드와 함께 응답으로 `{"detail": "Store already exists"}`, `{"detail": "Email already exists"}`, 또는 `{"detail": "Phone number already exists"}`를 반환합니다.

### 상점 조회 API

- 상점 조회 API는 GET 메서드로 `/api/store/{store_id}` 엔드포인트에 요청을 보내야 합니다.
- `{store_id}`는 조회하고자 하는 상점의 번호 또는 
- 상점이 존재하는 경우, `200 OK` 상태코드와 함께 `store_name`, `address`, `email`, `phone_number` 필드를 포함한 JSON 응답을 반환합니다.
- 상점이 존재하지 않는 경우, `404 Not Found` 상태코드를 반환합니다.

### 상품 추가 API

- 상품 추가 API는 POST 메서드로 `/api/item` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `item_name`, `price`, `stock` 필드를 포함해야 합니다.
  - `item_name` 필드는 2글자 이상 50글자 이하의 문자열이어야 합니다.
  - `price` 필드는 1 이상의 정수이어야 합니다.
  - `stock` 필드는 0 이상의 정수이어야 합니다.
- 상품 추가에 성공하면 `201 Created` 상태코드와 함께 추가된 상품 정보를 JSON 형식으로 반환합니다.
- 상품 추가에 실패하는 경우는 다음과 같습니다.
  - `item_name`, `price`, `stock` 필드 중 하나라도 형식이 올바르지 않은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`
  - 사용자가 상점을 소유하지 않은 경우:
    - `403 Forbidden` 상태코드와 함께 응답으로 `{"detail": "User does not own a store"}`를 반환합니다.
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.

### 상품 수정 API

- 상품 수정 API는 PATCH 메서드로 `/api/item/{item_id}` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `item_name`, `price`, `stock` 필드를 포함할 수 있습니다.
  - `item_name` 필드는 2글자 이상 50글자 이하의 문자열이어야 합니다.
  - `price` 필드는 0보다 큰 정수이어야 합니다.
  - `stock` 필드는 0 이상의 정수이어야 합니다.
- 상품 수정에 성공하면 `200 OK` 상태코드와 함께 수정된 상품 정보를 JSON 형식으로 반환합니다.
- 상품 수정에 실패하는 경우는 다음과 같습니다.
  - `item_name`, `price`, `stock` 필드 중 하나라도 형식이 올바르지 않은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`
  - 상점 또는 상품이 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.
  - 다른 유저 상점의 상품을 수정하려고 할 경우
    - `403 Forbidden` 상태코드를 반환합니다.

### 상품 목록 조회 API

- 상품 목록 조회 API는 GET 메서드로 `/api/items` 엔드포인트에 요청을 보내야 합니다.
- 쿼리 파라미터를 이용해 다음과 같이 필터링할 수 있습니다.
  - `store_id`: 특정 상점의 상품만 조회할 때 사용합니다.
  - `min_price`: 지정된 최소 가격 이상의 상품을 조회할 때 사용합니다.
  - `max_price`: 지정된 최대 가격 이하의 상품을 조회할 때 사용합니다.
  - `in_stock`: `true`로 설정할 경우, 재고가 있는 상품만 조회합니다.
  - 모든 조건은 AND 조건입니다.
- 쿼리 파라미터가 없으면 전체 상품 목록을 반환합니다.
- 요청이 성공하면 `200 OK` 상태코드와 함께 필터링된 상품 목록을 JSON 형식으로 반환합니다.
  - 응답에는 각 상품의 `item_name`, `price`, `stock` 필드가 포함됩니다.
  - 상품이 없는 경우, 빈 배열을 반환합니다.
- 상점이 존재하지 않는 경우, `404 Not Found` 상태코드를 반환합니다.


### 상품 찜 API

- 상품 찜 API는 POST 메서드로 `/api/item/{item_id}/like` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 상품을 찜하면, 유저의 찜 목록에 상품이 추가됩니다.
- 상품 찜에 성공하면 `201 Created` 상태코드를 반환합니다.
  - 이미 찜한 상품을 다시 찜하려고 할 경우, `200 OK` 상태코드를 반환합니다.
- 상품 찜에 실패하는 경우는 다음과 같습니다.
  - 상품이 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.

### 상품 찜 취소 API

- 상품 찜 취소 API는 DELETE 메서드로 `/api/item/{item_id}/like` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 상품 찜 취소에 성공하면 `204 No Content` 상태코드를 반환합니다.
  - 찜하지 않은 상품인 경우, `200 OK` 상태코드를 반환합니다.
- 상품 찜 취소에 실패하는 경우는 다음과 같습니다.
  - 상품이 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.

### 상품 주문 API

- 상품 주문 API는 POST 메서드로 `/api/order` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `items` 필드를 포함해야 합니다.
  - `items` 필드는 상품의 id와 수량을 포함하는 배열이어야 합니다.
  - 수량은 1 이상의 정수이어야 합니다.
- 주문에 성공하면 `201 Created` 상태코드와 함께 주문 정보를 JSON 형식으로 반환합니다.
- 주문에 실패하는 경우는 다음과 같습니다.
  - `items` 필드가 없는 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Missing required fields"}`를 반환합니다.
  - 상품이 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.
  - 주문할 수량이 재고보다 많은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Not enough stock"}`를 반환합니다.
  
### 상품 주문 조회 API

- 상품 주문 조회 API는 GET 메서드로 `/api/order/{order_id}` 엔드포인트에 요청을 보내야 합니다.
- 주문이 존재하는 경우, `200 OK` 상태코드와 함께 주문 정보를 JSON 형식으로 반환합니다.
- 주문이 존재하지 않는 경우, `404 Not Found` 상태코드를 반환합니다.

### 상품 주문 취소 API

- 상품 주문 취소 API는 DELETE 메서드로 `/api/order/{order_id}` 엔드포인트에 요청을 보내야 합니다.
- 주문 취소에 성공하면 `204 No Content` 상태코드를 반환합니다.
- 주문 취소에 실패하는 경우는 다음과 같습니다.
  - 주문이 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 다른 유저의 주문을 취소하려고 할 경우
    - `403 Forbidden` 상태코드를 반환합니다.

### 리뷰 추가 API

- 리뷰 추가 API는 POST 메서드로 `/api/review` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `item_id`, `rating`, `content` 필드를 포함해야 합니다.
  - `rating` 필드는 1 이상 5 이하의 정수이어야 합니다.
  - `content` 필드는 1글자 이상 1000글자 이하의 문자열이어야 합니다.
- 리뷰 추가에 성공하면 `201 Created` 상태코드와 함께 리뷰 정보를 JSON 형식으로 반환합니다.
- 리뷰 추가에 실패하는 경우는 다음과 같습니다.
  - `item_id`, `rating`, `content` 필드 중 하나라도 형식이 올바르지 않은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`
  - 상품이 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.
  - 이미 리뷰를 작성한 상품에 대해 리뷰를 작성하려고 할 경우
    - `409 Conflict` 상태코드를 반환합니다.

### 리뷰 조회 API

- 리뷰 조회 API는 GET 메서드로 `/api/review/{item_id}` 엔드포인트에 요청을 보내야 합니다.
- 상품에 대한 리뷰가 존재하는 경우, `200 OK` 상태코드와 함께 리뷰 목록을 JSON 형식으로 반환합니다.
- 상품에 대한 리뷰가 존재하지 않는 경우, `404 Not Found` 상태코드를 반환합니다.

### 리뷰 수정 API

- 리뷰 수정 API는 PATCH 메서드로 `/api/review/{review_id}` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `rating`, `content` 필드를 포함할 수 있습니다.
  - `rating` 필드는 1 이상 5 이하의 정수이어야 합니다.
  - `content` 필드는 1글자 이상 1000글자 이하의 문자열이어야 합니다.
- 리뷰 수정에 성공하면 `200 OK` 상태코드와 함께 수정된 리뷰 정보를 JSON 형식으로 반환합니다.
- 리뷰 수정에 실패하는 경우는 다음과 같습니다.
  - `rating`, `content` 필드 중 하나라도 형식이 올바르지 않은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`
  - 리뷰가 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 다른 유저의 리뷰를 수정하려고 할 경우
    - `403 Forbidden` 상태코드를 반환합니다.

### 리뷰 삭제 API

- 리뷰 삭제 API는 DELETE 메서드로 `/api/review/{review_id}` 엔드포인트에 요청을 보내야 합니다.
- 리뷰 삭제에 성공하면 `204 No Content` 상태코드를 반환합니다.
- 리뷰 삭제에 실패하는 경우는 다음과 같습니다.
  - 리뷰가 존재하지 않는 경우
    - `404 Not Found` 상태코드를 반환합니다.
  - 다른 유저의 리뷰를 삭제하려고 할 경우
    - `403 Forbidden` 상태코드를 반환합니다.



## 채점 기준

- 데이터베이스 모델이 ER 다이어그램을 잘 반영하고 있음
- 데이터베이스 마이그레이션을 성공적으로 수행함
- API 가 요구사항에 맞게 동작함
- API 가 데이터베이스를 사용하여 동작함
- API 가 예외 상황에 대해 적절한 응답을 반환함

## 제출 방법

과제 수락 시 생성된 레포지터리의 `main` 브랜치에 완성된 코드를 푸시하세요.

**(주의⚠️) Feedback PR 은 머지하지 마세요!**

## 참고 문서

sqlite3.version
이 모듈의 버전 번호(문자열). SQLite 라이브러리의 버전이 아닙니다.

sqlite3.version_info
이 모듈의 버전 번호(정수들의 튜플). SQLite 라이브러리의 버전이 아닙니다.

sqlite3.sqlite_version
런타임 SQLite 라이브러리의 버전 번호(문자열).

sqlite3.sqlite_version_info
런타임 SQLite 라이브러리의 버전 번호(정수들의 튜플).

sqlite3.PARSE_DECLTYPES
이 상수는 connect() 함수의 detect_types 매개 변수에 사용됩니다.

이것을 설정하면 sqlite3 모듈은 반환되는 각 열에 대해 선언된 형을 구문 분석합니다. 선언된 형의 첫 번째 단어를 구문 분석합니다, 즉 《integer primary key》에서는 《integer》를, 《number (10)》에서는 《number》를 구문 분석합니다. 그런 다음 해당 열에 대해, 변환기 딕셔너리를 조사하고 그 형에 대해 등록된 변환기 함수를 사용합니다.

sqlite3.PARSE_COLNAMES
이 상수는 connect() 함수의 detect_types 매개 변수에 사용됩니다.

이것을 설정하면 SQLite 인터페이스는 반환되는 각 열의 열 이름을 구문 분석합니다. 거기에서 [mytype] 형태의 문자열을 찾은 다음 〈mytype’을 열의 형으로 결정합니다. 변환기 딕셔너리에서 〈mytype〉 항목을 찾은 다음 거기에 있는 변환기 함수를 사용하여 값을 반환하려고 시도합니다. Cursor.description에서 발견되는 열 이름은 형 이름을 포함하지 않습니다, 즉, SQL에서 'as "Expiration date [datetime]"'와 같은 것을 사용하면, 열 이름의 첫 번째 '['까지 모든 것을 구문 분석하고 앞에 오는 공백을 제거합니다: 열 이름은 단순히 《Expiration date》 가 됩니다.

sqlite3.connect(database[, timeout, detect_types, isolation_level, check_same_thread, factory, cached_statements, uri])
SQLite 데이터베이스 파일 database에 대한 연결을 엽니다. 사용자 정의 factory가 주어지지 않는 한, 기본적으로 Connection 객체를 반환합니다.

database는 열릴 데이터베이스 파일의 경로명(절대 혹은 현재 작업 디렉터리에 대한 상대)을 제공하는 경로류 객체입니다. ":memory:"를 사용하여 디스크 대신 램(RAM)에 있는 데이터베이스에 대한 데이터베이스 연결을 열 수 있습니다.

데이터베이스가 여러 연결을 통해 액세스 되고, 프로세스 중 하나가 데이터베이스를 수정할 때, 해당 트랜잭션이 커밋될 때까지 SQLite 데이터베이스가 잠깁니다. timeout 매개 변수는 예외를 일으키기 전에 잠금이 해제되기를 연결이 기다려야 하는 시간을 지정합니다. timeout 매개 변수의 기본값은 5.0(5초)입니다.

isolation_level 매개 변수는 Connection 객체의 isolation_level 프로퍼티를 참조하십시오.

SQLite는 기본적으로 TEXT, INTEGER, REAL, BLOB 및 NULL 형만 지원합니다. 다른 형을 사용하려면 직접 지원을 추가해야 합니다. detect_types 매개 변수와 모듈 수준 register_converter() 함수로 등록된 사용자 정의 변환기를 사용하면 쉽게 할 수 있습니다.

detect_types defaults to 0 (i. e. off, no type detection), you can set it to any combination of PARSE_DECLTYPES and PARSE_COLNAMES to turn type detection on. Due to SQLite behaviour, types can’t be detected for generated fields (for example max(data)), even when detect_types parameter is set. In such case, the returned type is str.

기본적으로 check_same_thread는 True며, 만들고 있는 스레드 만 이 연결을 사용할 수 있습니다. False로 설정하면 반환된 연결을 여러 스레드에서 공유할 수 있습니다. 여러 스레드에서 같은 연결을 사용할 때, 데이터 손상을 피하려면 쓰기 연산을 사용자가 직렬화해야 합니다.

기본적으로, sqlite3 모듈은 connect 호출에 Connection 클래스를 사용합니다. 그러나, Connection 클래스의 서브 클래스를 만들고 factory 매개 변수에 클래스를 제공하면 connect()가 그 클래스를 사용하게 할 수 있습니다.

자세한 내용은 이 설명서의 섹션 SQLite 와 파이썬 형을 참조하십시오.

sqlite3 모듈은 내부적으로 SQL 구문 분석 오버헤드를 피하고자 명령문 캐시를 사용합니다. 연결에 대해 캐시 되는 명령문의 수를 명시적으로 설정하려면, cached_statements 매개 변수를 설정할 수 있습니다. 현재 구현된 기본값은 100개의 명령문을 캐시 하는 것입니다.

uri가 참이면 database는 URI로 해석됩니다. 이렇게 하면 옵션을 지정할 수 있습니다. 예를 들어, 읽기 전용 모드로 데이터베이스를 열려면 다음과 같이 할 수 있습니다:

db = sqlite3.connect('file:path/to/database?mode=ro', uri=True)
인식되는 옵션 목록을 포함하여, 이 기능에 대한 자세한 내용은 SQLite URI documentation에서 찾을 수 있습니다.

인자 database로 감사 이벤트(auditing event) sqlite3.connect를 발생시킵니다.

버전 3.4에서 변경: uri 매개 변수가 추가되었습니다.

버전 3.7에서 변경: database는 이제 문자열뿐만 아니라 경로류 객체 일 수도 있습니다.

sqlite3.register_converter(typename, callable)
데이터베이스의 바이트열을 사용자 정의 파이썬 형으로 변환할 수 있는 콜러블을 등록합니다. 콜러블은 형 typename 인 모든 데이터베이스 값에 대해 호출됩니다. 형 감지 작동 방식에 대해서는 connect() 함수의 매개 변수 detect_types를 참고하십시오. typename과 질의의 형 이름은 대/소문자를 구분하지 않고 일치시킴에 유의하십시오.

sqlite3.register_adapter(type, callable)
사용자 정의 파이썬 형 type을 SQLite의 지원되는 형 중 하나로 변환할 수 있는 콜러블을 등록합니다. 콜러블 callable은 단일 매개 변수로 파이썬 값을 받아들이고 다음 형들의 값을 반환해야 합니다: int, float, str 또는 bytes.

sqlite3.complete_statement(sql)
문자열 sql에 세미콜론으로 끝나는 하나 이상의 완전한 SQL 문이 포함되어 있으면 True를 반환합니다. SQL이 문법적으로 올바른지 확인하지는 않습니다. 닫히지 않은 문자열 리터럴이 없고 명령문이 세미콜론으로 끝나는지만 확인합니다.

이것은 다음 예제와 같이, SQLite 용 셸을 만드는데 사용할 수 있습니다:
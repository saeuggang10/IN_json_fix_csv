# Json_fix
-------------------------------
### 설명
```
 프로젝트 방침 변경으로 데이터를 모두 수정하게 되어 만들게 되었습니다.
 변경하기로 결정된 key값을 key리스트에, 삭제할 key는 key_del리스트에 넣은 후 not in을 활용해 수정할 key값인지 삭제할 key값인지 확인해 변경사항에 따라 바꿔줍니다.
```


# Json_csv
-------------------------------
### 설명
```
바뀐 json내용을 csv파일로 만들어줍니다.
(요청에 따라 Json_fix과 Json_csv파일로 나뉘어져 있습니다.)
```

-------------------------------
-------------------------------

### package
```
import glob
import pandas as pd
import json
from csv import DictWriter
import re
import math
import collections
```

### def
```
가로로 긴 사각형인지, 세로로 긴 사각형인지 구분하기 위한 수식입니다.
```

### input
```
targetDirectory = '주소를 입력해주세요'
```

-------------------------------
-------------------------------

#### 첨부파일
1. 57.Sample_v1.3-test.zip
    * 코드 테스팅을 위한 파일들이며 각각 버전이 다릅니다

2. makefromJson.csv
    * Json_csv.py 실행결과 만들어지는 csv파일입니다
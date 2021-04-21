from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.tag import Twitter

example = u"지난 2012년 대선 당시 국정원이 이른바 '대선 댓글 사건'에 직접 개입한 것으로 드러났다. 이후 민주당은 이듬해 원세훈 전 원장을 서울중앙지검에 고발했다."

taggers = [ ('꼬꼬마', Kkma()),
            ('코모란', Komoran()),
            ('트위터', Twitter()),
            ('한나눔', Hannanum())]
####################################################
# 공통 함수 테스트
###################################################
for name,tagger in taggers:
    print('%s %s %s'%('-'*10,name,'-'*10))
    try:
        print(tagger.pos(example))    # 품사 태깅
        print(tagger.morphs(example)) # 형태소만 추출
        print(tagger.nouns(example))  # 명사 추출
    except Exception as e:
        print(e)

#####################################################
# 단독 함수 및 옵션 테스트
#####################################################
print('='*50)

# [ 꼬꼬마 ]
print( taggers[0][1].sentences( example ) ) # 문장 추출
print('-'*50)
# [ 코모란 ]
print( taggers[1][1].pos( phrase=example, flatten=False ) ) # flatten=False이면, 어절 단위 PoS Tagging
print( taggers[1][1].pos( phrase=example, flatten=True ) )  # 차이 비교용
print('-'*50)
# [ 트위터 ]
print( taggers[2][1].pos( phrase=example, norm=True, stem=True) ) # norm=True 이면, 토큰 노멀라이즈, stem=True 이면, 토큰 스테밍
print( taggers[2][1].pos( phrase=example, norm=False, stem=False) ) # 차이 비교용
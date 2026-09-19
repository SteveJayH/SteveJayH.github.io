# Seungjae Han — 홈페이지 리디자인

## 디자인과 구성

Kanaka Rajan의 연구자 프로필 페이지에서 인물 소개 중심의 구성과 학력·경력·수상 내역을 구분하는 방식을 참고했습니다. 원본의 코드, 로고, 사진은 복제하지 않았습니다. 따뜻한 아이보리 배경, 짙은 청록색 글자, 테라코타 강조색, 큰 세리프 제목과 넓은 여백으로 별도의 디자인을 구현했습니다.

`index.html`에는 프로필, 최근 소식, 연구 분야, 대표 논문, 경력·학력·펠로십, 수상 내역, 학술 봉사 활동과 연락처가 있습니다. `publications.html`에는 기존 16개 논문 기록을 연도순으로 정리했습니다. 논문 유형, 연도, 제목·저자·학술지 검색 조건을 조합할 수 있습니다.

## 파일

- `index.html`: 메인 홈페이지. 내용 수정은 이 파일에서 합니다.
- `publications.html`: 전체 논문 목록. 새 논문은 해당 연도의 `.publication-list`에 `.publication` 항목으로 추가합니다.
- `assets/site.css`: 두 페이지에서 공유하는 반응형 스타일. 색상과 기본 치수는 상단 `:root`에서 조정합니다.
- `assets/site.js`: 모바일 메뉴, 현재 섹션 표시, 논문 필터와 검색.
- `.github/workflows/website-preview.yml`: 읽기 권한으로 실행되는 브라우저 검사와 미리보기 ZIP 생성.

기존 `photo.jpeg`, `nature_methods_cover.png`, `CV_SeungjaeHan_0707.pdf`, `PREVIOUS/`는 변경하지 않았습니다. 프로필 사진과 CV 링크는 기존 파일을 계속 사용합니다. 새로운 사진, 경력, 소속, 수상 내역, 연구 실적을 임의로 추가하지 않았습니다.

## 동작과 접근성

웹사이트 자체는 HTML/CSS/JavaScript 정적 파일이며 빌드 과정, 서버, npm 패키지 또는 외부 웹폰트가 필요하지 않습니다. 압축을 푼 후 `index.html`을 브라우저에서 열면 됩니다. 로컬 서버를 사용할 때는 저장소 루트에서 `python -m http.server 8000`을 실행할 수 있습니다.

모바일 메뉴에는 `aria-expanded`, Escape 닫기와 포커스 복귀를 적용했습니다. 키보드 포커스 표시, 본문 건너뛰기 링크, 검색 입력 레이블, 필터 결과의 라이브 알림, 동작 줄이기 설정, 인쇄용 스타일을 포함했습니다. JavaScript를 끈 경우에도 메뉴와 전체 논문 목록은 읽을 수 있습니다. 추적 스크립트나 개인정보 수집 폼은 없습니다.

## 내용 처리

프로필, 학력, 경력, 수상과 뉴스는 기존 홈페이지의 내용을 유지하면서 문장과 배치를 정리했습니다. 연구 분야별 설명은 기존 소개와 논문 주제를 요약한 편집 문구입니다.

기존 bioRxiv 기록 두 건은 정식 학술지 논문과 구분하기 위해 `preprint` 유형으로 분류했습니다. IMPASTO 기록의 기존 `Cover · KAIST Breakthroughs` 강조 문구는 확인되지 않아 새 디자인에 포함하지 않았습니다. Nature Electronics 논문 제목은 출판사 페이지에 표시된 정식 제목으로 정리했습니다. 대표 논문 두 편과 WACV 2025에는 출판사/학회 원문 링크를 연결했고, 나머지 기록에는 명시적으로 표시한 Google Scholar 검색 링크를 제공합니다. 인용 수 등 변동하는 지표는 새로 추가하지 않았습니다.

## 검토 및 적용

이 변경은 `redesign/rajan-inspired-20260918` 브랜치의 검토용 제안입니다. `main`과 현재 공개 홈페이지는 변경하지 않습니다. PR을 병합하면 기존 GitHub Pages의 main 배포 흐름에 반영됩니다.

PR 검사에는 320, 390, 560, 768, 1024, 1440px 화면의 가로 넘침, 프로필 사진 로딩, 모바일 메뉴, 과거 뉴스 펼치기, 논문 유형별 개수, 연도/검색 조합, 검색 결과 없음, 필터 초기화, JavaScript 비활성 상태의 콘텐츠 검사가 포함됩니다. 검사 성공 시 `seungjae-han-redesign-preview` 아티팩트에 사이트 파일, 기존 사진과 CV, 데스크톱/모바일 화면 이미지, 테스트 결과 JSON이 저장됩니다. 아티팩트 보관 기간은 14일입니다.

## 참고 자료

- 구성 참고: https://www.rajanlab.com/kanaka-rajan
- 기존 홈페이지: https://stevejayh.github.io/
- 기존 논문 목록: https://stevejayh.github.io/publications.html
- Nature Electronics: https://www.nature.com/articles/s41928-024-01318-6
- Nature Methods: https://www.nature.com/articles/s41592-023-02005-8
- WACV 2025: https://openaccess.thecvf.com/content/WACV2025/html/Yu_Design_Principles_of_Multi-Scale_J-Invariant_Networks_for_Self-Supervised_Image_Denoising_WACV_2025_paper.html

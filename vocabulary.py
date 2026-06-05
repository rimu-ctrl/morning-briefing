"""
영어 단어(WORDS)와 숙어/표현(IDIOMS)을 날짜 기반으로 각각 20개/10개 선택합니다.
"""

from datetime import date
from typing import List, Dict

# ── 단어 (80개) ────────────────────────────────────────────────────────────────
WORDS: List[Dict] = [
    {"word": "abstraction",    "type": "n",     "meaning": "추상화; 핵심만 남기고 세부를 감추는 것",          "example": "Good API design relies on abstraction to hide complexity."},
    {"word": "accessibility",  "type": "n",     "meaning": "접근성",                                         "example": "Designing for accessibility benefits all users, not just those with disabilities."},
    {"word": "advocate",       "type": "v/n",   "meaning": "지지하다; 옹호자",                               "example": "Designers should advocate for the user in every product meeting."},
    {"word": "affordance",     "type": "n",     "meaning": "행동 유도성 (디자인이 사용법을 암시하는 속성)",   "example": "The raised button shape is an affordance that invites clicking."},
    {"word": "agile",          "type": "adj",   "meaning": "민첩한; 애자일 방법론의",                        "example": "Agile teams release small updates frequently to reduce risk."},
    {"word": "align",          "type": "v",     "meaning": "맞추다, 일치시키다",                             "example": "We need to align product goals with user needs before we start."},
    {"word": "ambiguous",      "type": "adj",   "meaning": "모호한, 불분명한",                               "example": "The brief was ambiguous, so we scheduled a clarification call."},
    {"word": "benchmark",      "type": "v/n",   "meaning": "기준으로 삼다; 비교 기준",                       "example": "We benchmarked competitor apps to identify UX gaps."},
    {"word": "catalyst",       "type": "n",     "meaning": "촉매, 변화를 일으키는 요인",                     "example": "The pandemic was a catalyst for remote-first product design."},
    {"word": "cognitive load", "type": "n",     "meaning": "인지 부하 (사용자가 처리해야 할 정신적 노력)",   "example": "A cluttered UI increases cognitive load and leads to user errors."},
    {"word": "cohesive",       "type": "adj",   "meaning": "일관되고 통일된",                               "example": "A cohesive brand identity builds user trust across all platforms."},
    {"word": "compelling",     "type": "adj",   "meaning": "설득력 있는, 매력적인",                          "example": "A compelling value proposition is the foundation of good product copy."},
    {"word": "concise",        "type": "adj",   "meaning": "간결한",                                         "example": "Keep error messages concise — users don't read long explanations."},
    {"word": "connotation",    "type": "n",     "meaning": "함축, 내포된 의미",                              "example": "The color red carries a connotation of urgency in most Western interfaces."},
    {"word": "constraint",     "type": "n",     "meaning": "제약 조건",                                      "example": "Working within tight constraints often sparks the most creative solutions."},
    {"word": "converge",       "type": "v",     "meaning": "수렴하다, 한 점으로 모이다",                     "example": "After diverging with ideas, the team converged on a single direction."},
    {"word": "curate",         "type": "v",     "meaning": "엄선하다, 큐레이션하다",                         "example": "The dashboard curates only the most relevant KPIs for each user role."},
    {"word": "dependency",     "type": "n",     "meaning": "의존성, 종속 관계",                              "example": "A circular dependency in the component library caused build failures."},
    {"word": "deploy",         "type": "v",     "meaning": "배포하다",                                       "example": "We deploy to production every Friday after a full regression test."},
    {"word": "deprecate",      "type": "v",     "meaning": "(기능·API를) 사용 중단 예정으로 표시하다",       "example": "The old endpoint will be deprecated in the next major release."},
    {"word": "discern",        "type": "v",     "meaning": "식별하다, 파악하다",                             "example": "Good designers can discern signal from noise in user feedback."},
    {"word": "disruptive",     "type": "adj",   "meaning": "파괴적인, 기존을 뒤흔드는",                      "example": "Uber introduced a disruptive model to the taxi industry."},
    {"word": "ecosystem",      "type": "n",     "meaning": "생태계 (제품·서비스 환경)",                      "example": "Apple's ecosystem keeps users locked into its products and services."},
    {"word": "empirical",      "type": "adj",   "meaning": "경험적인, 실증적인",                             "example": "Design decisions should be backed by empirical evidence, not assumptions."},
    {"word": "facilitate",     "type": "v",     "meaning": "촉진하다, 수월하게 하다",                        "example": "Good information architecture facilitates faster user decision-making."},
    {"word": "fallback",       "type": "n",     "meaning": "폴백, 오류 시 대체 동작",                        "example": "Always design a fallback for cases where assets fail to load."},
    {"word": "fidelity",       "type": "n",     "meaning": "충실도 (hi-fi/lo-fi 프로토타입의)",              "example": "Start with low-fidelity wireframes before investing in high-fidelity mockups."},
    {"word": "friction",       "type": "n",     "meaning": "마찰, 불편함 (UX에서 방해 요소)",               "example": "Removing friction from sign-up increased conversion by 40%."},
    {"word": "gestalt",        "type": "n",     "meaning": "게슈탈트 (전체로 인식되는 형태·구조)",           "example": "Gestalt principles explain why users perceive grouped elements as a single unit."},
    {"word": "granular",       "type": "adj",   "meaning": "세분화된, 세밀한",                              "example": "We need granular analytics to understand where users drop off."},
    {"word": "handoff",        "type": "n",     "meaning": "핸드오프 (디자인→개발 전달)",                   "example": "A clean design handoff reduces back-and-forth between designers and engineers."},
    {"word": "heuristic",      "type": "n/adj", "meaning": "경험 법칙; 직관적 평가",                         "example": "Nielsen's 10 heuristics are a standard for UI evaluation."},
    {"word": "hierarchy",      "type": "n",     "meaning": "계층 구조, 시각적 우선순위",                    "example": "Strong visual hierarchy guides the user's eye to the most important action."},
    {"word": "holistic",       "type": "adj",   "meaning": "전체적·통합적인",                               "example": "A holistic UX strategy considers both digital and physical touchpoints."},
    {"word": "hypothesis",     "type": "n",     "meaning": "가설",                                           "example": "We tested the hypothesis that a shorter form would increase completions."},
    {"word": "idempotent",     "type": "adj",   "meaning": "멱등성의 (같은 요청을 여러 번 해도 결과가 동일)", "example": "DELETE requests should be idempotent — calling them twice should be safe."},
    {"word": "inclusive",      "type": "adj",   "meaning": "포용적인, 모든 사용자를 고려하는",               "example": "Inclusive design benefits people with and without disabilities alike."},
    {"word": "intuitive",      "type": "adj",   "meaning": "직관적인, 설명 없이 이해되는",                   "example": "The gesture navigation felt intuitive after just one use."},
    {"word": "iterate",        "type": "v",     "meaning": "반복·개선하다",                                  "example": "The team iterated on the prototype three times before launch."},
    {"word": "iterative",      "type": "adj",   "meaning": "반복적인, 점진적 개선의",                        "example": "An iterative design process reduces the risk of building the wrong thing."},
    {"word": "juxtapose",      "type": "v",     "meaning": "나란히 놓고 대비하다",                           "example": "Juxtaposing the old and new designs made the improvement obvious."},
    {"word": "latency",        "type": "n",     "meaning": "지연 시간",                                      "example": "High latency in the API response made the interface feel sluggish."},
    {"word": "legacy",         "type": "n/adj", "meaning": "레거시, 구식 시스템·코드",                       "example": "Migrating off legacy infrastructure was painful but necessary."},
    {"word": "leverage",       "type": "v/n",   "meaning": "(강점·자원을) 최대한 활용하다",                  "example": "We can leverage this user data to improve the onboarding flow."},
    {"word": "meticulous",     "type": "adj",   "meaning": "꼼꼼한, 세심한",                                "example": "Meticulous attention to spacing and alignment defines polished UI."},
    {"word": "mental model",   "type": "n",     "meaning": "멘탈 모델 (사용자가 시스템에 대해 갖는 내적 이해)", "example": "The new navigation broke users' existing mental models of the app."},
    {"word": "microinteraction","type": "n",    "meaning": "마이크로인터랙션 (세밀한 UI 피드백)",            "example": "The 'like' animation is a microinteraction that reinforces user action."},
    {"word": "mitigate",       "type": "v",     "meaning": "(위험·문제를) 완화·줄이다",                     "example": "Regular usability tests help mitigate costly design mistakes."},
    {"word": "modular",        "type": "adj",   "meaning": "모듈식의, 조립식의",                             "example": "A modular design system allows teams to build pages like Lego blocks."},
    {"word": "nascent",        "type": "adj",   "meaning": "초기 단계의, 막 시작된",                        "example": "Voice UI is still a nascent field with many unsolved design challenges."},
    {"word": "nuanced",        "type": "adj",   "meaning": "미묘한 차이가 있는, 세밀한",                    "example": "User feedback was nuanced and required careful qualitative analysis."},
    {"word": "onboarding",     "type": "n",     "meaning": "신규 사용자 안내 프로세스",                      "example": "Good onboarding reduces churn in the critical first 7 days."},
    {"word": "optimize",       "type": "v",     "meaning": "최적화하다",                                     "example": "We optimized the image pipeline to reduce load time by 60%."},
    {"word": "orchestrate",    "type": "v",     "meaning": "조율하다, 체계적으로 구성하다",                  "example": "The design lead orchestrated a week-long sprint to align all stakeholders."},
    {"word": "paradigm",       "type": "n",     "meaning": "패러다임, 사고의 틀",                            "example": "Agile was a paradigm shift from waterfall development."},
    {"word": "parameter",      "type": "n",     "meaning": "매개변수; 범위·한계",                            "example": "Setting clear parameters early prevents scope creep in projects."},
    {"word": "persona",        "type": "n",     "meaning": "페르소나 (가상의 목표 사용자)",                  "example": "We defined three personas to guide feature prioritization."},
    {"word": "pivot",          "type": "v/n",   "meaning": "방향 전환하다; 전략적 전환",                     "example": "After usability testing, we pivoted to a simpler navigation model."},
    {"word": "pragmatic",      "type": "adj",   "meaning": "실용적인",                                       "example": "A pragmatic approach skips perfection and ships a working MVP."},
    {"word": "prioritize",     "type": "v",     "meaning": "우선순위를 정하다",                              "example": "Prioritizing accessibility ensures the product works for all users."},
    {"word": "proliferate",    "type": "v",     "meaning": "급증하다, 빠르게 확산되다",                      "example": "AI-powered tools have proliferated in the design industry."},
    {"word": "prototype",      "type": "n/v",   "meaning": "프로토타입; 시제품을 만들다",                    "example": "We prototyped the new nav in Figma before a single line of code was written."},
    {"word": "redundant",      "type": "adj",   "meaning": "중복된, 불필요한",                               "example": "Redundant UI elements clutter the screen and confuse users."},
    {"word": "refactor",       "type": "v",     "meaning": "(기능 변화 없이) 코드를 개선·정리하다",          "example": "We refactored the component library to improve reusability."},
    {"word": "regression",     "type": "n",     "meaning": "리그레션 (이전에 작동하던 기능이 깨지는 현상)",  "example": "Every release includes a regression test to catch newly broken features."},
    {"word": "resilient",      "type": "adj",   "meaning": "회복력 있는, 탄탄한",                           "example": "A resilient system degrades gracefully rather than crashing completely."},
    {"word": "responsive",     "type": "adj",   "meaning": "반응형의; 빠르게 반응하는",                      "example": "Responsive design ensures the app works across all screen sizes."},
    {"word": "robust",         "type": "adj",   "meaning": "강력하고 신뢰할 수 있는",                        "example": "A robust error-handling system prevents cascading failures."},
    {"word": "scalable",       "type": "adj",   "meaning": "확장 가능한",                                    "example": "The design system needs to be scalable across 10+ product lines."},
    {"word": "seamless",       "type": "adj",   "meaning": "매끄러운, 끊김 없는",                            "example": "A seamless handoff between screens keeps users in a flow state."},
    {"word": "stakeholder",    "type": "n",     "meaning": "이해관계자",                                     "example": "Early stakeholder alignment prevents costly changes late in the project."},
    {"word": "streamline",     "type": "v",     "meaning": "간소화·효율화하다",                              "example": "Streamlining the checkout process reduced cart abandonment by 30%."},
    {"word": "succinct",       "type": "adj",   "meaning": "간결하고 명확한",                                "example": "Succinct microcopy guides users without overwhelming them."},
    {"word": "synthesize",     "type": "v",     "meaning": "(정보를) 통합·종합하다",                         "example": "She synthesized findings from 20 interviews into clear design principles."},
    {"word": "tangible",       "type": "adj",   "meaning": "구체적인, 실질적인",                             "example": "We need tangible outcomes from this workshop, not just sticky notes."},
    {"word": "throughput",     "type": "n",     "meaning": "처리량, 처리 속도",                              "example": "Increasing server throughput reduced page load time significantly."},
    {"word": "token",          "type": "n",     "meaning": "디자인 토큰 (색상·간격·폰트의 변수)",            "example": "Design tokens ensure color consistency across web and mobile platforms."},
    {"word": "tradeoff",       "type": "n",     "meaning": "트레이드오프, 상충 관계",                        "example": "There's always a tradeoff between performance and visual richness."},
    {"word": "trajectory",     "type": "n",     "meaning": "궤적, 발전 방향",                               "example": "The product's trajectory shifted after the acquisition."},
    {"word": "transparent",    "type": "adj",   "meaning": "투명한, 명확한",                                 "example": "Being transparent about data usage builds user confidence."},
    {"word": "validate",       "type": "v",     "meaning": "검증하다, 확인하다",                             "example": "Prototype testing validates assumptions before full development."},
    {"word": "verbatim",       "type": "adv",   "meaning": "그대로, 원문 그대로",                            "example": "Quote user feedback verbatim in your research report for authenticity."},
    {"word": "viable",         "type": "adj",   "meaning": "실행 가능한",                                    "example": "We need a viable MVP that can be shipped within one sprint."},
    {"word": "whitespace",     "type": "n",     "meaning": "여백 (디자인에서의 빈 공간)",                    "example": "Strategic use of whitespace improves readability and visual hierarchy."},
]

# ── 숙어/표현 (30개) ───────────────────────────────────────────────────────────
IDIOMS: List[Dict] = [
    {"word": "at the end of the day",       "type": "idiom", "meaning": "결국, 결론적으로",                          "example": "At the end of the day, user satisfaction is the only metric that matters."},
    {"word": "back to the drawing board",   "type": "idiom", "meaning": "처음부터 다시 시작하다",                   "example": "The user tests failed completely — it's back to the drawing board."},
    {"word": "ballpark figure",             "type": "idiom", "meaning": "대략적인 수치·견적",                       "example": "Can you give me a ballpark figure for the dev effort required?"},
    {"word": "bandwidth",                   "type": "n (fig)","meaning": "여유 시간·여력 (비유적)",                  "example": "I don't have the bandwidth to take on another project this sprint."},
    {"word": "bite off more than you can chew","type":"idiom","meaning": "감당할 수 없을 만큼 많이 맡다",           "example": "We bit off more than we could chew by targeting three platforms at once."},
    {"word": "boil the ocean",              "type": "idiom", "meaning": "불필요하게 범위를 넓히다",                  "example": "We don't need to boil the ocean — focus on the top 3 user flows first."},
    {"word": "bring to the table",          "type": "idiom", "meaning": "기여하다, 가치를 제공하다",                "example": "Strong visual storytelling is what she brings to the table."},
    {"word": "circle back",                 "type": "idiom", "meaning": "나중에 다시 논의하다",                     "example": "Let's circle back on pricing once we have more user data."},
    {"word": "deep dive",                   "type": "idiom", "meaning": "깊이 있는 분석·탐구",                     "example": "We did a deep dive into competitor apps before defining our strategy."},
    {"word": "dog fooding",                 "type": "idiom", "meaning": "자사 제품을 직접 사용해 테스트하다",       "example": "Dog fooding the app daily helps us catch bugs before users do."},
    {"word": "double down",                 "type": "idiom", "meaning": "더 강하게 밀어붙이다, 배로 노력하다",     "example": "After the positive A/B test, we doubled down on that design direction."},
    {"word": "flip the script",             "type": "idiom", "meaning": "기존 방식을 완전히 바꾸다",               "example": "Instead of surveying, we flipped the script and had users teach us live."},
    {"word": "game changer",                "type": "idiom", "meaning": "판도를 바꾸는 것",                         "example": "Real-time collaboration in Figma was a game changer for design teams."},
    {"word": "give the green light",        "type": "idiom", "meaning": "승인하다, 진행 허가를 주다",              "example": "The VP gave the green light to launch the redesign next quarter."},
    {"word": "go the extra mile",           "type": "idiom", "meaning": "기대 이상으로 노력하다",                  "example": "Going the extra mile on micro-animations made the app feel truly premium."},
    {"word": "heads up",                    "type": "idiom", "meaning": "미리 알림, 사전 공지",                    "example": "Just a heads up — the API will be down for maintenance tonight."},
    {"word": "hit the ground running",      "type": "idiom", "meaning": "즉시 열정적으로 시작하다",               "example": "The new designer hit the ground running and shipped a redesign in week one."},
    {"word": "in the pipeline",             "type": "idiom", "meaning": "진행 중인, 계획된",                       "example": "A dark mode update is in the pipeline for Q3."},
    {"word": "keep the ball rolling",       "type": "idiom", "meaning": "진행을 계속 유지하다",                   "example": "Daily standups help keep the ball rolling on long projects."},
    {"word": "level up",                    "type": "idiom", "meaning": "실력·수준을 높이다",                      "example": "This project was a chance to level up our animation skills."},
    {"word": "low-hanging fruit",           "type": "idiom", "meaning": "쉽게 달성 가능한 목표",                  "example": "Fixing broken links is low-hanging fruit — quick wins with real impact."},
    {"word": "move the needle",             "type": "idiom", "meaning": "의미 있는 차이를 만들다",                "example": "Small UI tweaks didn't move the needle — we needed a full redesign."},
    {"word": "north star",                  "type": "idiom", "meaning": "핵심 목표, 지향점",                       "example": "Our north star metric is weekly active users, not total installs."},
    {"word": "on the back burner",          "type": "idiom", "meaning": "일시 보류 중인",                          "example": "The tablet version has been on the back burner while we fix mobile."},
    {"word": "on the same page",            "type": "idiom", "meaning": "같은 이해를 공유하다",                   "example": "Let's hold a kickoff meeting to make sure everyone is on the same page."},
    {"word": "pain point",                  "type": "n",     "meaning": "불편함, 사용자가 겪는 문제",              "example": "The biggest pain point was the confusing filter system in search."},
    {"word": "raise the bar",               "type": "idiom", "meaning": "기준을 높이다",                           "example": "Apple's design has consistently raised the bar for the entire industry."},
    {"word": "run it up the flagpole",      "type": "idiom", "meaning": "아이디어를 제안해 반응을 보다",          "example": "Let's run the new onboarding concept up the flagpole in tomorrow's review."},
    {"word": "scope creep",                 "type": "n",     "meaning": "범위가 점진적으로 확장되는 현상",         "example": "Scope creep killed the timeline — we need clearer sign-off on requirements."},
    {"word": "touch base",                  "type": "idiom", "meaning": "간단히 연락하다, 확인하다",               "example": "Let's touch base on Friday to see where the project stands."},
]


def get_daily_words(target_date: date = None) -> dict:
    """날짜를 시드로 오늘의 단어 20개 + 숙어 10개를 반환합니다."""
    d = target_date or date.today()
    ordinal = d.toordinal()

    w_start = ordinal % len(WORDS)
    i_start = ordinal % len(IDIOMS)

    words  = [WORDS[(w_start + i) % len(WORDS)]  for i in range(20)]
    idioms = [IDIOMS[(i_start + i) % len(IDIOMS)] for i in range(10)]

    return {"words": words, "idioms": idioms}


if __name__ == "__main__":
    result = get_daily_words()
    print("=== 단어 20개 ===")
    for i, w in enumerate(result["words"], 1):
        print(f"{i:2d}. [{w['type']:8s}] {w['word']:25s} — {w['meaning']}")
    print("\n=== 숙어 10개 ===")
    for i, w in enumerate(result["idioms"], 1):
        print(f"{i:2d}. {w['word']:35s} — {w['meaning']}")

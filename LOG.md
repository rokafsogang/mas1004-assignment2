# Log

One entry for each recipe, selection or Track B model you train, newest at
the bottom. The numbers come from `experiments.csv`. "Why" and "what it means"
are in your own words: your agent asks you for them and does not make them up.
End the log with your plan for what to try next.

<!-- The form of an entry:

## <date> <tag> (Track A or B)
- changed: what is different from the run before
- why: your reason
- validation: 0.000 (before: 0.000)
- what it means: what you think the result says
-->

## 2026-11-09 Step 1: looking at the photos
- what tells the cities apart (my words): 서울 잠실 주경기장을 통해 알수 있음, 부산 - 해운대 모래사장을 통해 알 수 있음, 도쿄 - JR전철을 통해(초록색), 오사카 - 도톤보리 수로를 통해, 타이페이 - 한자와 타이페이101을 통해 알 수 있음
- sheets: results/curate/look_<city>_00.png (`curate.py look <city> --every 90`)

## 2026-11-09 baseline (Track A)
- changed: nothing; the starter recipe on all 44,257 training photos, seed 0
- why: the reference for every later Track A change
- validation: 0.496 (seoul 0.595, busan 0.386, tokyo 0.624, osaka 0.344, taipei 0.531)
- note: trained on this MacBook's GPU (mps) through scripts/official_mps.py, which runs src/official.py unchanged except that it turns off the channels_last memory format (torch 2.6 on mps stops with "view size is not compatible" otherwise)

## 2026-11-09 balanced (Track A)
- changed: sample_weights in track_a/recipe.py gives each photo 1 / (number of photos of its city), so every city is drawn equally often; nothing else changed
- why (my words): 어차피 최대 양의 사진 (도쿄)꺼를 해야하는데 그거만 13,347할게 아니라 그 시간에 부산도 여러번 보면 정확도가 올라갈거라 생각해서 밸런스 선택
- validation: 0.508 (before: 0.496); seoul 0.496, busan 0.471, tokyo 0.520, osaka 0.435, taipei 0.616
- what it means (my words): 서울 도쿄를 제외한 나머지 도시는 베이스라인보다 높은 정확도를 보여줬는데 그 이유는 아무래도 사진 양이 적었기에 여러번 학습하여 정확도가 올라갔다고 보여짐
- released as track-a-2

## 2026-11-09 b1_mnv3l_320 (Track B)
- changed: first Track B model: MobileNetV3-Large (torchvision IMAGENET1K_V2) at 320 x 320, 6 epochs, every city drawn equally often (--balance), starter training photos only; trained on Colab (cuda). 4.20 million parameters, 0.44 billion multiply-adds
- why: chosen from the options the agent explained: a smaller network that can look at a bigger image than ResNet18 at 224
- validation: 0.563 (seoul 0.554, busan 0.529, tokyo 0.608, osaka 0.486, taipei 0.637); check_submission.py on this Mac: format and limits OK, 0.562
- what it means (my words): 사진을 크게 보면 픽셀이 조각되면서 컴퓨터가 학습을 조금더 세밀하게할 수 있어서 더 높은 값을 추출했다
- note: this run changed the model, the image size, the epochs and the balancing at once compared with train_b.py as given, so it does not say which of them helped
- released as track-b-1

## 2026-11-09 balanced_drop (Track A), my decision from the photos
- looked at: the suspects sheets of the baseline (`curate.py suspects results/baseline_seed0/model.onnx --every 4`), results/curate/suspects_baseline_seed0_<city>_00.png, the 48 training photos per city the baseline thought least likely to be their city
- rule (my words, written before dropping): 사람사진과 음식 사진 그 두개는 어디 나라인지정도까진 추측이 가능해도 도시를 알기는 어려움 그리고 의미없는 자동차 이런거 다 없앰
- changed: dropped the 115 photos I named (seoul 25, busan 29, tokyo 26, osaka 25, taipei 10) with `curate.py drop`; the selection went from 44,257 to 44,142 photos (track_a/dropped.csv); recipe unchanged (balanced)
- validation: 0.510 (before: 0.508); seoul 0.536, busan 0.459, tokyo 0.517, osaka 0.423, taipei 0.614
- what it means (my words): 아무래도 그 많은 사진 중에 115장 밖에 안뺐는데 당연히 정확도가 거의 그대로겠지 정말 다량의 사진을 검수 수거 하지 않는한 크게 안바뀔거야
- released as track-a-3

## 2026-11-09 b2_mnv3l_384 (Track B)
- changed: the image size only, 320 -> 384 (MobileNetV3-Large, 6 epochs, balanced, starter photos, as in b1); trained on Colab (cuda). 4.20 million parameters, 0.63 billion multiply-adds
- why (my words, from b1): 사진을 크게 보면 픽셀이 조각되면서 컴퓨터가 학습을 조금더 세밀하게할 수 있어서 더 높은 값을 추출했다
- validation: 0.570 (before: 0.563); seoul 0.586, busan 0.513, tokyo 0.631, osaka 0.470, taipei 0.649; check_submission.py on this Mac: format and limits OK, 0.569
- what it means (my words): 픽셀을 더 쪼개야한다고 봐
- released as track-b-2

## 2026-11-10 no_flip (Track A)
- changed: deleted T.RandomHorizontalFlip() from train_transform; selection (115 dropped) and everything else as in balanced_drop
- why (my words): 좌우반전을 하면 너 말대로 일본과 같은 반대인 나라에 대한 오류가 생길거라 생각이 들어
- why not the other options (my words): 나머지 옵션은 별로야 확대해봤자 픽셀이 더 세분화되는거 아니니 도움 안될거같고 100%라는건 세상에 없어
- validation: 0.500 (before: 0.510); seoul 0.550, busan 0.430, tokyo 0.511, osaka 0.419, taipei 0.590
- what it means (my words): 예상과 달리 떨어졌고, 이유는 모르겠다
- not released; track-a-3 stays my Track A submission, and track_a/recipe.py goes back to its version

## 2026-11-10 baseline, seed 1 (Track A)
- changed: only the seed, 0 -> 1; the starter recipe (from commit 2414a84, run with MAS1004_RECIPE_DIR=results/starter_recipe) on all 44,257 training photos
- why: to see how much the score moves by chance when nothing else changes
- validation: 0.4956 (seed 0: 0.4961); seoul 0.598, busan 0.383, tokyo 0.607, osaka 0.367, taipei 0.523
- what it means (my words): 같은 설정인데도 값이 살짝 다른걸 보면 기계라고 그 전껄 100%같게 판독하지 못한다는 걸 알았다. 사람처럼 얘네도 시행마다 살짝씩 다르단걸
- note: the commit column of this row is the commit at the time it ran (no_flip); the recipe_sha is the starter recipe's (17ac485223fa, the same as seed 0)

## What I would try next (my words)
- 픽셀을 훨씬 더 많이 줄여서 이걸 반복해서 실험해보고 싶음 내 가설 증명하고 싶음

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

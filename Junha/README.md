## KAPOAI2020
#### by Junha
lger : learning rate, decay_gamma, exp_rate, rounds

### RL
Reinforcement Learning
단순 강화학습

policy_legr_0.2_0.3_0.99_5 : 학습 테스트
policy_legr_0.2_0.05_0.99_1000_run : 각자 1회 복제 후 도망만 다님
policy_legr_0.2_0.05_0.99_1000 : 게임이 종료는 됨
policy_legr_0.2_0.05_0.99_2000 : 각자 1회 복제 후 도망만 다님


### RL_max
Reinforcement Learning with max strategy
자신의 세균수 증가량 + 상대의 세균수 감소량이 최대인 움직임 중에 골라서 이동

policy_mx_legr_0.2_0.1_0.95_1000 : 잘 작동, Easy bot과 대결에서 22:27로 패배

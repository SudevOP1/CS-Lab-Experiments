import numpy as np


def solve_HMM(
    observations: list[int],
    states: list[str],
    start_prob: list[float],
    trans_prob: list[list[float]],
    emit_prob: list[list[float]],
) -> list[str]:

    T: int = len(observations)
    N: int = len(states)

    # dp table
    dp: np.ndarray = np.zeros((N, T))
    prev: np.ndarray = np.zeros((N, T), dtype=int)

    # initialization
    for i in range(N):
        dp[i][0] = start_prob[i] * emit_prob[i][observations[0]]

    # viterbi
    for t in range(1, T):
        for j in range(N):
            max_prob: float = -1.0
            max_state: int = 0
            for i in range(N):
                prob: float = (
                    dp[i][t - 1] * trans_prob[i][j] * emit_prob[j][observations[t]]
                )
                if prob > max_prob:
                    max_prob = prob
                    max_state = i
            dp[j][t] = max_prob
            prev[j][t] = max_state

    # backtrack
    last_state: int = int(np.argmax(dp[:, T - 1]))
    path: list[int] = [0] * T
    path[T - 1] = last_state

    for t in range(T - 2, -1, -1):
        path[t] = int(prev[path[t + 1]][t + 1])

    decoded_states: list[str] = [states[i] for i in path]

    return decoded_states


if __name__ == "__main__":

    states: list[str] = ["Rainy", "Sunny"]

    # Walk=0, Shop=1, Clean=2
    observations: list[int] = [0, 1, 2]
    start_prob: list[float] = [0.6, 0.4]
    trans_prob: list[list[float]] = [
        [0.7, 0.3],
        [0.4, 0.6],
    ]
    emit_prob: list[list[float]] = [
        [0.1, 0.4, 0.5],
        [0.6, 0.3, 0.1],
    ]

    result: list[str] = solve_HMM(
        observations=observations,
        states=states,
        start_prob=start_prob,
        trans_prob=trans_prob,
        emit_prob=emit_prob,
    )

    print("Most likely states:", result)

import numpy as np
import least_squares as lsq
import sys

def gradient_descent(model, eta, max_iterations=1e4, epsilon=1e-5,
                     beta_start=None):
    """
    Gradient descent

    Parameters
    ----------
    model: optimization model object
    eta: learning rate
    max_iterations: maximum number of gradient iterations
    epsilon: tolerance for stopping condition
    beta_start: where to start (otherwise random)

    Output
    ------
    solution: final beta value
    beta_history: beta values from each iteration
    """

    # data from model
    grad_F = model.grad_F
    d = model.d
    # F = model.F

    # initialization
    if beta_start:
        beta_current = beta_start
    else:
        beta_current = np.random.normal(loc=0, scale=1, size=d)

    # keep track of history
    beta_history = []

    for k in range(int(max_iterations)):

        beta_history.append(beta_current)

        # gradient update
        beta_next = beta_current - eta * grad_F(beta_current)

        # relative error stoping condition
        if np.linalg.norm(beta_next - beta_current) <= epsilon*np.linalg.norm(beta_current):
            #  if np.linalg.norm(beta_next) <= epsilon:
            break

        beta_current = beta_next

    return {'solution': beta_current,
            'beta_history': beta_history}

# eta = 0.009
# max_iterations = 10
# epsilon = 0.00002

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: ./gradient_descent <eta> <max_iterations> <epsilon>")
        exit()
    else:
        eta = float(sys.argv[1]) #0.009
        max_iterations = int(sys.argv[2]) #10
        epsilon = float(sys.argv[3]) #0.00002

        x = np.array(([1,1.1,1.2,4],
                        [0.5,2,2,1],
                        [2,0,1,2]))
        y = np.array([1,2,0])
        model = lsq.LeastSquares(x,y)

        result1 = model.F(gradient_descent(model, eta, max_iterations, epsilon)['solution'])

        x = np.array(([1,0,1,3],
                        [0,2,1,1],
                        [2,0,1,1]))
        y = np.array([1,0,1])
        model = lsq.LeastSquares(x,y)
        result2 = model.F(gradient_descent(model, eta, max_iterations, epsilon)['solution'])

        x = np.array(([1,1,1,1],
                        [1,1,1,1],
                        [2,1,2,1]))
        y = np.array([1,0,1])
        model = lsq.LeastSquares(x,y)
        result3 = model.F(gradient_descent(model, eta, max_iterations, epsilon)['solution'])
        print("%s %s %s" %(result1, result2, result3))
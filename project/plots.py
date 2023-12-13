## render the plot function used in this project

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import cm
from parameter import *
config = {"axes.titlesize":"14", "axes.labelsize":"15", "axes.labelweight":"medium"}
rcParams.update(config)
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']

fig_dir = os.path.join(os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2]), "result")
if not os.path.exists(fig_dir):
    os.mkdir(fig_dir)

def plot_tuning_curves(l_route, n_samples):
    """
    Args:
        l_route: 路线总长(cm)
        n_samples: 采样次数
    """
    phi_PF_rad = l_place_field/l_route * 2*np.pi
    x = np.arange(0, l_route, 0.1)
    x_rad = x/l_route * 2*np.pi
    sample = l_route/n_samples
    fig = plt.figure()
    plt.axis([0, l_route, 0.0, 1.0])
    j = -l_place_field/2
    while j <= l_route:
        mid_PF = j/l_route * 2*np.pi + phi_PF_rad/2.0
        tau = [np.exp(-np.power(i-mid_PF, 2)/(2*std**2)) for i in x_rad]
        plt.plot(x, tau, color=cm.jet(j/l_route))
        j = j + sample
    plt.title("Place Cell Tuning Curves")
    plt.xlabel("Position(cm)")
    plt.ylabel(r"$\tau_{i}$(x)")
    fig.savefig(os.path.join(fig_dir, "Place Cell Tuning Curves.png"), dpi=200)
    
def plot_firing_rates(t_sample, n_samples):
    """
    Args:
        t_sample: 采样时间(s)
        n_samples: 采样次数
    """
    from poisson_simu import evaluate_lambda_t
    x_sample = w_mice * t_sample
    sample = x_sample/n_samples
    t = np.arange(0, t_sample, 0.01)
    fig = plt.figure()
    plt.axis([0, t_sample, 0, 20])
    j = 0
    while j <= x_sample:
        _lambda = 20 * evaluate_lambda_t(t, j, 0.0)
        plt.plot(t, _lambda, color=cm.jet(j/x_sample))
        j = j + sample
    plt.title("Firing rates of place cells")
    plt.xlabel("Time(s)")
    plt.ylabel(r"$\lambda_{i}$(x)(Hz)")
    fig.savefig(os.path.join(fig_dir, "Firing rates of place cells.png"), dpi=200)

def plot_STDP_rule(taup, taum, Ap, Am):
    """
    Saves plot of the STDP rule used for learning
    exponential STDP: f(s) = A_p * exp(-s/tau_p) (if s > 0), where s=tpost_{spike}-tpre_{spike}
    :param taup, taum: time constant of weight change
    :param Ap, Am: max amplitude of weight change
    """

    delta_t = np.linspace(-150, 150, 1000)
    delta_w = np.where(delta_t>0, Ap*np.exp(-delta_t/taup), Am*np.exp(delta_t/taum))

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)

    plt.plot(delta_t, delta_w, color="black", label=r"STDP rule $\tau_{\pm}:%s ms, A_{+}:%s pA$" % (taup, Ap))
    plt.legend(loc="upper right")
    plt.xlabel("$\Delta t$ post-pre (ms)")
    plt.ylabel("$\Delta w$ (nS)")
    plt.xlim([-150, 150])
    if Ap == Am:
        plt.title("Symmetric STDP rule")
        plt.ylim([-Ap*0.05, Ap*1.05])
        fig.savefig(os.path.join(fig_dir, "Symmetric STDP rule.png"), dpi=200)
    else:
        plt.title("Asymmetric STDP rule")
        plt.ylim([-Ap*1.05, Ap*1.05])
        fig.savefig(os.path.join(fig_dir, "Asymmetrc STDP rule.png"), dpi=200)
    

def plot_weight_matrix(weight_matrix, title):
    """
    Saves figure with the weight matrix
    :param weight_matrix: numpy array representing the weight matrix
    :param title: title and name of saved img
    """

    fig = plt.figure()
    i = plt.imshow(weight_matrix, cmap="GnBu", origin="lower", interpolation="nearest")
    fig.colorbar(i)
    plt.title(title)
    plt.axis([0, len(weight_matrix), 0, len(weight_matrix)])
    plt.xlabel("Target neuron")
    plt.ylabel("Source neuron")
    fig.savefig(os.path.join(fig_dir, "%s.png" % title), dpi=200)
    
def plot_weight_matrix_avg(weight_matrix, n_pops, title):
    """
    Saves figure with the weight matrix
    :param weight_matrix: numpy array representing the weight matrix
    :param n_pops: number of populations
    :param title: title and name of saved img
    """

    assert len(weight_matrix) % n_pops == 0

    pop_size = int(len(weight_matrix) / n_pops)
    mean_wmx = np.zeros((n_pops, n_pops))
    for i in range(n_pops):
        for j in range(n_pops):
            tmp = weight_matrix[int(i*pop_size):int((i+1)*pop_size), int(j*pop_size):int((j+1)*pop_size)]
            mean_wmx[i, j] = np.mean(tmp)

    fig = plt.figure()
    i = plt.imshow(mean_wmx, cmap="GnBu", origin="lower", interpolation="nearest")
    fig.colorbar(i)
    plt.title(title)
    plt.axis([0, len(mean_wmx), 0, len(mean_wmx)])
    plt.xlabel("Target neuron")
    plt.ylabel("Source neuron")
    fig.savefig(os.path.join(fig_dir, "%s.png" % title), dpi=200)

def plot_raster(spike_times, spike_neurons, title):
    sp = np.asarray(spike_neurons)
    ts = np.asarray(spike_times)

    # get index and time
    elements = np.where(sp > 0.)
    index = elements[1]
    time = ts[elements[0]]
    color = index

    # plot raster
    fig=plt.figure()
    plt.scatter(time, index, c=color, cmap="cividis", marker=".", s=12)
    plt.xlabel("Time(ms)")
    plt.ylabel("Neuron ID")
    plt.title(title)
    fig.savefig(os.path.join(fig_dir, "%s.png" % title), dpi=200)

def plot_spike_events(event_time, ax):
    return None

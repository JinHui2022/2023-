## simulate the spike train produced while the virtual mouse is 
## getting through the track

import numpy as np
import brainpy as bp
from tqdm import tqdm
from poisson_simu import hom_poisson, inhom_poisson
from parameter import *
from file_management import save_place_field, generate_file_path, save_spike_trains

## parameter
outfield_rate = 0.1  # avg. firing rate outside place field [Hz]
infield_rate = 20.0  # avg. in-field firing rate [Hz]
t_max = 405.0  # [s]

def generate_spike_train(n_neurons, place_cell_ratio, ordered=True, seed=1234):
    """
    Generates hippocampal like spike trains (used later for learning the weights via STDP)
    :param n_neurons: #{neurons}
    :param place_cell_ratio: ratio of place cells in the whole population
    :param ordered: bool to order neuronIDs based on their place fields (used for teaching 2 environments - see `stdp_2nd_env.py`)
    :param seed: starting seed for random number generation
    :return: spike_trains - list of lists with indiviual neuron's spikes
    """

    neuronIDs=np.arange(0,n_neurons)

    if ordered:
        np.random.seed(seed)

        p_uniform=1./n_neurons
        tmp=(1-2*2*100*p_uniform)/(n_neurons-200)
        p=np.concatenate([2*p_uniform*np.ones(100),tmp*np.ones(n_neurons-2*100),2*p_uniform*np.ones(100)]) # oversample (double prop.) the two ends of the track
        place_cells=np.sort(np.random.choice(neuronIDs,int(n_neurons*place_cell_ratio),p=p,replace=False),kind="mergesort")
        phi_starts=np.sort(np.random.rand(n_neurons),kind="mergesort")
        phi_starts -= 0.1*np.pi  # shift half a PF against boundary effects (mid_PFs will be in [0, 2*np.pi]...)

    place_fields={neuron_id:phi_starts[i] for i, neuron_id in enumerate(place_cells)}

    ## generate spike trains
    spike_trains=[]
    for neuron_id in tqdm(range(0, n_neurons)):
        if neuron_id in place_fields:
            spike_train=inhom_poisson(infield_rate,t_max,place_fields[neuron_id],seed=seed)
        else:
            spike_train=hom_poisson(outfield_rate,t_max,seed)
        spike_trains.append(spike_train)
        seed+=1
    
    return place_fields,spike_trains

place_fields,spike_trains=generate_spike_train(n_neurons=n_PC,place_cell_ratio=place_cell_ratio)

file_place_fields="place_fields.txt"
file_spike_trains="spike_trains.npz"

## save the result
save_place_field(place_fields,file_place_fields)
save_spike_trains(spike_trains,file_spike_trains)